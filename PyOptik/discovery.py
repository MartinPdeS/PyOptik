"""Human-readable material discovery backed by canonical catalog identities."""

from difflib import get_close_matches
from pathlib import Path
import unicodedata

from .catalog import MaterialCatalog, MaterialPage


# Aliases identify a material family; documented defaults are applied only
# by load_material, never by discovery or explicit source selection.
_BOOK_ALIASES = {
    "sio2": ("main", "SiO2"),
    "silica": ("main", "SiO2"),
    "fusedsilica": ("main", "SiO2"),
    "au": ("main", "Au"),
    "gold": ("main", "Au"),
    "ag": ("main", "Ag"),
    "silver": ("main", "Ag"),
    "si": ("main", "Si"),
    "silicon": ("main", "Si"),
    "h2o": ("main", "H2O"),
    "water": ("main", "H2O"),
}
_PAGE_ALIASES = {
    "bk7": "specs/SCHOTT-optical/N-BK7",
    "nbk7": "specs/SCHOTT-optical/N-BK7",
}


# These source choices are part of the convenience API, not a ranking of
# measurement quality. Keep canonical IDs explicit and document any changes.
_DEFAULT_SOURCES = {
    ("main", "SiO2"): "main/SiO2/Malitson",
    ("main", "Au"): "main/Au/Johnson",
    ("main", "Ag"): "main/Ag/Johnson",
    ("main", "H2O"): "main/H2O/Hale",
}


def _normalize(value: str) -> str:
    """Normalize case, accents, spacing, and punctuation for exact matching."""
    value = unicodedata.normalize("NFKD", value).casefold()
    return "".join(character for character in value if character.isalnum())


def _nonempty(value: str, label: str) -> str:
    """Validate a required non-empty name or source argument."""
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string.")
    if not _normalize(value):
        raise ValueError(f"{label} must not be empty.")
    return value.strip()


def _get_catalog(catalog: MaterialCatalog | None, data_root: Path | str | None) -> MaterialCatalog:
    """Read a local index or obtain the snapshot on the first lookup."""
    if catalog is not None:
        if data_root is not None:
            raise ValueError("Pass either catalog or data_root, not both.")
        return catalog
    from .directories import user_data_path

    root = Path(data_root or (user_data_path / "rii")).expanduser()
    catalog_file = root / "catalog-nk.yml"
    if catalog_file.is_file():
        return MaterialCatalog(catalog_file=catalog_file, data_root=root)
    return MaterialCatalog.from_snapshot(data_root=root)


def _candidates(name: str, catalog: MaterialCatalog) -> list[MaterialPage]:
    """Resolve exact identities and families before falling back to text search."""
    if "/" in name:
        return [catalog.get(name)]
    normalized = _normalize(name)
    if normalized in _PAGE_ALIASES:
        return [catalog.get(_PAGE_ALIASES[normalized])]
    if normalized in _BOOK_ALIASES:
        shelf, book = _BOOK_ALIASES[normalized]
        return catalog.pages(shelf=shelf, book=book)
    pages = catalog.pages()
    exact_books = [page for page in pages if _normalize(page.id.book) == normalized]
    if exact_books:
        return exact_books
    exact_pages = [page for page in pages if _normalize(page.id.page) == normalized]
    if exact_pages:
        return exact_pages
    return catalog.search(name)


def _select_source(pages: list[MaterialPage], source: str) -> list[MaterialPage]:
    """Prefer an exact page ID to a partial source or description match."""
    normalized = _normalize(source)
    exact = [page for page in pages if normalized in (
        _normalize(page.id.page), _normalize(page.id.key),
    )]
    if exact:
        return exact
    return [page for page in pages if any(
        normalized in _normalize(value)
        for value in (page.id.page, page.description or "")
    )]


class AmbiguousMaterialError(ValueError):
    """A name or source matches several scientific datasets.

    Attributes
    ----------
    candidates : list of MaterialPage
        Matching pages in canonical order, including descriptions and provenance.
    """

    def __init__(self, name: str, candidates: list[MaterialPage]):
        """List candidate identities and show how to select a source explicitly."""
        self.candidates = candidates
        lines = [f"Multiple datasets found for {name!r}:"]
        lines.extend(
            f"  {number}. {page.id.key}: {page.description or page.name}"
            for number, page in enumerate(candidates, start=1)
        )
        first = candidates[0]
        lines.extend([
            "",
            f"Select a source with material({name!r}, source={first.id.page!r}),",
            f"or use a canonical ID: material({first.id.key!r}).",
            "Use find_materials(name) to inspect candidates and provenance.",
        ])
        super().__init__("\n".join(lines))


def find_materials(
    name: str,
    *,
    source: str | None = None,
    catalog: MaterialCatalog | None = None,
    data_root: Path | str | None = None,
) -> list[MaterialPage]:
    """Find material datasets by common name, formula, or canonical identity.

    Parameters
    ----------
    name : str
        Common name (gold, fused silica, water), formula (Au, SiO2), glass
        name (BK7, N-BK7), or canonical shelf/book/page ID. BK7 is an explicit
        alias for SCHOTT N-BK7. Other aliases select families; find_materials always returns all sources.
    source : str, optional
        Page ID, canonical ID, or source-description text. Exact page IDs
        take precedence over partial matches.
    catalog : MaterialCatalog, optional
        Existing catalog, including custom or offline catalogs.
    data_root : pathlib.Path or str, optional
        Snapshot location. Cannot be combined with catalog.

    Returns
    -------
    list of MaterialPage
        Candidates in canonical order, or an empty list if none match.

    Notes
    -----
    Names and source descriptions ignore case, accents, spaces, and punctuation
    for exact matching. General text search uses the catalog's case-insensitive
    substring search. The first lookup downloads the snapshot if no local
    index exists. An existing index is read locally without a network request.
    """
    name = _nonempty(name, "name")
    if source is not None:
        source = _nonempty(source, "source")
    resolved_catalog = _get_catalog(catalog, data_root)
    try:
        pages = _candidates(name, resolved_catalog)
    except KeyError:
        return []
    return _select_source(pages, source) if source is not None else pages


def load_material(
    name: str,
    *,
    source: str | None = None,
    catalog: MaterialCatalog | None = None,
    data_root: Path | str | None = None,
    interpolation: str = "linear",
    use_default: bool = True,
):
    """Load a material by name with documented defaults and source overrides.

    This is also available as ``from PyOptik import material; material(...)``.
    Common names use documented canonical defaults unless source is supplied
    or use_default is False. Other ambiguous queries raise an error listing
    sources and canonical IDs. Ordering and cache availability never select
    a dataset.

    Parameters
    ----------
    name : str
        Common name, chemical formula, glass name, or canonical page ID.
    source : str, optional
        Exact page ID or source-description text. Use the exact ID when
        a source publishes several datasets or measurement conditions.
    catalog : MaterialCatalog, optional
        Existing catalog for custom data or offline operation.
    data_root : pathlib.Path or str, optional
        Snapshot directory. Cannot be combined with catalog.
    interpolation : {"linear", "pchip"}, optional
        Interpolation for tabulated data; ignored for formula models.
    use_default : bool, optional
        Use the documented source for a known family alias (default True).
        Set False to require a source whenever several datasets match.

    Returns
    -------
    SellmeierMaterial or TabulatedMaterial
        Loaded model, retaining canonical ID and scientific provenance.

    Raises
    ------
    AmbiguousMaterialError
        More than one dataset matches and no documented default applies, or
        use_default is False. Inspect candidates or use find_materials.
    ValueError
        Empty name or source, or conflicting catalog/data_root arguments.
    TypeError
        Name or source is not a string, or use_default is not a bool.
    KeyError
        No material or source matches; includes spelling suggestions when possible.
    FileNotFoundError
        The chosen page has no local data. Run pyoptik setup to repair the cache.

    Notes
    -----
    Defaults are main/SiO2/Malitson for silica, main/Au/Johnson for gold,
    main/Ag/Johnson for silver, and main/H2O/Hale for water. BK7 and N-BK7
    refer explicitly to specs/SCHOTT-optical/N-BK7. Loaded models expose
    catalog_id and provenance. A missing default never falls back to another
    dataset. See the materials-and-catalog guide for the full source table.

    Examples
    --------
    >>> from PyOptik import material
    >>> gold = material("gold", source="Johnson")  # doctest: +SKIP
    >>> gold.catalog_id  # doctest: +SKIP
    'main/Au/Johnson'
    """
    name = _nonempty(name, "name")
    if source is not None:
        source = _nonempty(source, "source")
    if not isinstance(use_default, bool):
        raise TypeError("use_default must be a bool.")
    resolved_catalog = _get_catalog(catalog, data_root)
    default = _DEFAULT_SOURCES.get(_BOOK_ALIASES.get(_normalize(name)))
    if source is None and use_default and default is not None:
        try:
            selected = resolved_catalog.get(default)
        except KeyError as error:
            raise KeyError(
                f"Documented default {default!r} for {name!r} is absent from this catalog. "
                "Use find_materials(name) and select an explicit source."
            ) from error
        return selected.load(interpolation=interpolation)
    pages = find_materials(name, catalog=resolved_catalog)
    if not pages:
        known_names = sorted(set(_BOOK_ALIASES) | set(_PAGE_ALIASES) |
                             {page.id.book for page in resolved_catalog.pages()})
        suggestions = get_close_matches(_normalize(name), known_names, n=3, cutoff=0.6)
        hint = f" Did you mean {', '.join(repr(item) for item in suggestions)}?" if suggestions else ""
        raise KeyError(f"No material found for {name!r}.{hint} Use find_materials(name) to search the catalog.")
    if source is not None:
        selected = _select_source(pages, source)
        if not selected:
            available = ", ".join(page.id.key for page in pages)
            raise KeyError(f"No source {source!r} found for {name!r}. Available datasets: {available}")
        pages = selected
    if len(pages) > 1:
        raise AmbiguousMaterialError(name, pages)
    return pages[0].load(interpolation=interpolation)
