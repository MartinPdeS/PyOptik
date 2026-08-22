"""Catalog and upstream-identity support for optical material data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional
from datetime import datetime, timezone
import hashlib
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
import zipfile

import yaml
import requests

from PyOptik.directories import user_data_path
from PyOptik.material_type import MaterialType
from PyOptik.utils import download_yml_file

logger = logging.getLogger(__name__)

UPSTREAM_CATALOG_URL = (
    "https://raw.githubusercontent.com/polyanskiy/refractiveindex.info-database/"
    "main/database/catalog-nk.yml"
)
UPSTREAM_ARCHIVE_URL = (
    "https://github.com/polyanskiy/refractiveindex.info-database/"
    "archive/refs/heads/main.zip"
)
UPSTREAM_TIMEOUT = 10


@dataclass(frozen=True)
class MaterialId:
    """Canonical upstream identity: shelf, book, and page."""

    shelf: str
    book: str
    page: str

    def __str__(self) -> str:
        """Return the canonical ``shelf/book/page`` path."""
        return f"{self.shelf}/{self.book}/{self.page}"

    def __repr__(self) -> str:
        """Return an unambiguous representation using the canonical ID."""
        return f"MaterialId({self.key!r})"

    @property
    def key(self) -> str:
        """Return the canonical identifier as a string."""
        return str(self)


@dataclass
class MaterialPage:
    """A catalog page and its associated optical-data file."""

    id: MaterialId
    name: str
    data_path: Optional[str] = None
    source_url: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None
    data_root: Optional[Path] = None

    @property
    def available(self) -> bool:
        """Whether this page's data file is available in the local cache."""
        return self.local_path is not None and self.local_path.exists()

    @property
    def reference(self) -> Optional[str]:
        """Return the local source reference, when the page has been cached."""
        if not self.available:
            return None
        try:
            with self.local_path.open("r") as stream:
                reference = (yaml.safe_load(stream) or {}).get("REFERENCES")
                return str(reference) if reference is not None else None
        except (OSError, yaml.YAMLError):
            return None

    def provenance(self) -> dict:
        """Return the canonical identity and source information for this page.

        Returns
        -------
        dict
            Serializable identity, cache-path, availability, and source fields.
        """
        return {
            "id": self.id.key,
            "name": self.name,
            "description": self.description,
            "reference": self.reference,
            "source_url": self.source_url,
            "local_path": str(self.local_path) if self.local_path else None,
            "available": self.available,
        }

    @property
    def local_path(self) -> Optional[Path]:
        """Return the local cached path, if a data path is known."""
        if self.data_path is None or self.data_root is None:
            return None
        return self.data_root / self.data_path

    def __str__(self) -> str:
        """Return the canonical identifier of this page."""
        return str(self.id)

    def __repr__(self) -> str:
        """Return a concise description of this catalog page.

        The representation intentionally omits YAML metadata and source URLs,
        which may be large or distracting when inspecting a catalog.
        """
        state = "available" if self.available else "missing"
        return f"MaterialPage(id={self.id.key!r}, name={self.name!r}, data={state!r})"

    def load(self, *, interpolation: str = "linear"):
        """Load this page as the appropriate PyOptik material object.

        Parameters
        ----------
        interpolation : {"linear", "pchip"}, optional
            Tabulated-data interpolation method. Formula materials ignore this
            option.

        Returns
        -------
        SellmeierMaterial or TabulatedMaterial
            Material model selected from the local YAML data type.

        Raises
        ------
        FileNotFoundError
            If the page has not been downloaded locally.
        ValueError
            If the file contains no supported optical dataset.
        """
        from PyOptik.material.sellmeier_class import SellmeierMaterial
        from PyOptik.material.tabulated_class import TabulatedMaterial

        if self.local_path is not None and self.local_path.exists():
            with self.local_path.open("r") as stream:
                document = yaml.safe_load(stream) or {}
            entries = document.get("DATA", [])
            if any("formula" in str(entry.get("type", "")) for entry in entries):
                material = SellmeierMaterial(self.name, file_path=self.local_path)
                material.catalog_id = self.id.key
                material.source_url = self.source_url
                return material
            if any("tabulated" in str(entry.get("type", "")) for entry in entries):
                material = TabulatedMaterial(
                    self.name,
                    file_path=self.local_path,
                    interpolation=interpolation,
                )
                material.catalog_id = self.id.key
                material.source_url = self.source_url
                return material
            raise ValueError(f"No supported optical dataset found in {self.local_path}")

        raise FileNotFoundError(
            f"Material data for '{self.id}' is not available locally. "
            "Download the upstream snapshot with Python using "
            "'from PyOptik import download_snapshot; download_snapshot()' "
            "or from the terminal with 'pyoptik setup'."
        )


class MaterialCatalog:
    """Browse and download materials using the upstream hierarchy."""

    def __init__(self, catalog_file: Optional[Path | str] = None, data_root: Optional[Path | str] = None):
        """Create a material catalog.

        Parameters
        ----------
        catalog_file : pathlib.Path or str, optional
            Path to an upstream ``catalog-nk.yml`` file. If omitted, the
            packaged catalog is used when available. If no catalog is
            available, the catalog starts empty and the user can call
            :func:`download_snapshot`.
        data_root : pathlib.Path or str, optional
            Root directory for hierarchy-preserving downloaded data.
        """
        self.data_root = Path(data_root or (user_data_path / "rii")).expanduser()
        self._pages: dict[MaterialId, MaterialPage] = {}
        if catalog_file is not None:
            self.load_catalog(catalog_file)
        logger.info("Initialized catalog with %s material pages", len(self._pages))

    def __repr__(self) -> str:
        """Return a concise summary of the catalog state.

        Returns
        -------
        str
            Class name, number of indexed pages, and local data root. Page
            metadata is deliberately excluded to keep interactive output
            readable for catalogs containing thousands of materials.
        """
        return f"MaterialCatalog(pages={len(self._pages)}, data_root={str(self.data_root)!r})"

    @classmethod
    def from_upstream(cls, data_root: Optional[Path | str] = None, url: str = UPSTREAM_CATALOG_URL):
        """Download and load the current upstream catalog index.

        Parameters
        ----------
        data_root : pathlib.Path or str, optional
            Directory used for the catalog index and downloaded pages.
        url : str, optional
            Catalog YAML URL.

        Returns
        -------
        MaterialCatalog
            Catalog indexed from the downloaded upstream YAML file.
        """
        root = Path(data_root or (user_data_path / "rii")).expanduser()
        catalog_file = root / "catalog-nk.yml"
        download_yml_file(
            url=url,
            filename=catalog_file.stem,
            save_location=MaterialType.SELLMEIER,
            destination=catalog_file,
        )
        catalog = cls(catalog_file=catalog_file, data_root=root)
        manifest = catalog._read_manifest()
        manifest["catalog"] = {
            "source": url,
            "mode": "pages",
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        for material_page in catalog.pages():
            if not material_page.data_path:
                continue
            destination = root / material_page.data_path
            if destination.exists():
                manifest["pages"][material_page.id.key] = {
                    "source_url": material_page.source_url,
                    "local_path": str(destination.relative_to(root)),
                    "status": "snapshot",
                    "sha256": catalog._sha256(destination),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
        catalog._write_manifest(manifest)
        return catalog

    @classmethod
    def from_snapshot(
        cls,
        data_root: Optional[Path | str] = None,
        url: str = UPSTREAM_ARCHIVE_URL,
        force: bool = False,
        progress=None,
    ):
        """Download and extract the complete upstream database snapshot.

        Parameters
        ----------
        data_root : pathlib.Path or str, optional
            Root directory where the upstream ``database`` contents are
            extracted.
        url : str, optional
            URL of a ZIP archive containing the upstream database.
        force : bool, optional
            Download the archive even when a catalog is already present.
        progress : callable, optional
            Callback receiving ``(downloaded_bytes, total_bytes)`` while the
            archive is downloaded.

        Returns
        -------
        MaterialCatalog
            Catalog backed by the extracted snapshot.
        """
        root = Path(data_root or (user_data_path / "rii")).expanduser()
        catalog_file = root / "catalog-nk.yml"
        existing_manifest = None
        if catalog_file.exists() and not force:
            try:
                with (root / "manifest.json").open("r") as stream:
                    existing_manifest = json.load(stream)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_manifest = None
        if (
            catalog_file.exists()
            and not force
            and existing_manifest is not None
            and existing_manifest.get("catalog", {}).get("mode") == "snapshot"
        ):
            existing_catalog = cls(catalog_file=catalog_file, data_root=root)
            complete = all(
                page.data_path is None
                or (page.local_path is not None and page.local_path.exists())
                for page in existing_catalog.pages()
            )
            if complete:
                logger.info("Using existing upstream snapshot at %s", root)
                return existing_catalog
            logger.warning("Existing upstream snapshot is incomplete; refreshing it")

        logger.info("Downloading upstream database snapshot from %s", url)
        response = requests.get(url, timeout=UPSTREAM_TIMEOUT, stream=True)
        response.raise_for_status()
        root.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(prefix="pyoptik-snapshot-") as temporary:
            archive = Path(temporary) / "database.zip"
            total_bytes = int(getattr(response, "headers", {}).get("content-length", 0))
            downloaded_bytes = 0
            if hasattr(response, "iter_content"):
                with archive.open("wb") as stream:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if not chunk:
                            continue
                        stream.write(chunk)
                        downloaded_bytes += len(chunk)
                        if progress:
                            progress(downloaded_bytes, total_bytes)
            else:
                content = response.content
                archive.write_bytes(content)
                if progress:
                    progress(len(content), len(content))
            with zipfile.ZipFile(archive) as bundle:
                members = bundle.namelist()
                database_member = next(
                    (name for name in members if "/database/" in name),
                    None,
                )
                if database_member is None:
                    raise ValueError("Upstream archive does not contain a database directory")
                database_prefix = database_member.split("/database/", 1)[0] + "/database/"
                root_resolved = root.resolve()
                for member in members:
                    if not member.startswith(database_prefix) or member == database_prefix:
                        continue
                    relative = Path(member[len(database_prefix):])
                    if relative.parts and relative.parts[0] == "data":
                        relative = Path(*relative.parts[1:])
                    if not relative.parts:
                        continue
                    destination = (root / relative).resolve()
                    if not destination.is_relative_to(root_resolved):
                        raise ValueError(f"Unsafe path in upstream archive: {member}")
                    if member.endswith("/"):
                        destination.mkdir(parents=True, exist_ok=True)
                    else:
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        destination.write_bytes(bundle.read(member))

        catalog = cls(catalog_file=catalog_file, data_root=root)
        manifest = catalog._read_manifest()
        manifest["catalog"] = {
            "source": url,
            "mode": "snapshot",
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        for material_page in catalog.pages():
            if material_page.local_path is None or not material_page.local_path.exists():
                continue
            manifest["pages"][material_page.id.key] = {
                "source_url": material_page.source_url,
                "local_path": str(material_page.local_path.relative_to(root)),
                "status": "snapshot",
                "sha256": catalog._sha256(material_page.local_path),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        catalog._write_manifest(manifest)
        logger.info("Extracted upstream snapshot with %s catalog pages", len(catalog.pages()))
        return catalog

    def load_catalog(self, catalog_file: Path | str) -> None:
        """Load an upstream ``catalog-nk.yml`` file."""
        catalog_file = Path(catalog_file)
        with catalog_file.open("r") as stream:
            document = yaml.safe_load(stream) or []
        self._pages.clear()

        def walk(node, shelf=None, book=None):
            """Recursively convert catalog YAML nodes into material pages."""
            if isinstance(node, list):
                for child in node:
                    walk(child, shelf, book)
            elif isinstance(node, dict):
                current_shelf = node.get("SHELF", shelf)
                current_book = node.get("BOOK", book)
                if node.get("PAGE") and current_shelf and current_book:
                    page = str(node["PAGE"])
                    identifier = MaterialId(str(current_shelf), str(current_book), page)
                    data_path = node.get("data")
                    source_url = (
                        f"https://refractiveindex.info/database/data/{data_path}"
                        if data_path else None
                    )
                    self._pages[identifier] = MaterialPage(
                        id=identifier,
                        name=page,
                        data_path=data_path,
                        source_url=source_url,
                        description=node.get("name"),
                        data_root=self.data_root,
                    )
                walk(node.get("content", []), current_shelf, current_book)

        walk(document)
        logger.info("Loaded %s material pages from %s", len(self._pages), catalog_file)

    def pages(self, shelf: Optional[str] = None, book: Optional[str] = None) -> list[MaterialPage]:
        """Return pages filtered by shelf and/or book.

        Parameters
        ----------
        shelf, book : str, optional
            Canonical hierarchy filters.

        Returns
        -------
        list of MaterialPage
            Matching pages in canonical identifier order.
        """
        return sorted(
            (page for page in self._pages.values()
             if (shelf is None or page.id.shelf == shelf)
             and (book is None or page.id.book == book)),
            key=lambda page: page.id.key,
        )

    def search(
        self,
        query: Optional[str] = None,
        *,
        shelf: Optional[str] = None,
        book: Optional[str] = None,
        source: Optional[str] = None,
        reference: Optional[str] = None,
        available: Optional[bool] = None,
    ) -> list[MaterialPage]:
        """Search catalog pages by text and provenance-aware filters.

        Text matching is case-insensitive and covers canonical IDs, page names,
        catalog descriptions, and source URLs. ``reference`` filters the
        local YAML ``REFERENCES`` field, so it requires cached pages. Set
        ``available=True`` to restrict results to local pages. Each result
        exposes :meth:`MaterialPage.provenance` for a source record.

        Parameters
        ----------
        query : str, optional
            Case-insensitive text query.
        shelf, book : str, optional
            Canonical hierarchy filters.
        source : str, optional
            Case-insensitive source-URL filter.
        reference : str, optional
            Case-insensitive local YAML reference filter.
        available : bool, optional
            Restrict results by cache availability.

        Returns
        -------
        list of MaterialPage
            Matching pages in canonical identifier order.
        """
        terms = (query or "").casefold()
        source_term = source.casefold() if source else None
        reference_term = reference.casefold() if reference else None
        matched = []
        for material_page in self.pages(shelf=shelf, book=book):
            haystack = " ".join(
                value for value in (
                    material_page.id.key,
                    material_page.name,
                    material_page.description,
                    material_page.source_url,
                ) if value
            ).casefold()
            if terms and terms not in haystack:
                continue
            if source_term and source_term not in (material_page.source_url or "").casefold():
                continue
            if reference_term and reference_term not in (material_page.reference or "").casefold():
                continue
            if available is not None and material_page.available is not available:
                continue
            matched.append(material_page)
        return matched

    def shelves(self) -> list[str]:
        """Return sorted upstream shelf identifiers.

        Returns
        -------
        list of str
            Unique shelf identifiers represented in the catalog.
        """
        return sorted({page.id.shelf for page in self._pages.values()})

    def books(self, shelf: Optional[str] = None) -> list[str]:
        """Return sorted book identifiers, optionally within one shelf.

        Parameters
        ----------
        shelf : str, optional
            Restrict the result to this shelf.

        Returns
        -------
        list of str
            Unique book identifiers.
        """
        return sorted({page.id.book for page in self.pages(shelf=shelf)})

    @property
    def manifest_path(self) -> Path:
        """Return the path of the resumable download manifest."""
        return self.data_root / "manifest.json"

    def _read_manifest(self) -> dict:
        """Read the download manifest, tolerating a missing or invalid file."""
        if not self.manifest_path.exists():
            return {"catalog": {}, "pages": {}}
        try:
            with self.manifest_path.open("r") as stream:
                manifest = json.load(stream)
            manifest.setdefault("catalog", {})
            manifest.setdefault("pages", {})
            return manifest
        except (OSError, json.JSONDecodeError) as error:
            logger.warning("Ignoring invalid download manifest %s: %s", self.manifest_path, error)
            return {"catalog": {}, "pages": {}}

    def _write_manifest(self, manifest: dict) -> None:
        """Atomically write the download manifest after a page completes."""
        self.data_root.mkdir(parents=True, exist_ok=True)
        temporary = self.manifest_path.with_suffix(".json.tmp")
        with temporary.open("w") as stream:
            json.dump(manifest, stream, indent=2, sort_keys=True)
            stream.write("\n")
        temporary.replace(self.manifest_path)

    @staticmethod
    def _sha256(path: Path) -> str:
        """Return the SHA-256 digest of a local file."""
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()

    def verify_integrity(self) -> dict[MaterialId, bool]:
        """Verify checksums recorded in the local download manifest.

        Pages without a recorded checksum are omitted. The returned mapping is
        keyed by canonical material identity, allowing callers to identify and
        re-download only altered or incomplete cached files.

        Returns
        -------
        dict of MaterialId to bool
            Whether every manifest-recorded page matches its SHA-256 digest.
        """
        checked = {}
        for key, record in self._read_manifest().get("pages", {}).items():
            expected = record.get("sha256")
            relative_path = record.get("local_path")
            if not expected or not relative_path:
                continue
            path = self.data_root / relative_path
            parts = key.split("/")
            if len(parts) < 3:
                continue
            identifier = MaterialId(parts[0], "/".join(parts[1:-1]), parts[-1])
            checked[identifier] = path.is_file() and self._sha256(path) == expected
        return checked

    def get(self, identifier: MaterialId | str, book: Optional[str] = None, page: Optional[str] = None) -> MaterialPage:
        """Get a page by ``MaterialId``, canonical path, or components.

        Parameters
        ----------
        identifier : MaterialId or str
            Canonical identifier, or shelf when ``book`` and ``page`` are set.
        book, page : str, optional
            Remaining canonical hierarchy components.

        Returns
        -------
        MaterialPage
            The selected catalog page.

        Raises
        ------
        KeyError
            If the identifier is unknown or incomplete.
        """
        if isinstance(identifier, MaterialId):
            key = identifier
        elif book is not None and page is not None:
            key = MaterialId(identifier, book, page)
        else:
            parts = identifier.split("/")
            if len(parts) < 3:
                raise KeyError(f"Unknown material page: {identifier}")
            key = MaterialId(parts[0], "/".join(parts[1:-1]), parts[-1])
        try:
            return self._pages[key]
        except KeyError as error:
            raise KeyError(f"Unknown material page: {key}") from error

    def download(
        self,
        shelf: Optional[str] = None,
        book: Optional[str] = None,
        *,
        force: bool = False,
        continue_on_error: bool = False,
        progress=None,
        workers: int = 1,
    ) -> list[MaterialPage]:
        """Download matching pages into a resumable hierarchical cache.

        Parameters
        ----------
        shelf, book : str, optional
            Optional hierarchy filters.
        force : bool, optional
            Re-download files even when a local copy already exists.
        continue_on_error : bool, optional
            Record failures and continue with remaining pages. If false, the
            first download error is raised.
        progress : callable, optional
            Callback receiving ``(completed, total, page, status)`` after each
            page. Status is one of ``"downloaded"``, ``"cached"``,
            ``"skipped"``, ``"snapshot"``, or ``"error"``.
        workers : int, optional
            Number of concurrent page downloads. Keep this bounded to respect
            the upstream service.

        Returns
        -------
        list of MaterialPage
            Pages selected by the filters.
        """
        if workers < 1:
            raise ValueError("workers must be at least 1")
        selected = self.pages(shelf=shelf, book=book)
        manifest = self._read_manifest()
        total = len(selected)

        def fetch(item):
            """Download one page and return a manifest-ready result tuple."""
            number, material_page = item
            if not material_page.source_url or not material_page.data_path:
                return number, material_page, "skipped", None, None
            destination = self.data_root / material_page.data_path
            try:
                was_cached = destination.exists() and not force
                download_yml_file(
                    url=material_page.source_url,
                    filename=destination.stem,
                    save_location=MaterialType.SELLMEIER,
                    destination=destination,
                    overwrite=force,
                )
                status = "cached" if was_cached else "downloaded"
                record = {
                    "source_url": material_page.source_url,
                    "local_path": str(destination.relative_to(self.data_root)),
                    "status": status,
                    "sha256": self._sha256(destination),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
                return number, material_page, status, record, None
            except Exception as error:
                record = {
                    "source_url": material_page.source_url,
                    "local_path": str(destination.relative_to(self.data_root)),
                    "status": "error",
                    "error": str(error),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
                return number, material_page, "error", record, error

        items = list(enumerate(selected, start=1))
        if workers == 1:
            results = (fetch(item) for item in items)
            executor = None
        else:
            executor = ThreadPoolExecutor(max_workers=workers)
            results = (future.result() for future in as_completed(
                [executor.submit(fetch, item) for item in items]
            ))
        try:
            for number, material_page, status, record, error in results:
                if record is not None:
                    manifest["pages"][material_page.id.key] = record
                if status == "skipped":
                    logger.warning("No download URL for material page %s", material_page.id)
                elif status == "error":
                    logger.error("[%s/%s] failed: %s (%s)", number, total, material_page.id, error)
                    if not continue_on_error:
                        self._write_manifest(manifest)
                        raise error
                else:
                    logger.info("[%s/%s] %s: %s", number, total, status, material_page.id)
                self._write_manifest(manifest)
                if progress:
                    progress(number, total, material_page, status)
        finally:
            if executor is not None:
                executor.shutdown(wait=True)
        return selected

    def download_all(
        self,
        *,
        force: bool = False,
        continue_on_error: bool = True,
        progress=None,
        workers: int = 1,
    ) -> list[MaterialPage]:
        """Download every page in the catalog.

        Parameters
        ----------
        force : bool, optional
            Re-download all files instead of using local copies.
        continue_on_error : bool, optional
            Continue after failed pages and record failures in the manifest.
        progress : callable, optional
            Callback receiving ``(completed, total, page, status)``.
        workers : int, optional
            Number of concurrent page downloads.

        Returns
        -------
        list of MaterialPage
            All catalog pages.
        """
        return self.download(
            force=force,
            continue_on_error=continue_on_error,
            progress=progress,
            workers=workers,
        )

    def __iter__(self) -> Iterable[MaterialPage]:
        """Iterate over catalog pages in canonical identifier order."""
        return iter(self.pages())


def download_snapshot(
    data_root: Optional[Path | str] = None,
    *,
    force: bool = False,
    progress=None,
) -> MaterialCatalog:
    """Download and activate the complete upstream material snapshot.

    Parameters
    ----------
    data_root : pathlib.Path or str, optional
        Directory where the snapshot should be stored.
    force : bool, optional
        Refresh an existing snapshot.
    progress : callable, optional
        Callback receiving ``(downloaded_bytes, total_bytes)``.

    Returns
    -------
    MaterialCatalog
        Catalog backed by the downloaded snapshot.

    Examples
    --------
    >>> from PyOptik import download_snapshot
    >>> catalog = download_snapshot()
    >>> silver = catalog.get("main/Ag/Johnson").load()
    """
    return MaterialCatalog.from_snapshot(
        data_root=data_root,
        force=force,
        progress=progress,
    )
