import numpy as np
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
    material = _catalog(tmp_path).get("specs/Example/Glass").load()
    wavelength = 0.8 * ureg.micrometer
    assert float(material.compute_refractive_index(wavelength)) > 1
    assert float(material.compute_group_index(wavelength)) > 0
    assert material.compute_group_delay(wavelength, length=1 * ureg.meter).magnitude > 0


def test_canonical_tabulated_material_and_group_properties(tmp_path):
    material = _catalog(tmp_path).get("main/Example/Metal").load()
    wavelengths = np.linspace(0.5, 1.0, 3) * ureg.micrometer
    index = material.compute_refractive_index(wavelengths)
    assert index.shape == wavelengths.shape
    assert np.all(np.isfinite(material.compute_group_index(wavelengths).magnitude))
