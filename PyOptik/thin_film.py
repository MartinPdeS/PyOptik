"""Fresnel interfaces and coherent thin-film transfer-matrix calculations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

import numpy
from TypedUnit import ureg


@dataclass(frozen=True)
class ThinFilmLayer:
    """One homogeneous layer in a coherent optical stack.

    Parameters
    ----------
    material : complex or BaseMaterial
        Constant complex refractive index or a PyOptik material model.
    thickness : Length
        Physical layer thickness. Bare numbers are interpreted as metres.
    """

    material: Any
    thickness: Any


@dataclass(frozen=True)
class FresnelResult:
    """Amplitude coefficients and power fractions at one interface."""

    reflection_amplitude: Any
    transmission_amplitude: Any
    reflectance: Any
    transmittance: Any
    absorptance: Any
    transmitted_angle: Any


@dataclass(frozen=True)
class ThinFilmResult:
    """Coherent reflection, transmission, and absorption of a layer stack."""

    reflection_amplitude: Any
    transmission_amplitude: Any
    reflectance: Any
    transmittance: Any
    absorptance: Any


def fresnel_coefficients(
    incident_index,
    transmitted_index,
    angle=0.0,
    *,
    polarization: str = "s",
    wavelength=None,
) -> FresnelResult:
    """Calculate Fresnel amplitude coefficients and power fractions.

    Parameters
    ----------
    incident_index, transmitted_index : complex or BaseMaterial
        Refractive indices or material models on either side of the interface.
    angle : float or angle quantity, optional
        Incidence angle. Bare values are radians.
    polarization : {"s", "p"}, optional
        Electric-field polarization.
    wavelength : Length, optional
        Required when either index is a wavelength-dependent material model.
    """
    polarization = _validate_polarization(polarization)
    theta_1 = _angle_radians(angle)
    n_1 = _index_value(incident_index, wavelength)
    n_2 = _index_value(transmitted_index, wavelength)
    sin_theta_2 = n_1 * numpy.sin(theta_1) / n_2
    cos_theta_1 = numpy.cos(theta_1)
    cos_theta_2 = _forward_cosine(n_2, sin_theta_2)
    theta_2 = numpy.lib.scimath.arcsin(sin_theta_2)

    if polarization == "s":
        denominator = n_1 * cos_theta_1 + n_2 * cos_theta_2
        reflection = (n_1 * cos_theta_1 - n_2 * cos_theta_2) / denominator
    else:
        denominator = n_2 * cos_theta_1 + n_1 * cos_theta_2
        reflection = (n_2 * cos_theta_1 - n_1 * cos_theta_2) / denominator
    transmission = 2 * n_1 * cos_theta_1 / denominator
    reflectance = numpy.abs(reflection) ** 2
    flux_ratio = numpy.real(n_2 * cos_theta_2) / numpy.real(n_1 * cos_theta_1)
    transmittance = flux_ratio * numpy.abs(transmission) ** 2
    absorptance = 1 - reflectance - transmittance
    return FresnelResult(
        _scalarize(reflection),
        _scalarize(transmission),
        _scalarize(reflectance),
        _scalarize(transmittance),
        _scalarize(absorptance),
        _scalarize(theta_2) * ureg.radian,
    )


def brewster_angle(incident_index, transmitted_index, *, wavelength=None):
    """Return the p-polarized Brewster angle for two lossless media."""
    n_1 = _lossless_scalar_index(incident_index, wavelength)
    n_2 = _lossless_scalar_index(transmitted_index, wavelength)
    return numpy.arctan2(n_2, n_1) * ureg.radian


def critical_angle(incident_index, transmitted_index, *, wavelength=None):
    """Return the total-internal-reflection critical angle.

    Raises
    ------
    ValueError
        If the media are absorbing or the incident index is not larger than
        the transmitted index.
    """
    n_1 = _lossless_scalar_index(incident_index, wavelength)
    n_2 = _lossless_scalar_index(transmitted_index, wavelength)
    if n_1 <= n_2:
        raise ValueError("critical angle requires incident_index > transmitted_index")
    return numpy.arcsin(n_2 / n_1) * ureg.radian


def thin_film_stack(
    wavelength,
    layers: Iterable[ThinFilmLayer | tuple[Any, Any]],
    *,
    incident_index=1.0,
    substrate_index=1.0,
    angle=0.0,
    polarization: str = "s",
) -> ThinFilmResult:
    """Evaluate a coherent isotropic multilayer using characteristic matrices.

    Wavelength may be scalar or one-dimensional. Layers may be
    :class:`ThinFilmLayer` objects or ``(material, thickness)`` tuples. All
    layers are treated as optically coherent; surface roughness, incoherent
    substrates, anisotropy, and magnetic media are outside this model.
    """
    polarization = _validate_polarization(polarization)
    wavelength_quantity = _wavelength_quantity(wavelength)
    scalar_input = numpy.isscalar(wavelength_quantity.magnitude)
    wavelengths = numpy.atleast_1d(wavelength_quantity)
    normalized_layers = [
        layer if isinstance(layer, ThinFilmLayer) else ThinFilmLayer(*layer)
        for layer in layers
    ]
    results = [
        _stack_at_wavelength(
            item,
            normalized_layers,
            incident_index,
            substrate_index,
            _angle_radians(angle),
            polarization,
        )
        for item in wavelengths
    ]
    reflection, transmission, reflectance, transmittance, absorptance = (
        numpy.asarray(values) for values in zip(*results)
    )
    if scalar_input:
        reflection, transmission, reflectance, transmittance, absorptance = (
            _scalarize(value) for value in
            (reflection, transmission, reflectance, transmittance, absorptance)
        )
    return ThinFilmResult(
        reflection, transmission, reflectance, transmittance, absorptance
    )


def _stack_at_wavelength(wavelength, layers, incident, substrate, angle, polarization):
    """Evaluate one wavelength of a coherent characteristic matrix."""
    n_0 = complex(_index_value(incident, wavelength))
    n_s = complex(_index_value(substrate, wavelength))
    conserved = n_0 * numpy.sin(angle)
    cos_0 = _forward_cosine(n_0, conserved / n_0)
    cos_s = _forward_cosine(n_s, conserved / n_s)
    q_0 = _admittance(n_0, cos_0, polarization)
    q_s = _admittance(n_s, cos_s, polarization)
    matrix = numpy.identity(2, dtype=complex)
    wavelength_m = wavelength.to(ureg.meter).magnitude
    for layer in layers:
        index = complex(_index_value(layer.material, wavelength))
        cosine = _forward_cosine(index, conserved / index)
        q_layer = _admittance(index, cosine, polarization)
        thickness_m = _length_meters(layer.thickness)
        phase = 2 * numpy.pi * index * cosine * thickness_m / wavelength_m
        layer_matrix = numpy.array([
            [numpy.cos(phase), -1j * numpy.sin(phase) / q_layer],
            [-1j * q_layer * numpy.sin(phase), numpy.cos(phase)],
        ])
        matrix = matrix @ layer_matrix
    b_term = matrix[0, 0] + matrix[0, 1] * q_s
    c_term = matrix[1, 0] + matrix[1, 1] * q_s
    denominator = q_0 * b_term + c_term
    reflection = (q_0 * b_term - c_term) / denominator
    transmission = 2 * q_0 / denominator
    reflectance = float(numpy.abs(reflection) ** 2)
    transmittance = float(numpy.real(q_s / q_0) * numpy.abs(transmission) ** 2)
    absorptance = float(numpy.real_if_close(1 - reflectance - transmittance))
    return reflection, transmission, reflectance, transmittance, absorptance


def _admittance(index, cosine, polarization):
    """Return the characteristic optical admittance."""
    return index * cosine if polarization == "s" else index / cosine


def _forward_cosine(index, sine):
    """Select the forward/decaying branch of the complex propagation angle."""
    cosine = numpy.lib.scimath.sqrt(1 - numpy.asarray(sine, dtype=complex) ** 2)
    wavevector = index * cosine
    flip = (numpy.real(wavevector) < 0) | (
        numpy.isclose(numpy.real(wavevector), 0) & (numpy.imag(wavevector) < 0)
    )
    return numpy.where(flip, -cosine, cosine)


def _index_value(value, wavelength):
    """Resolve a constant index or evaluate a PyOptik material model."""
    evaluator = getattr(value, "compute_refractive_index", None)
    if evaluator is None:
        return numpy.asarray(value, dtype=complex)
    if wavelength is None:
        raise ValueError("wavelength is required when using a material model")
    return numpy.asarray(evaluator(wavelength), dtype=complex)


def _lossless_scalar_index(value, wavelength):
    """Return a positive real scalar refractive index."""
    index = numpy.asarray(_index_value(value, wavelength), dtype=complex)
    if index.ndim != 0:
        raise ValueError("angle calculations require scalar refractive indices")
    if not numpy.isclose(index.imag, 0) or index.real <= 0:
        raise ValueError("angle calculations require positive lossless refractive indices")
    return float(index.real)


def _wavelength_quantity(value):
    """Normalize a wavelength to a positive length quantity."""
    quantity = value if isinstance(value, ureg.Quantity) else value * ureg.meter
    meters = numpy.asarray(quantity.to(ureg.meter).magnitude)
    if meters.ndim > 1 or numpy.any(~numpy.isfinite(meters)) or numpy.any(meters <= 0):
        raise ValueError("wavelength must be finite, positive, and at most one-dimensional")
    return quantity


def _length_meters(value):
    """Normalize one positive layer thickness to metres."""
    quantity = value if isinstance(value, ureg.Quantity) else value * ureg.meter
    meters = numpy.asarray(quantity.to(ureg.meter).magnitude)
    if meters.ndim != 0 or not numpy.isfinite(meters) or meters < 0:
        raise ValueError("layer thickness must be a non-negative scalar length")
    return float(meters)


def _angle_radians(value):
    """Normalize a scalar incidence angle to radians."""
    radians = value.to(ureg.radian).magnitude if isinstance(value, ureg.Quantity) else value
    radians = numpy.asarray(radians)
    if radians.ndim != 0 or not numpy.isfinite(radians) or not 0 <= radians < numpy.pi / 2:
        raise ValueError("angle must be a finite scalar in [0, pi/2)")
    return float(radians)


def _validate_polarization(value):
    """Normalize and validate a polarization name."""
    polarization = str(value).lower()
    if polarization not in {"s", "p"}:
        raise ValueError("polarization must be 's' or 'p'")
    return polarization


def _scalarize(value):
    """Convert zero- or one-element arrays to Python/NumPy scalars."""
    array = numpy.asarray(value)
    return array.reshape(-1)[0] if array.size == 1 else array
