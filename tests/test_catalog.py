import yaml

from PyOptik import MaterialCatalog, MaterialId


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


def test_catalog_loads_local_page(tmp_path):
    data_root = tmp_path / "rii"
    data_file = data_root / "main/Si/nk/Test.yml"
    data_file.parent.mkdir(parents=True)
    data_file.write_text(
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
