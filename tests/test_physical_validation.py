"""Physical assumptions are configurable; malformed numerical data is not."""

import warnings

import numpy as np
import pytest
from TypedUnit import ureg

from PyOptik import (
    MaterialValidationWarning, SellmeierMaterial, TabulatedMaterial,
    validate_refractive_indices, validate_wavelengths,
)


@pytest.mark.parametrize("value, message", [(-1 + 0.1j, "must be positive"), (1 - 0.1j, "contains gain"), (0, "must be positive")])
def test_default_warning_and_strict_policy(value, message):
    with pytest.warns(MaterialValidationWarning, match=message):
        result = validate_refractive_indices(value)
    assert result == value
    with pytest.raises(ValueError, match=message):
        validate_refractive_indices(value, policy="raise")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert validate_refractive_indices(value, policy="ignore") == value


def test_explicit_allowances_are_independent():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        validate_refractive_indices(-1 - 0.1j, policy="raise", allow_negative_index=True, allow_gain=True)
    with pytest.raises(ValueError, match="gain"):
        validate_refractive_indices(-1 - 0.1j, policy="raise", allow_negative_index=True)
    with pytest.raises(ValueError, match="positive"):
        validate_refractive_indices(-1 - 0.1j, policy="raise", allow_gain=True)


@pytest.mark.parametrize("policy", ["ignore", "warn", "raise"])
@pytest.mark.parametrize("value", [[], [np.nan], [np.inf], [1 + np.inf * 1j]])
def test_nonfinite_or_empty_samples_always_raise(policy, value):
    with pytest.raises(ValueError, match="nonempty and finite"):
        validate_refractive_indices(value, policy=policy, allow_gain=True, allow_negative_index=True)


@pytest.mark.parametrize("kwargs", [{"policy": "invalid"}, {"tolerance": -1}, {"tolerance": np.inf}, {"tolerance": np.nan}])
def test_invalid_policy_options_raise(kwargs):
    with pytest.raises(ValueError):
        validate_refractive_indices(1.5, **kwargs)


def test_gain_tolerance_does_not_relax_real_index_check():
    validate_refractive_indices([1 - 1e-13j], policy="raise")
    with pytest.raises(ValueError, match="gain"):
        validate_refractive_indices([1 - 1e-13j], policy="raise", tolerance=0)
    with pytest.raises(ValueError, match="positive"):
        validate_refractive_indices([-1e-13], policy="raise")


@pytest.mark.parametrize("kind", ["tabulated", "formula"])
def test_evaluation_and_aliases_apply_validation(kind):
    material = (TabulatedMaterial.from_arrays("negative", [0.4, 0.5], n=[-1, -2]) if kind == "tabulated"
                else SellmeierMaterial.from_coefficients("negative", [-1, 0, 1], formula_type=5, wavelength_range=[0.4, 0.5]))
    wavelength = 450 * ureg.nanometer
    with pytest.warns(MaterialValidationWarning, match="positive"):
        material.compute_refractive_index(wavelength)
    with pytest.raises(ValueError, match="positive"):
        material.nk(wavelength, validation="raise")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert material.n(wavelength, validation="raise", allow_negative_index=True) < 0


def test_array_export_uses_same_policy():
    material = TabulatedMaterial.from_arrays("gain", [0.4, 0.5], n=[1, 2], k=[-0.1, -0.2])
    with pytest.warns(MaterialValidationWarning, match="gain"):
        material.to_arrays()
    with pytest.raises(ValueError, match="gain"):
        material.to_arrays(validation="raise")
    _, _, k = material.to_arrays(validation="raise", allow_gain=True)
    assert k == pytest.approx([-0.1, -0.2])


@pytest.mark.parametrize("values", [[], [0], [-1], [np.nan], [np.inf]])
def test_invalid_wavelengths_rejected_even_when_unbounded(values):
    with pytest.raises(ValueError, match="strictly positive"):
        validate_wavelengths(values)
    material = SellmeierMaterial.from_coefficients("unbounded", [1.4, 0, 1], formula_type=5)
    with pytest.raises(ValueError, match="strictly positive"):
        material.compute_refractive_index(np.asarray(values) * ureg.nanometer, validation="ignore")


def test_valid_wavelength_units_and_shape_are_preserved():
    wavelength = np.array([[400, 500]]) * ureg.nanometer
    assert validate_wavelengths(wavelength) is wavelength
    result = validate_refractive_indices(np.ones((2, 3)), policy="raise")
    assert result.shape == (2, 3)
