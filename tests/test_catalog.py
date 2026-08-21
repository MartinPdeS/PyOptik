import io
import zipfile

import yaml

import pytest

from PyOptik import MaterialCatalog, MaterialId, download_snapshot


def test_catalog_reads_upstream_hierarchy(tmp_path):
    catalog_file = tmp_path / "catalog-nk.yml"
    catalog_file.write_text(
        yaml.safe_dump([
            {
                "SHELF": "specs",
                "name": "Specifications",
                "content": [{
                    "BOOK": "SCHOTT-optical",
                    "content": [{
                        "PAGE": "N-BK7",
                        "name": "SCHOTT N-BK7",
                        "data": "specs/schott/optical/N-BK7.yml",
                    }],
                }],
            }
        ])
    )
    catalog = MaterialCatalog(catalog_file=catalog_file, data_root=tmp_path / "rii")

    page = catalog.get(MaterialId("specs", "SCHOTT-optical", "N-BK7"))
    assert page.id.key == "specs/SCHOTT-optical/N-BK7"
    assert page.local_path == tmp_path / "rii/specs/schott/optical/N-BK7.yml"
    assert page.source_url.endswith("/specs/schott/optical/N-BK7.yml")
    assert catalog.shelves() == ["specs"]
    assert catalog.books("specs") == ["SCHOTT-optical"]
    matches = catalog.search("bk7", source="refractiveindex.info", available=False)
    assert [item.id.key for item in matches] == ["specs/SCHOTT-optical/N-BK7"]
    assert matches[0].provenance()["available"] is False


def test_catalog_loads_local_page(tmp_path):
    data_root = tmp_path / "rii"
    data_file = data_root / "main/Si/nk/Test.yml"
    data_file.parent.mkdir(parents=True)
    data_file.write_text(
        "REFERENCES: Example et al. 2024\n"
        "DATA:\n  - type: tabulated nk\n    data: |\n      0.4 1.5 0.1\n      0.5 1.6 0.2\n"
    )
    catalog_file = tmp_path / "catalog.yml"
    catalog_file.write_text(
        "- SHELF: main\n  content:\n    - BOOK: Si\n      content:\n        - PAGE: Test\n          data: main/Si/nk/Test.yml\n"
    )
    page = MaterialCatalog(catalog_file, data_root).get("main/Si/Test")
    material = page.load()
    assert material.filename == "Test"
    assert material.compute_refractive_index(450e-9).imag > 0
    assert page.reference == "Example et al. 2024"
    catalog = MaterialCatalog(catalog_file, data_root)
    assert [item.id.key for item in catalog.search(reference="2024")] == ["main/Si/Test"]


def test_missing_page_explains_snapshot_setup(tmp_path):
    catalog_file = tmp_path / "catalog.yml"
    catalog_file.write_text(
        "- SHELF: main\n  content:\n    - BOOK: Ag\n      content:\n        - PAGE: Johnson\n          data: main/Ag/nk/Johnson.yml\n"
    )
    page = MaterialCatalog(catalog_file, tmp_path / "rii").get("main/Ag/Johnson")

    with pytest.raises(FileNotFoundError, match="download_snapshot.*pyoptik setup"):
        page.load()


def test_download_snapshot_wrapper(monkeypatch, tmp_path):
    expected = object()

    def fake_snapshot(**kwargs):
        assert kwargs == {"data_root": tmp_path, "force": True, "progress": None}
        return expected

    monkeypatch.setattr(MaterialCatalog, "from_snapshot", fake_snapshot)
    assert download_snapshot(tmp_path, force=True) is expected


def test_catalog_from_upstream_uses_local_cache(monkeypatch, tmp_path):
    def fake_download(**kwargs):
        destination = kwargs["destination"]
        destination.parent.mkdir(parents=True)
        destination.write_text(
            "- SHELF: main\n  content:\n    - BOOK: Si\n      content:\n        - PAGE: Test\n          data: main/Si/nk/Test.yml\n"
        )

    monkeypatch.setattr("PyOptik.catalog.download_yml_file", fake_download)
    catalog = MaterialCatalog.from_upstream(data_root=tmp_path / "rii")
    assert catalog.shelves() == ["main"]


def test_catalog_from_snapshot_extracts_database(monkeypatch, tmp_path):
    archive = io.BytesIO()
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr(
            "database-main/database/catalog-nk.yml",
            "- SHELF: main\n  content:\n    - BOOK: Si\n      content:\n        - PAGE: Test\n          data: main/Si/nk/Test.yml\n",
        )
        bundle.writestr("database-main/database/data/main/Si/nk/Test.yml", "DATA: []\n")

    class Response:
        content = archive.getvalue()

        @staticmethod
        def raise_for_status():
            return None

    monkeypatch.setattr("PyOptik.catalog.requests.get", lambda *args, **kwargs: Response())
    root = tmp_path / "rii"
    catalog = MaterialCatalog.from_snapshot(data_root=root)

    assert catalog.shelves() == ["main"]
    assert (root / "main/Si/nk/Test.yml").read_text() == "DATA: []\n"
    manifest = yaml.safe_load((root / "manifest.json").read_text())
    assert manifest["catalog"]["mode"] == "snapshot"
    assert manifest["pages"]["main/Si/Test"]["status"] == "snapshot"
    assert all(catalog.verify_integrity().values())
    (root / "main/Si/nk/Test.yml").write_text("altered\n")
    assert catalog.verify_integrity()[MaterialId("main", "Si", "Test")] is False


def test_download_all_writes_resumable_manifest(monkeypatch, tmp_path):
    catalog_file = tmp_path / "catalog.yml"
    catalog_file.write_text(
        "- SHELF: main\n  content:\n    - BOOK: Si\n      content:\n        - PAGE: Test\n          data: main/Si/nk/Test.yml\n"
    )
    root = tmp_path / "rii"

    def fake_download(**kwargs):
        destination = kwargs["destination"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("DATA: []\n")

    monkeypatch.setattr("PyOptik.catalog.download_yml_file", fake_download)
    progress = []
    catalog = MaterialCatalog(catalog_file, root)
    catalog.download_all(progress=lambda *args: progress.append(args))

    manifest = yaml.safe_load((root / "manifest.json").read_text())
    assert manifest["pages"]["main/Si/Test"]["status"] == "downloaded"
    assert len(progress) == 1
    assert progress[0][3] == "downloaded"

    catalog.download_all(progress=lambda *args: progress.append(args))
    assert progress[-1][3] == "cached"
    assert catalog.verify_integrity()[MaterialId("main", "Si", "Test")] is True
