import numpy as np
import pytest
from PyOptik import MaterialBank
from PyOptik.units import micrometer, meter, ureg


def test_group_index_sellmeier():
    bk7 = MaterialBank.BK7
    gi = bk7.compute_group_index(0.8 * micrometer)
    assert gi.magnitude > 0.0


def test_group_velocity_tabulated():
    si = MaterialBank.silicon
    gv = si.compute_group_velocity(0.6 * micrometer)
    c = 299792458 * meter / ureg.second
    assert gv < c


def test_group_index_array():
    water = MaterialBank.water
    wavelengths = np.linspace(0.5, 0.6, 3) * micrometer
    gi = water.compute_group_index(wavelengths)
    assert gi.shape == wavelengths.shape


def test_group_delay():
    bk7 = MaterialBank.BK7
    gd = bk7.compute_group_delay(0.8 * micrometer, length=1 * meter)
    assert gd.magnitude > 0.0


def test_group_delay_dispersion():
    si = MaterialBank.silicon
    gdd = si.compute_group_delay_dispersion(0.6 * micrometer)
    assert np.isfinite(gdd.magnitude)


if __name__ == "__main__":
    pytest.main(["-W error", "-s", __file__])
