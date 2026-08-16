import logging

import numpy as np
import pytest
from TypedUnit import ureg

from PyOptik import MaterialBank
from PyOptik.material.tabulated_class import TabulatedMaterial


def test_material_cache_and_explicit_kind():
    first = MaterialBank.get("BK7", kind="sellmeier")
    second = MaterialBank.get("BK7", kind="sellmeier")
    assert first is second


def test_range_modes(caplog):
    material = MaterialBank.get("BK7", kind="sellmeier")
    outside = 100 * ureg.nanometer

    with pytest.raises(ValueError):
        material.compute_refractive_index(outside, out_of_range="raise")

    with caplog.at_level(logging.DEBUG, logger="PyOptik.material.base_class"):
        clipped = material.compute_refractive_index(outside, out_of_range="clip")
    edge = material.compute_refractive_index(material.wavelength_bound[0])
    assert np.isclose(clipped, edge)
    assert "Clipping out-of-range wavelengths" in caplog.text


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
