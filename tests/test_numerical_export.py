"""Numerical export and dataset validation, independent of any consumer."""

import numpy as np
import pytest
from TypedUnit import ureg

from PyOptik import FormulaDataset, TabulatedMaterial


@pytest.mark.parametrize("component", ["n", "k", "nk"])
def test_export_single_grid_defaults_units_and_independent_arrays(component):
    kwargs = {}
    if "n" in component:
        kwargs["n"] = [1.4, 1.5, 1.7]
    if "k" in component:
        kwargs["k"] = [-0.1, 0.0, 0.2]
    material = TabulatedMaterial.from_arrays("sample", [400, 500, 600] * ureg.nanometer, **kwargs)
    wavelength, n, k = material.to_arrays(allow_gain=True)
    assert wavelength.to(ureg.nanometer).magnitude == pytest.approx([400, 500, 600])
    assert n == pytest.approx(kwargs.get("n", [1, 1, 1]))
    assert k == pytest.approx(kwargs.get("k", [0, 0, 0]))
    wavelength.magnitude[:] = 0
    n[:] = 0
    k[:] = 0
    assert material.compute_refractive_index(450 * ureg.nanometer, allow_gain=True).real == pytest.approx(1.45 if "n" in component else 1)


def test_export_separate_grids_preserves_linear_curves(tmp_path):
    path = tmp_path / "separate.yml"
    path.write_text("DATA:\n- type: tabulated n\n  data: |\n    0.4 1.4\n    0.5 1.8\n    0.7 1.9\n- type: tabulated k\n  data: |\n    0.45 0.1\n    0.55 0.4\n    0.6 0.2\n")
    material = TabulatedMaterial("separate", file_path=path)
    wavelength, n, k = material.to_arrays(allow_gain=True)
    assert wavelength.magnitude == pytest.approx([0.45, 0.5, 0.55, 0.6])
    query = np.linspace(0.45, 0.6, 101)
    restored = np.interp(query, wavelength.magnitude, n) + 1j * np.interp(query, wavelength.magnitude, k)
    assert restored == pytest.approx(material.compute_refractive_index(query * ureg.micrometer, out_of_range="raise"))


@pytest.mark.parametrize("cells", [("", "0.1"), ("0.1", ""), (" ", "0.1"), ("", "")])
def test_csv_missing_extinction_requires_explicit_fill(tmp_path, cells):
    path = tmp_path / "sample.csv"
    path.write_text(f"wavelength,n,k\n0.4,1.4,{cells[0]}\n0.5,1.5,{cells[1]}\n")
    with pytest.raises(ValueError, match="Missing 'k'.*CSV line"):
        TabulatedMaterial.from_csv(path)
    material = TabulatedMaterial.from_csv(path, missing_k=0.0)
    assert material.to_arrays()[2] == pytest.approx([float(value) if value.strip() else 0 for value in cells])


@pytest.mark.parametrize("row", ["0.4,,0.1", "0.4, ,0.1"])
def test_csv_missing_real_index_is_never_silently_discarded(tmp_path, row):
    path = tmp_path / "sample.csv"
    path.write_text(f"wavelength,n,k\n{row}\n0.5,1.5,0.2\n")
    with pytest.raises(ValueError, match="Missing 'n'.*line 2"):
        TabulatedMaterial.from_csv(path, missing_k=0)


@pytest.mark.parametrize("start", [-1.0, 0.0])
def test_dataset_wavelengths_and_formula_bounds_must_be_positive(start):
    with pytest.raises(ValueError, match="positive"):
        TabulatedMaterial.from_arrays("bad", [start, 1], n=[1.4, 1.5])
    with pytest.raises(ValueError, match="positive"):
        FormulaDataset(5, (1.4,), (start, 1.0))


def test_negative_optical_constants_remain_valid():
    material = TabulatedMaterial.from_arrays("active", [0.4, 0.5], n=[-1, -2], k=[-0.1, -0.2])
    assert material.compute_refractive_index(0.45 * ureg.micrometer, allow_negative_index=True, allow_gain=True) == pytest.approx(-1.5 - 0.15j)


@pytest.mark.parametrize("column, expected", [("n", 1.45 + 0j), ("k", 1 + 0.15j)])
def test_csv_absent_component_columns_keep_evaluation_defaults(tmp_path, column, expected):
    path = tmp_path / "sample.csv"
    values = [1.4, 1.5] if column == "n" else [0.1, 0.2]
    path.write_text(f"wavelength,{column}\n0.4,{values[0]}\n0.5,{values[1]}\n")
    material = TabulatedMaterial.from_csv(path)
    assert material.compute_refractive_index(0.45 * ureg.micrometer) == pytest.approx(expected)


@pytest.mark.parametrize("fill", [np.nan, np.inf, -np.inf])
def test_csv_missing_extinction_fill_must_be_finite(tmp_path, fill):
    path = tmp_path / "sample.csv"
    path.write_text("wavelength,n,k\n0.4,1.4,\n0.5,1.5,0.2\n")
    with pytest.raises(ValueError, match="missing_k must be finite"):
        TabulatedMaterial.from_csv(path, missing_k=fill)


def test_pchip_export_keeps_interpolation_policy():
    pytest.importorskip("scipy")
    material = TabulatedMaterial.from_arrays(
        "curved", [0.4, 0.5, 0.6], n=[1.4, 1.5, 1.9], interpolation="pchip",
    )
    wavelength, n, k = material.to_arrays(allow_gain=True)
    assert material.interpolation == "pchip"
    assert n + 1j * k == pytest.approx(material.compute_refractive_index(wavelength))
    assert material.compute_refractive_index(0.45 * ureg.micrometer).real != pytest.approx(1.45)
