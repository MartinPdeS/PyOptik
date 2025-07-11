import pytest
import numpy as np

from PyOptik.material.base_class import BaseMaterial
from PyOptik.units import micrometer, meter, Quantity


class DummyMaterial(BaseMaterial):
    def __init__(self, bounds=None):
        self.filename = "dummy"
        self.wavelength_bound = bounds

    @BaseMaterial.ensure_units
    def echo(self, wavelength: Quantity = None) -> Quantity:
        return wavelength


def test_ensure_units_provides_default_range():
    bounds = np.array([0.4, 0.7]) * micrometer
    mat = DummyMaterial(bounds=bounds)

    result = mat.echo()

    assert isinstance(result, Quantity)
    assert len(result) == 100
    assert np.isclose(result.magnitude[0], 0.4)
    assert np.isclose(result.magnitude[-1], 0.7)
    assert result.units == micrometer


def test_ensure_units_converts_float():
    bounds = np.array([0.4, 0.7]) * micrometer
    mat = DummyMaterial(bounds=bounds)

    result = mat.echo(0.5)

    assert isinstance(result, Quantity)
    assert np.isclose(result.magnitude, 0.5)
    assert result.units == meter  # ensure_units converts to meters


def test_ensure_units_no_bounds_error():
    mat = DummyMaterial(bounds=None)

    with pytest.raises(ValueError, match="Wavelength must be provided"):
        mat.echo(None)

