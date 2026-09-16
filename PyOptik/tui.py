"""Optional Textual terminal interface for browsing the material catalog."""

from __future__ import annotations

from pathlib import Path

from PyOptik.catalog import MaterialCatalog, MaterialPage


def run_browser(data_root: Path | str | None = None) -> None:
    """Open the local material catalog in an interactive terminal browser."""
    root = Path(data_root).expanduser() if data_root is not None else None
    if root is None:
        from PyOptik.directories import user_data_path
        root = user_data_path / "rii"
    catalog_file = root / "catalog-nk.yml"
    if not catalog_file.exists():
        raise FileNotFoundError(
            f"No local catalog found at {catalog_file}. Run 'pyoptik setup' first."
        )
    try:
        from textual.app import App, ComposeResult
        from textual.containers import Horizontal, Vertical
        from textual.widgets import DataTable, Footer, Header, Input, Static
    except ImportError as error:
        raise RuntimeError(
            "The catalog browser requires the optional UI dependency. "
            "Install it with 'python -m pip install PyOptik[ui]'."
        ) from error
    catalog = MaterialCatalog(catalog_file=catalog_file, data_root=root)

    class CatalogBrowser(App):
        """Full-screen searchable browser for one local catalog."""

        TITLE = "PyOptik Material Catalog"
        CSS = """
        #body { height: 1fr; }
        #left { width: 2fr; }
        #details { width: 1fr; padding: 1 2; border-left: solid $accent; }
        #search { margin: 0 1; }
        DataTable { height: 1fr; }
        """
        BINDINGS = [("q", "quit", "Quit"), ("/", "focus_search", "Search")]

        def __init__(self, material_catalog: MaterialCatalog):
            """Store the catalog displayed by the application."""
            super().__init__()
            self.material_catalog = material_catalog
            self.visible_pages: dict[str, MaterialPage] = {}

        def compose(self) -> ComposeResult:
            """Create the search, result table, and provenance pane."""
            yield Header()
            with Horizontal(id="body"):
                with Vertical(id="left"):
                    yield Input(placeholder="Search ID, name, description, or source…", id="search")
                    yield DataTable(id="materials", cursor_type="row", zebra_stripes=True)
                yield Static("Select a material to inspect it.", id="details")
            yield Footer()

        def on_mount(self) -> None:
            """Initialize table columns and catalog rows."""
            table = self.query_one("#materials", DataTable)
            table.add_columns("ID", "Description", "Cached")
            self._populate("")
            self.query_one("#search", Input).focus()

        def _populate(self, query: str) -> None:
            """Replace table contents with pages matching ``query``."""
            table = self.query_one("#materials", DataTable)
            table.clear()
            self.visible_pages.clear()
            for page in self.material_catalog.search(query):
                key = page.id.key
                self.visible_pages[key] = page
                table.add_row(key, page.description or page.name, "yes" if page.available else "no", key=key)

        def on_input_changed(self, event: Input.Changed) -> None:
            """Filter results as the search value changes."""
            if event.input.id == "search":
                self._populate(event.value)

        def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
            """Show identity, source, reference, and availability for a row."""
            page = self.visible_pages.get(str(event.row_key.value))
            if page is None:
                return
            provenance = page.provenance()
            lines = [
                f"[b]{provenance['id']}[/b]", "",
                provenance["description"] or provenance["name"], "",
                f"Cached: {'yes' if provenance['available'] else 'no'}",
                f"Path: {provenance['local_path'] or '—'}",
                f"Source: {provenance['source_url'] or '—'}", "",
                f"Reference: {provenance['reference'] or '—'}",
            ]
            self.query_one("#details", Static).update("\n".join(lines))

        def action_focus_search(self) -> None:
            """Focus and select the search field."""
            search = self.query_one("#search", Input)
            search.focus()
            search.action_select_all()

    CatalogBrowser(catalog).run()
