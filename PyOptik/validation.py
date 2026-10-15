"""Configurable checks for optical constants, independent of a solver."""

import warnings

import numpy as np


class MaterialValidationWarning(UserWarning):
    """Optical constants violate the requested physical assumptions."""


def validate_refractive_indices(values, *, policy="warn", allow_negative_index=False, allow_gain=False, tolerance=1e-12):
    """Validate samples and return a complex NumPy array.

    ``policy`` is 'ignore', 'warn' (default), or 'raise'. By default nonpositive
    real indices and negative extinction coefficients are reported. Explicit
    allowances support zero/negative-index and active materials respectively.
    Gain follows the n + i*k convention with positive k describing absorption.
    ``tolerance`` applies only to negative extinction coefficients. Empty or
    nonfinite samples and invalid options always raise, even with 'ignore'.
    These checks validate samples, not causality or an entire dispersion curve.
    """
    if policy not in {"ignore", "warn", "raise"}:
        raise ValueError("policy must be 'ignore', 'warn', or 'raise'.")
    if not np.isscalar(tolerance) or not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative.")
    indices = np.asarray(values, dtype=complex)
    if indices.size == 0 or not np.all(np.isfinite(indices)):
        raise ValueError("Refractive-index samples must be nonempty and finite.")
    issues = []
    if not allow_negative_index and np.any(indices.real <= 0):
        issues.append("The real part of the refractive index must be positive; use allow_negative_index=True for zero/negative-index materials.")
    if not allow_gain and np.any(indices.imag < -tolerance):
        issues.append("The material contains gain; passive data requires imag(n) >= 0. Use allow_gain=True for active materials.")
    if issues and policy != "ignore":
        message = " ".join(issues)
        if policy == "raise":
            raise ValueError(message)
        warnings.warn(message, MaterialValidationWarning, stacklevel=2)
    return indices


def validate_wavelengths(wavelength):
    """Require nonempty, finite, positive wavelengths and return the input.

    Quantities are checked in metres. Plain numerical values are checked in
    their existing unit; this function does not infer or attach units.
    """
    values = wavelength.to("meter").magnitude if hasattr(wavelength, "to") else wavelength
    values = np.asarray(values, dtype=float)
    if values.size == 0 or not np.all(np.isfinite(values)) or np.any(values <= 0):
        raise ValueError("Wavelengths must be nonempty, finite and strictly positive.")
    return wavelength
