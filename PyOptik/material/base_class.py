#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable
import numpy
import warnings
import logging

from TypedUnit import Length, AnyUnit, Time, ureg, validate_units

logger = logging.getLogger(__name__)

class BaseMaterial(object):
    """Common interface for refractive-index material models.

    Subclasses provide :meth:`compute_refractive_index`; this class supplies
    unit handling, validity-range checks, and group-delay calculations.
    """

    def __eq__(self, other) -> bool:
        """Compare materials by concrete type and filename.

        Parameters
        ----------
        other : object
            Object to compare with this material.

        Returns
        -------
        bool
            True when both objects represent the same material class and file.
        """
        if not isinstance(other, self.__class__):
            return False

        if self.filename != other.filename:
            return False

        return True

    def __str__(self) -> str:
        """
        Provides an informal string representation of the Material object.

        Returns
        -------
        str
            Informal representation of the Material object.
        """
        return f"Material: {self.filename}"

    def __repr__(self) -> str:
        """Return a concise, informative representation of the material.

        The representation includes the concrete model, source filename, and
        validity range when available. Numerical arrays are intentionally not
        included, so inspecting a material never produces a large output.
        """
        details = [f"filename={self.filename!r}"]
        file_path = getattr(self, "file_path", None)
        if file_path is not None:
            details.append(f"file_path={str(file_path)!r}")
        wavelength_bound = getattr(self, "wavelength_bound", None)
        if wavelength_bound is not None:
            details.append(f"wavelength_range={wavelength_bound!r}")
        return f"{type(self).__name__}({', '.join(details)})"

    def _check_wavelength(self, wavelength: Length, out_of_range: str = "warn") -> None:
        """
        Checks if a wavelength is within the material's allowable range and raises a warning if it is not.

        Parameters
        ----------
        wavelength : Length
            The wavelength to check, in micrometers.
        out_of_range : {"warn", "raise", "clip"}, optional
            Policy for wavelengths outside ``wavelength_bound``.

        Raises
        ------
        UserWarning
            If the wavelength is outside the allowable range.
        ValueError
            If ``out_of_range`` is invalid or has value ``"raise"`` for an
            out-of-range wavelength.
        """
        if out_of_range not in {"warn", "raise", "clip"}:
            raise ValueError("out_of_range must be 'warn', 'raise', or 'clip'.")
        if self.wavelength_bound is not None:
            min_value, max_value = self.wavelength_bound

            if numpy.any((wavelength < min_value) | (wavelength > max_value)):
                message = (
                    f"Wavelength range goes from {wavelength.min().to_compact()} to {wavelength.max().to_compact()} "
                    f"which is outside the allowable range of {min_value.to_compact()} to {max_value.to_compact()} µm. "
                    f"[Material: {self.filename}]"
                )
                if out_of_range == "raise":
                    logger.error("Wavelength validation failed: %s", message)
                    raise ValueError(message)
                if out_of_range == "clip":
                    logger.debug("Clipping out-of-range wavelengths for material '%s'", self.filename)
                    return
                logger.warning(message)
                warnings.warn(
                    message,
                    stacklevel=2,
                )

    def _clip_wavelength(self, wavelength: Length) -> Length:
        """Clip wavelengths to the material validity interval.

        Parameters
        ----------
        wavelength : Length
            Wavelength quantity to clip.

        Returns
        -------
        Length
            Wavelengths constrained to the material's validity interval.
        """
        if self.wavelength_bound is None:
            return wavelength
        values = numpy.clip(
            wavelength.to(ureg.meter).magnitude,
            self.wavelength_bound[0].to(ureg.meter).magnitude,
            self.wavelength_bound[1].to(ureg.meter).magnitude,
        )
        return values * ureg.meter

    def ensure_units(func) -> Callable:
        """Decorator ensuring the wavelength argument carries ureg.

        Parameters
        ----------
        func : Callable
            Function that expects a wavelength :class:`~PyOptik.ureg.Quantity`.

        Returns
        -------
        Callable
            Wrapped version of ``func`` that accepts numerical wavelengths and
            converts them to metre-based :class:`~PyOptik.ureg.Quantity` objects.
        """
        def wrapper(self, wavelength: Length = None, *args, **kwargs):
            """Apply the unit-normalization behavior of the decorator."""
            if wavelength is None:
                if self.wavelength_bound is None:
                    raise ValueError('Wavelength must be provided for computation.')
                wavelength = numpy.linspace(self.wavelength_bound[0].magnitude, self.wavelength_bound[1].magnitude, 100) * self.wavelength_bound.units

            if not isinstance(wavelength, ureg.Quantity):
                wavelength = wavelength * ureg.meter
            return func(self, wavelength, *args, **kwargs)
        return wrapper

    @validate_units
    def compute_group_index(self, wavelength: Length, delta: Length = 1 * ureg.nanometer) -> Length:
        """
        Calculate the group refractive index n_g(\u03bb).
        The group index is defined as n_g(\u03bb) = n(\u03bb) - \u03bb * dn/d\u03bb,
        where n(\u03bb) is the refractive index and dn/d\u03bb is the derivative of
        the refractive index with respect to wavelength.

        Parameters
        ----------
        wavelength : ureg.Quantity
            Wavelength at which to compute the group index, in metres.
        delta : ureg.Quantity, optional
            Small change in wavelength for numerical differentiation, default is 1 nanometer.

        Returns
        -------
        ureg.Quantity
            Group refractive index at the specified wavelength, in dimensionless ureg.
        -------
        ureg.Quantity
            Group refractive index at the specified wavelength, in dimensionless ureg.
        """
        n = self.compute_refractive_index(wavelength)
        n_plus = self.compute_refractive_index(wavelength + delta / 2)
        n_minus = self.compute_refractive_index(wavelength - delta / 2)
        dn_dlambda = (n_plus - n_minus) / delta
        return n - wavelength * dn_dlambda

    @validate_units
    def compute_group_velocity(self, wavelength: Length) -> AnyUnit:
        """
        Calculate the group velocity v_g(\u03bb) = c / n_g(\u03bb),
        where c is the speed of light in vacuum and n_g(\u03bb) is the group index.

        Parameters
        ----------
        wavelength : Length
            Wavelength at which to compute the group velocity, in metres.

        Returns
        -------
        AnyUnit
            Group velocity at the specified wavelength, in metres per second.
        """
        ng = self.compute_group_index(wavelength)
        c = 299792458 * ureg.meter / ureg.second
        return c / ng

    @validate_units
    def compute_group_delay(
        self,
        wavelength: Length,
        length: Length = 1 * ureg.meter,
    ) -> Time:
        """Calculate the group delay for a given propagation length.

        Parameters
        ----------
        wavelength : Length
            Wavelength at which to compute the group delay, in metres.
        length : Length, optional
            Propagation length (default is 1 metre).

        Returns
        -------
        Time
            Group delay for the specified wavelength and length.
        """
        vg = self.compute_group_velocity(wavelength)
        return length / vg

    @validate_units
    def compute_group_delay_wavelength_slope(
        self,
        wavelength: Length,
        length: Length = 1 * ureg.meter,
        delta: Length = 1 * ureg.nanometer,
    ) -> AnyUnit:
        """Calculate the wavelength slope ``dτ_g/dλ`` for a given length.

        This is a wavelength-space derivative, not conventional GDD.

        Parameters
        ----------
        wavelength : Length
            Central wavelength for the computation, in metres.
        length : Length, optional
            Propagation length (default is 1 metre).
        delta : Length, optional
            Wavelength step used for the numerical differentiation (default is
            1 nanometre).

        Returns
        -------
        AnyUnit
            Wavelength derivative of group delay evaluated at ``wavelength``.
        """
        gd_plus = self.compute_group_delay(wavelength + delta / 2, length)
        gd_minus = self.compute_group_delay(wavelength - delta / 2, length)
        return (gd_plus - gd_minus) / delta

    @validate_units
    def compute_group_delay_dispersion(
        self,
        wavelength: Length,
        length: Length = 1 * ureg.meter,
        delta_angular_frequency: AnyUnit = 2 * numpy.pi * 1e12 / ureg.second,
    ) -> AnyUnit:
        """Calculate conventional GDD, ``dτ_g/dω = d²β/dω² × length``.

        The derivative is evaluated with a centred finite difference in
        angular frequency and has time-squared units (commonly fs²). Use
        :meth:`compute_group_delay_wavelength_slope` for ``dτ_g/dλ``.

        Parameters
        ----------
        wavelength : Length
            Central vacuum wavelength.
        length : Length, optional
            Propagation length.
        delta_angular_frequency : ureg.Quantity, optional
            Positive centred angular-frequency increment. The default is
            ``2π × 1 THz``.

        Returns
        -------
        AnyUnit
            Conventional group-delay dispersion with time-squared units.

        Raises
        ------
        TypeError
            If ``delta_angular_frequency`` does not carry units.
        ValueError
            If ``delta_angular_frequency`` is not positive.
        """
        if not isinstance(delta_angular_frequency, ureg.Quantity):
            raise TypeError("delta_angular_frequency must carry units.")
        if delta_angular_frequency.magnitude <= 0:
            raise ValueError("delta_angular_frequency must be positive.")
        speed_of_light = 299792458 * ureg.meter / ureg.second
        frequency_unit = 1 / ureg.second
        omega = (2 * numpy.pi * speed_of_light / wavelength).to(frequency_unit)
        delta = delta_angular_frequency.to(frequency_unit)
        wavelength_plus = 2 * numpy.pi * speed_of_light / (omega + delta / 2)
        wavelength_minus = 2 * numpy.pi * speed_of_light / (omega - delta / 2)
        delay_plus = self.compute_group_delay(wavelength_plus, length)
        delay_minus = self.compute_group_delay(wavelength_minus, length)
        return (delay_plus - delay_minus) / delta
