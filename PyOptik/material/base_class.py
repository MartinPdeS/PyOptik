#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable
import numpy
import warnings

from TypedUnit import Length, AnyUnit, Time, ureg, validate_units

class BaseMaterial(object):
    def __eq__(self, other) -> bool:
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
        """
        Provides a formal string representation of the Material object, including key attributes.

        Returns
        -------
        str
            Formal representation of the Material object.
        """
        return self.__str__()

    def _check_wavelength(self, wavelength: Length) -> None:
        """
        Checks if a wavelength is within the material's allowable range and raises a warning if it is not.

        Parameters
        ----------
        wavelength : Length
            The wavelength to check, in micrometers.

        Raises
        ------
        UserWarning
            If the wavelength is outside the allowable range.
        """
        if self.wavelength_bound is not None:
            min_value, max_value = self.wavelength_bound

            if numpy.any((wavelength < min_value) | (wavelength > max_value)):
                warnings.warn(
                    f"Wavelength range goes from {wavelength.min().to_compact()} to {wavelength.max().to_compact()} "
                    f"which is outside the allowable range of {min_value.to_compact()} to {max_value.to_compact()} µm. "
                    f"[Material: {self.filename}]"
                )

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
    def compute_group_delay_dispersion(
        self,
        wavelength: Length,
        length: Length = 1 * ureg.meter,
        delta: Length = 1 * ureg.nanometer,
    ) -> AnyUnit:
        """Calculate ``d\u03c4_g/d\u03bb`` for a given propagation length.

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
            Group delay dispersion evaluated at ``wavelength``.
        """
        gd_plus = self.compute_group_delay(wavelength + delta / 2, length)
        gd_minus = self.compute_group_delay(wavelength - delta / 2, length)
        return (gd_plus - gd_minus) / delta
