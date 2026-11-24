"""Reference and validation tests for interface and thin-film optics."""

import numpy as np
import pytest
from TypedUnit import ureg

from PyOptik import (
    TabulatedMaterial,
    ThinFilmLayer,
    brewster_angle,
    critical_angle,
    fresnel_coefficients,
    thin_film_stack,
)


@pytest.mark.parametrize("polarization", ["s", "p"])
def test_air_glass_interface_at_normal_incidence(polarization):
    """Air-to-glass power coefficients match the analytic 4% result."""
    result = fresnel_coefficients(1.0, 1.5, polarization=polarization)
    assert result.reflectance == pytest.approx(0.04)
    assert result.transmittance == pytest.approx(0.96)
    assert result.absorptance == pytest.approx(0.0, abs=1e-15)
    assert result.transmitted_angle.to(ureg.degree).magnitude == pytest.approx(0.0)


def test_brewster_and_critical_angles():
    """Characteristic interface angles agree with their closed forms."""
    brewster = brewster_angle(1.0, 1.5)
    result = fresnel_coefficients(1.0, 1.5, brewster, polarization="p")
    assert result.reflectance == pytest.approx(0.0, abs=1e-15)
    assert brewster.to(ureg.degree).magnitude == pytest.approx(56.309932, rel=1e-7)
    assert critical_angle(1.5, 1.0).to(ureg.degree).magnitude == pytest.approx(
        41.810315, rel=1e-7
    )
    with pytest.raises(ValueError, match="incident_index"):
        critical_angle(1.0, 1.5)


def test_total_internal_reflection_has_unit_reflectance():
    """Above the critical angle, a lossless interface transmits no power."""
    result = fresnel_coefficients(1.5, 1.0, 50 * ureg.degree, polarization="s")
    assert result.reflectance == pytest.approx(1.0)
    assert result.transmittance == pytest.approx(0.0, abs=1e-15)


@pytest.mark.parametrize("polarization", ["s", "p"])
def test_empty_stack_matches_single_interface(polarization):
    """A stack without films reduces to its bounding interface."""
    interface = fresnel_coefficients(1.0, 1.5, 25 * ureg.degree, polarization=polarization)
    stack = thin_film_stack(
        550 * ureg.nanometer,
        [],
        incident_index=1.0,
        substrate_index=1.5,
        angle=25 * ureg.degree,
        polarization=polarization,
    )
    assert stack.reflectance == pytest.approx(interface.reflectance)
    assert stack.transmittance == pytest.approx(interface.transmittance)


def test_quarter_wave_antireflection_layer():
    """An ideal quarter-wave matching layer suppresses design-wave reflection."""
    substrate = 1.5
    layer_index = np.sqrt(substrate)
    wavelength = 600 * ureg.nanometer
    thickness = wavelength / (4 * layer_index)
    result = thin_film_stack(
        wavelength,
        [ThinFilmLayer(layer_index, thickness)],
        substrate_index=substrate,
    )
    assert result.reflectance == pytest.approx(0.0, abs=1e-14)
    assert result.transmittance == pytest.approx(1.0)


def test_stack_supports_spectra_and_material_models():
    """Layers and bounding media may use existing PyOptik material models."""
    film = TabulatedMaterial.from_arrays(
        "film", [400, 700] * ureg.nanometer, n=[2.0, 2.0]
    )
    wavelengths = np.array([500, 600]) * ureg.nanometer
    result = thin_film_stack(
        wavelengths,
        [(film, 75 * ureg.nanometer)],
        substrate_index=1.5,
    )
    assert result.reflectance.shape == (2,)
    assert np.all((result.reflectance >= 0) & (result.reflectance <= 1))
    assert result.reflectance + result.transmittance == pytest.approx(np.ones(2))


def test_absorbing_film_has_positive_absorptance():
    """The package's n + i*k convention produces attenuation, not gain."""
    result = thin_film_stack(
        500 * ureg.nanometer,
        [(2 + 0.1j, 100 * ureg.nanometer)],
        substrate_index=1.5,
    )
    assert 0 < result.absorptance < 1
    assert result.reflectance + result.transmittance + result.absorptance == pytest.approx(1)


@pytest.mark.parametrize("call, message", [
    (lambda: fresnel_coefficients(1, 1.5, polarization="x"), "polarization"),
    (lambda: fresnel_coefficients(1, 1.5, -1), "angle"),
    (lambda: brewster_angle(1 + 0.1j, 1.5), "lossless"),
    (lambda: thin_film_stack(-500e-9, []), "wavelength"),
    (lambda: thin_film_stack(500e-9, [(1.5, -1e-9)]), "thickness"),
])
def test_optics_validation_errors(call, message):
    """Invalid physical inputs fail with an actionable error."""
    with pytest.raises(ValueError, match=message):
        call()


def test_material_interface_requires_wavelength():
    """Dispersive material interfaces require an evaluation wavelength."""
    material = TabulatedMaterial.from_arrays("glass", [0.4, 0.7], n=[1.5, 1.5])
    with pytest.raises(ValueError, match="wavelength is required"):
        fresnel_coefficients(1.0, material)
    result = fresnel_coefficients(1.0, material, wavelength=550 * ureg.nanometer)
    assert result.reflectance == pytest.approx(0.04)
