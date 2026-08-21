import numpy as np
import pytest
from TypedUnit import ureg

from PyOptik import MaterialCatalog


def _catalog(tmp_path):
    root = tmp_path / "data"
    sellmeier = root / "specs/Example/Glass.yml"
    tabulated = root / "main/Example/nk/Metal.yml"
    sellmeier.parent.mkdir(parents=True)
    tabulated.parent.mkdir(parents=True)
    sellmeier.write_text(
        "DATA:\n"
        "  - type: formula 2\n"
        "    coefficients: 1.0 0.01 0.5 0.1\n"
        "    wavelength_range: 0.2 2.0\n"
    )
    tabulated.write_text(
        "DATA:\n"
        "  - type: tabulated nk\n"
        "    data: |\n"
        "      0.4 1.5 0.1\n"
        "      0.8 1.6 0.2\n"
        "      1.2 1.7 0.3\n"
    )
    catalog_file = tmp_path / "catalog.yml"
    catalog_file.write_text(
        "- SHELF: specs\n"
        "  content:\n"
        "    - BOOK: Example\n"
        "      content:\n"
        "        - PAGE: Glass\n"
        "          data: specs/Example/Glass.yml\n"
        "- SHELF: main\n"
        "  content:\n"
        "    - BOOK: Example\n"
        "      content:\n"
        "        - PAGE: Metal\n"
        "          data: main/Example/nk/Metal.yml\n"
    )
    return MaterialCatalog(catalog_file, root)


def test_canonical_formula_material_and_group_properties(tmp_path):
    catalog = _catalog(tmp_path)
    page = catalog.get("specs/Example/Glass")
    material = page.load()
    assert repr(catalog).startswith("MaterialCatalog(pages=2, data_root=")
    assert repr(page) == "MaterialPage(id='specs/Example/Glass', name='Glass', data='available')"
    assert repr(material).startswith("SellmeierMaterial(filename='Glass'")
    wavelength = 0.8 * ureg.micrometer
    assert float(material.compute_refractive_index(wavelength)) > 1
    assert float(material.compute_group_index(wavelength)) > 0
    assert material.compute_group_delay(wavelength, length=1 * ureg.meter).magnitude > 0
    assert material.compute_group_delay_wavelength_slope(wavelength).magnitude != 0
    assert material.compute_group_delay_dispersion(wavelength).to(ureg.second ** 2).magnitude != 0


def test_canonical_tabulated_material_and_group_properties(tmp_path):
    material = _catalog(tmp_path).get("main/Example/Metal").load()
    assert repr(material).startswith("TabulatedMaterial(filename='Metal'")
    wavelengths = np.linspace(0.5, 1.0, 3) * ureg.micrometer
    index = material.compute_refractive_index(wavelengths)
    assert index.shape == wavelengths.shape
    assert np.all(np.isfinite(material.compute_group_index(wavelengths).magnitude))


def test_formula_six_accumulates_all_gas_terms(tmp_path):
    data_file = tmp_path / "gas.yml"
    data_file.write_text(
        "DATA:\n"
        "  - type: formula 6\n"
        "    coefficients: 0.01 0.1 4.0 0.2 5.0\n"
        "    wavelength_range: 0.2 2.0\n"
    )
    from PyOptik.material import SellmeierMaterial

    material = SellmeierMaterial("gas", file_path=data_file)
    wavelength_um = 0.6
    expected = 1.01 + 0.1 / (4.0 - wavelength_um ** -2) + 0.2 / (5.0 - wavelength_um ** -2)
    assert material.compute_refractive_index(wavelength_um * ureg.micrometer) == pytest.approx(expected)


@pytest.mark.parametrize("formula_type, coefficients, expected", [
    (1, "0.1 0.2 0.3", np.sqrt(1.1 + 0.2 * 0.5**2 / (0.5**2 - 0.3**2))),
    (2, "0.1 0.2 0.3", np.sqrt(1.1 + 0.2 * 0.5**2 / (0.5**2 - 0.3))),
    (3, "1.1 0.2 2", np.sqrt(1.1 + 0.2 * 0.5**2)),
    (4, "1.1 0.2 2 0.3 2", np.sqrt(1.1 + 0.2 * 0.5**2 / (0.5**2 - 0.3**2))),
    (5, "1.1 0.2 2", 1.1 + 0.2 * 0.5**2),
    (6, "0.1 0.2 5", 1.1 + 0.2 / (5 - 0.5**-2)),
    (7, "1.1 0.2 0.3 0.4", 1.1 + 0.2 / (0.5**2 - 0.028) + 0.3 / (0.5**2 - 0.028)**2 + 0.4 * 0.5**2),
    (8, "0.1 0.2 0.1 0.04", np.sqrt((2 * (0.1 + 0.2 * 0.5**2 / (0.5**2 - 0.1) + 0.04 * 0.5**2) + 1) / (1 - (0.1 + 0.2 * 0.5**2 / (0.5**2 - 0.1) + 0.04 * 0.5**2)))),
    (9, "1.1 0.2 0.1 0.04 0.1 0.2", np.sqrt(1.1 + 0.2 / (0.5**2 - 0.1) + 0.04 * (0.5 - 0.1) / ((0.5 - 0.1)**2 + 0.2))),
])
def test_all_upstream_formula_types_match_reference_equations(tmp_path, formula_type, coefficients, expected):
    data_file = tmp_path / f"formula-{formula_type}.yml"
    data_file.write_text(
        f"DATA:\n  - type: formula {formula_type}\n    coefficients: {coefficients}\n    wavelength_range: 0.2 2.0\n"
    )
    from PyOptik.material import SellmeierMaterial

    material = SellmeierMaterial(str(data_file.stem), file_path=data_file)
    assert material.compute_refractive_index(500 * ureg.nanometer) == pytest.approx(expected)


def test_wavelength_units_are_equivalent_for_formula_and_tabulated_materials(tmp_path):
    catalog = _catalog(tmp_path)
    for identifier in ("specs/Example/Glass", "main/Example/Metal"):
        material = catalog.get(identifier).load()
        assert material.compute_refractive_index(800 * ureg.nanometer) == pytest.approx(
            material.compute_refractive_index(0.8 * ureg.micrometer)
        )
