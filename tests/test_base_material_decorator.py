import numpy
import pytest
from PyOptik.material.base_class import BaseMaterial
from PyOptik.units import meter, Quantity


class Dummy(BaseMaterial):
    def __init__(self):
        self.filename = 'dummy'
        self.wavelength_bound = numpy.array([1.0, 2.0]) * meter

    @BaseMaterial.ensure_units
    def identity(self, wavelength: Quantity) -> Quantity:
        return wavelength

def test_ensure_units_numeric():
    dummy = Dummy()
    out = dummy.identity(1.5)
    assert isinstance(out, Quantity)
    assert out.units == meter


def test_ensure_units_quantity():
    dummy = Dummy()
    wl = 1.6 * meter
    out = dummy.identity(wl)
    assert out == wl


def test_ensure_units_default():
    dummy = Dummy()
    out = dummy.identity()
    assert len(out) == 100
    assert out.units == meter


if __name__ == "__main__":
    pytest.main(["-W error", "-s", __file__])
