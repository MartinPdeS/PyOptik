import pytest

from PyOptik import MaterialBank
from PyOptik.material_type import MaterialType

def test_set_filter_invalid():
    with pytest.raises(ValueError):
        MaterialBank.set_filter(use_tabulated=False, use_sellmeier=False)
    # restore default
    MaterialBank.set_filter(use_tabulated=True, use_sellmeier=True)


def test_list_materials(monkeypatch, tmp_path):
    tmp_sell = tmp_path / "sellmeier"
    tmp_tab = tmp_path / "tabulated"
    tmp_sell.mkdir()
    tmp_tab.mkdir()
    (tmp_sell / "mat1.yml").write_text("test")
    (tmp_tab / "mat2.yml").write_text("test")

    with monkeypatch.context() as m:
        m.setattr("PyOptik.material_bank.data_path", tmp_path)
        sell_list = MaterialBank._list_materials(MaterialType.SELLMEIER)
        tab_list = MaterialBank._list_materials(MaterialType.TABULATED)

    assert sell_list == ["mat1"]
    assert tab_list == ["mat2"]


def test_search_materials(monkeypatch, tmp_path):
    tmp_sell = tmp_path / "sellmeier"
    tmp_tab = tmp_path / "tabulated"
    tmp_sell.mkdir()
    tmp_tab.mkdir()
    (tmp_sell / "BK7.yml").write_text("test")
    (tmp_tab / "gold.yml").write_text("test")

    with monkeypatch.context() as m:
        m.setattr("PyOptik.material_bank.data_path", tmp_path)
        found_sell = MaterialBank.search("bk")
        found_tab = MaterialBank.search("gold", material_type=MaterialType.TABULATED)

    assert "BK7" in found_sell
    assert found_tab == ["gold"]

if __name__ == "__main__":
    pytest.main(["-W error", "-s", __file__])
