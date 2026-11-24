import pytest
from PyOptik.material.tabulated_class import TabulatedMaterial


def test_tabulated_data_rejects_unsorted_wavelengths(monkeypatch, tmp_path):
    directory = tmp_path / "tabulated"
    directory.mkdir()
    (directory / "invalid.yml").write_text(
        "DATA:\n  - type: tabulated nk\n    data: |\n      2.0 1.5 0.0\n      1.0 1.5 0.0\n"
    )
    monkeypatch.setattr(
        "PyOptik.material.tabulated_class.material_paths",
        lambda material_type: (directory,),
    )
    with pytest.raises(ValueError, match="Invalid or missing data"):
        TabulatedMaterial("invalid")
