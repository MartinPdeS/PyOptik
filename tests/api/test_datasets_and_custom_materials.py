"""Tests for typed datasets and user-authored materials."""

import numpy as np
import pytest
import yaml
from TypedUnit import ureg

from PyOptik import (
    FormulaDataset,
    MaterialDocument,
    SellmeierMaterial,
    TabulatedMaterial,
    parse_material,
)


def test_typed_parser_preserves_metadata_and_dataset_types(tmp_path):
    path = tmp_path / "glass.yml"
    path.write_text(
        "REFERENCES: Test source\nCOMMENTS: Dry sample\n"
        "CONDITIONS:\n  temperature: 293 K\n"
        "DATA:\n  - type: formula 1\n    coefficients: 0.1 0.2 0.3\n"
        "    wavelength_range: 0.4 1.0\n"
    )
    document = parse_material(path)
    assert document.formula_datasets == (FormulaDataset(1, (0.1, 0.2, 0.3), (0.4, 1.0)),)
    assert document.metadata.conditions == {"temperature": "293 K"}


@pytest.mark.parametrize("document, message", [
    ({"DATA": "not a list"}, "DATA must be a list"),
    ({"DATA": []}, "no supported dataset"),
    ({"DATA": [{"type": "formula 10", "coefficients": "1"}]}, "Unsupported formula"),
    ({"DATA": [{"type": "tabulated n", "data": "0.5 1\n0.4 2"}]}, "strictly increasing"),
    ({"DATA": [{"type": "tabulated nk", "data": "0.4 1\n0.5 2"}]}, "require 3 columns"),
    ({"CONDITIONS": [1], "DATA": [{"type": "formula 5", "coefficients": "1"}]}, "metadata"),
])
def test_parser_failure_messages(document, message):
    with pytest.raises(ValueError, match=message):
        parse_material(document)


def test_custom_tabulated_material_round_trip_and_boundaries(tmp_path):
    material = TabulatedMaterial.from_arrays(
        "custom",
        np.array([400, 500, 600]) * ureg.nanometer,
        n=[1.4, 1.5, 1.6],
        k=[0.01, 0.02, 0.04],
        reference="Lab data",
        conditions={"temperature": "20 C"},
    )
    path = material.to_yaml(tmp_path / "custom.yml")
    restored = TabulatedMaterial("custom", file_path=path)
    query = np.array([400, 450, 600]) * ureg.nanometer
    assert restored.compute_refractive_index(query) == pytest.approx(
        material.compute_refractive_index(query)
    )
    assert restored.reference == "Lab data"
    assert yaml.safe_load(path.read_text())["DATA"][0]["type"] == "tabulated nk"


def test_custom_tabulated_validation_and_range_policy():
    with pytest.raises(ValueError, match="at least one"):
        TabulatedMaterial.from_arrays("bad", [0.4, 0.5])
    with pytest.raises(ValueError, match="match wavelength"):
        TabulatedMaterial.from_arrays("bad", [0.4, 0.5], n=[1.0])
    with pytest.raises(ValueError, match="one-dimensional"):
        TabulatedMaterial.from_arrays("bad", 0.5, n=1.0)
    with pytest.raises(ValueError, match="strictly increasing"):
        TabulatedMaterial.from_arrays("bad", [0.5, 0.4], n=[1.0, 1.1])
    material = TabulatedMaterial.from_arrays("ok", [0.4, 0.5], n=[1.4, 1.5])
    with pytest.raises(ValueError, match="outside the allowable range"):
        material.compute_refractive_index(0.6 * ureg.micrometer, out_of_range="raise")
    assert material.compute_refractive_index(
        0.6 * ureg.micrometer, out_of_range="clip"
    ).real == pytest.approx(1.5)


def test_custom_formula_round_trip(tmp_path):
    material = SellmeierMaterial.from_coefficients(
        "custom-glass",
        [0.1, 0.2, 0.3],
        formula_type=1,
        wavelength_range=[400, 900] * ureg.nanometer,
        comments="Fitted sample",
    )
    path = material.to_yaml(tmp_path / "formula.yml")
    restored = SellmeierMaterial("formula", file_path=path)
    assert restored.compute_refractive_index(500 * ureg.nanometer) == pytest.approx(
        material.compute_refractive_index(500 * ureg.nanometer)
    )
    assert restored.comments == "Fitted sample"


def test_csv_constructor_with_unit_conversion(tmp_path):
    path = tmp_path / "measured.csv"
    path.write_text("wavelength,n,k\n400,1.4,0.01\n500,1.5,0.02\n")
    material = TabulatedMaterial.from_csv(path, wavelength_unit=ureg.nanometer)
    assert material.compute_refractive_index(450 * ureg.nanometer) == pytest.approx(1.45 + 0.015j)


def test_document_export_is_atomic_on_success(tmp_path):
    document = MaterialDocument((FormulaDataset(5, (1.0, 0.2, 2.0), None),))
    destination = document.to_yaml(tmp_path / "nested" / "material.yml")
    assert destination.exists()
    assert not destination.with_suffix(".yml.tmp").exists()
