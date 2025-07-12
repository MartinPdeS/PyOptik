#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable
from PyOptik.units import Quantity, meter
import numpy
import warnings


class BaseMaterial:
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

    def _check_wavelength(self, wavelength: Quantity) -> None:
        """
        Checks if a wavelength is within the material's allowable range and raises a warning if it is not.

        Parameters
        ----------
        wavelength : Quantity
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
        """Decorator ensuring the wavelength argument carries units.

        Parameters
        ----------
        func : Callable
            Function that expects a wavelength :class:`~PyOptik.units.Quantity`.

        Returns
        -------
        Callable
            Wrapped version of ``func`` that accepts numerical wavelengths and
            converts them to metre-based :class:`~PyOptik.units.Quantity` objects.
        """
        def wrapper(self, wavelength: Quantity = None, *args, **kwargs):
            if wavelength is None:
                if self.wavelength_bound is None:
                    raise ValueError('Wavelength must be provided for computation.')
                wavelength = numpy.linspace(self.wavelength_bound[0].magnitude, self.wavelength_bound[1].magnitude, 100) * self.wavelength_bound.units

            import PyOptik.units
            if not isinstance(wavelength, PyOptik.units.Quantity):
                wavelength = wavelength * meter
            return func(self, wavelength, *args, **kwargs)
        return wrapper
