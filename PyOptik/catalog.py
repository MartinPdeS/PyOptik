"""Catalog and upstream-identity support for optical material data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import unquote, urlparse
import logging

import yaml

from PyOptik.directories import libraries_path, user_data_path
from PyOptik.material_type import MaterialType
from PyOptik.utils import download_yml_file

logger = logging.getLogger(__name__)

UPSTREAM_CATALOG_URL = (
    "https://raw.githubusercontent.com/polyanskiy/refractiveindex.info-database/"
    "main/database/catalog-nk.yml"
)


@dataclass(frozen=True)
class MaterialId:
    """Canonical upstream identity: shelf, book, and page."""

    shelf: str
    book: str
    page: str

    def __str__(self) -> str:
        """Return the canonical ``shelf/book/page`` path."""
        return f"{self.shelf}/{self.book}/{self.page}"

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
    legacy_name: Optional[str] = None
    data_root: Optional[Path] = None

    @property
    def local_path(self) -> Optional[Path]:
        """Return the local cached path, if a data path is known."""
        if self.data_path is None or self.data_root is None:
            return None
        return self.data_root / self.data_path

    def __str__(self) -> str:
        """Return the canonical identifier of this page."""
        return str(self.id)

    def load(self):
        """Load this page as the appropriate PyOptik material object."""
        from PyOptik.material.sellmeier_class import SellmeierMaterial
        from PyOptik.material.tabulated_class import TabulatedMaterial

        if self.local_path is not None and self.local_path.exists():
            with self.local_path.open("r") as stream:
                document = yaml.safe_load(stream) or {}
            entries = document.get("DATA", [])
            if any("formula" in str(entry.get("type", "")) for entry in entries):
                return SellmeierMaterial(self.name, file_path=self.local_path)
            if any("tabulated" in str(entry.get("type", "")) for entry in entries):
                return TabulatedMaterial(self.name, file_path=self.local_path)
            raise ValueError(f"No supported optical dataset found in {self.local_path}")

        if self.legacy_name is not None:
            if self.data_path and "/nk/" in self.data_path:
                return TabulatedMaterial(self.legacy_name)
            return SellmeierMaterial(self.legacy_name)
        raise FileNotFoundError(f"Material page data is not available: {self.id}")


class MaterialCatalog:
    """Browse and download materials using the upstream hierarchy."""

    def __init__(self, catalog_file: Optional[Path | str] = None, data_root: Optional[Path | str] = None):
        """Create a material catalog.

        Parameters
        ----------
        catalog_file : pathlib.Path or str, optional
            Path to an upstream ``catalog-nk.yml`` file. If omitted, the
            packaged catalog is used when available, otherwise the legacy
            PyOptik repertoire is converted into catalog entries.
        data_root : pathlib.Path or str, optional
            Root directory for hierarchy-preserving downloaded data.
        """
        self.data_root = Path(data_root or (user_data_path / "rii")).expanduser()
        self._pages: dict[MaterialId, MaterialPage] = {}
        self._aliases: dict[str, MaterialId] = {}
        if catalog_file is not None:
            self.load_catalog(catalog_file)
        else:
            default_catalog = libraries_path / "catalog-nk.yml"
            if default_catalog.exists():
                self.load_catalog(default_catalog)
            else:
                self._load_legacy_repertoire(libraries_path / "repertoire.yml")

    @classmethod
    def from_upstream(cls, data_root: Optional[Path | str] = None, url: str = UPSTREAM_CATALOG_URL):
        """Download and load the current upstream catalog index."""
        root = Path(data_root or (user_data_path / "rii")).expanduser()
        catalog_file = root / "catalog-nk.yml"
        download_yml_file(
            url=url,
            filename=catalog_file.stem,
            save_location=MaterialType.SELLMEIER,
            destination=catalog_file,
        )
        return cls(catalog_file=catalog_file, data_root=root)

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

    def _load_legacy_repertoire(self, repertoire_file: Path) -> None:
        """Create a compatibility catalog from PyOptik's old URL map."""
        with repertoire_file.open("r") as stream:
            repertoire = yaml.safe_load(stream) or {}
        for kind, entries in repertoire.items():
            material_type = MaterialType(kind)
            for alias, url in (entries or {}).items():
                parsed = [unquote(part) for part in urlparse(url).path.split("/") if part]
                try:
                    data_index = parsed.index("data")
                    path_parts = parsed[data_index + 1:]
                    data_path = "/".join(path_parts)
                    page = Path(path_parts[-1]).stem
                    book = "/".join(path_parts[1:-1]) or "unknown"
                    shelf = path_parts[0]
                except (ValueError, IndexError):
                    logger.warning("Could not derive hierarchy from URL: %s", url)
                    continue
                identifier = MaterialId(shelf, book, page)
                self._pages.setdefault(
                    identifier,
                    MaterialPage(
                        id=identifier,
                        name=page,
                        data_path=data_path,
                        source_url=url,
                        legacy_name=alias,
                        data_root=self.data_root,
                    ),
                )
                self._aliases[alias] = identifier

    def pages(self, shelf: Optional[str] = None, book: Optional[str] = None) -> list[MaterialPage]:
        """Return pages filtered by shelf and/or book."""
        return sorted(
            (page for page in self._pages.values()
             if (shelf is None or page.id.shelf == shelf)
             and (book is None or page.id.book == book)),
            key=lambda page: page.id.key,
        )

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

    def get(self, identifier: MaterialId | str, book: Optional[str] = None, page: Optional[str] = None) -> MaterialPage:
        """Get a page by ``MaterialId``, canonical path, or components."""
        if isinstance(identifier, MaterialId):
            key = identifier
        elif book is not None and page is not None:
            key = MaterialId(identifier, book, page)
        elif identifier in self._aliases:
            key = self._aliases[identifier]
        else:
            parts = identifier.split("/")
            if len(parts) < 3:
                raise KeyError(f"Unknown material page: {identifier}")
            key = MaterialId(parts[0], "/".join(parts[1:-1]), parts[-1])
        try:
            return self._pages[key]
        except KeyError as error:
            raise KeyError(f"Unknown material page: {key}") from error

    def download(self, shelf: Optional[str] = None, book: Optional[str] = None) -> list[MaterialPage]:
        """Download all matching pages into a hierarchy-preserving cache."""
        selected = self.pages(shelf=shelf, book=book)
        for material_page in selected:
            if not material_page.source_url or not material_page.data_path:
                logger.warning("No download URL for material page %s", material_page.id)
                continue
            destination = self.data_root / material_page.data_path
            download_yml_file(
                url=material_page.source_url,
                filename=destination.stem,
                save_location=MaterialType.SELLMEIER,
                destination=destination,
            )
            logger.info("Downloaded material page %s", material_page.id)
        return selected

    def __iter__(self) -> Iterable[MaterialPage]:
        """Iterate over catalog pages in canonical identifier order."""
        return iter(self.pages())
