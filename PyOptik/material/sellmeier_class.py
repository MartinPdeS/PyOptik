#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import logging
from matplotlib import pyplot as plt
from TypedUnit import Length, RefractiveIndex, validate_units, ureg

from PyOptik.directories import material_paths
from PyOptik.material_type import MaterialType
from PyOptik.material.base_class import BaseMaterial
from PyOptik.material.dataset import FormulaDataset, MaterialDocument, MaterialMetadata, parse_material

logger = logging.getLogger(__name__)


class SellmeierMaterial(BaseMaterial):
    """
    Class representing a material with Sellmeier coefficients for refractive index computation.

    Attributes
    ----------
    filename : str
        The name of the YAML file containing material properties.
    coefficients : numpy.ndarray
        The Sellmeier coefficients used for calculating the refractive index.
    wavelength_range : Optional[Tuple[float, float]]
        The allowable wavelength range for the material in micrometers.
    reference : Optional[str]
        Reference information for the material data.
    formula_type : int
        The formula type to use for refractive index calculation.
    """
    def __init__(self, filename: str, file_path=None):
        """
        Initializes the SellmeierMaterial with a filename.

        Parameters
        ----------

        filename : str
            The name of the YAML file containing material properties.
        file_path : pathlib.Path, optional
            Explicit YAML path for hierarchy-preserving catalog pages. When
            omitted, the user material directory is searched.
        """
        self.filename = filename
        self.file_path = file_path

        self.coefficients = None
        self.wavelength_bound = None
        self.reference = None
        self.conditions = None
        self.comments = None
        self.formula_type = None

        self._load_coefficients()

    def __str__(self) -> str:
        """Return the material name and ``Sellmeier`` model type."""
        return self.filename + '[Sellmeier]'

    def _load_coefficients(self) -> None:
        """
        Loads the Sellmeier coefficients, wavelength range, formula type, and reference from the specified YAML file.
        """
        file_path = self.file_path or next(
            (directory / f"{self.filename}.yml"
             for directory in material_paths(MaterialType.SELLMEIER)
             if (directory / f"{self.filename}.yml").exists()),
            None,
        )
        if file_path is None:
            raise FileNotFoundError(f"Sellmeier YAML file '{self.filename}.yml' not found.")

        file_path = file_path.with_suffix('.yml')
        try:
            document = parse_material(file_path)
        except ValueError as error:
            raise ValueError(f"Invalid Sellmeier data in YAML file {file_path}: {error}") from error
        logger.debug("Loaded Sellmeier data from %s", file_path)
        if not document.formula_datasets:
            raise ValueError(f"No formula dataset found in {file_path}")
        dataset = document.formula_datasets[0]
        self._document = document
        self.formula_type = dataset.formula_type
        self.coefficients = numpy.asarray(dataset.coefficients)
        self.wavelength_bound = (
            numpy.asarray(dataset.wavelength_range) * ureg.micrometer
            if dataset.wavelength_range is not None else None
        )
        self.reference = document.metadata.reference
        self.conditions = dict(document.metadata.conditions)
        self.comments = document.metadata.comments
        logger.debug("Validated Sellmeier material '%s' with formula %s", self.filename, self.formula_type)

    @classmethod
    def from_coefficients(
        cls,
        name: str,
        coefficients,
        *,
        formula_type: int = 1,
        wavelength_range=None,
        reference: str | None = None,
        conditions=None,
        comments: str | None = None,
    ):
        """Construct a formula material without an intermediate YAML file.

        ``wavelength_range`` may be a unit-bearing two-element quantity or a
        pair interpreted as micrometres.
        """
        if wavelength_range is None:
            bounds = None
        elif isinstance(wavelength_range, ureg.Quantity):
            bounds = tuple(float(value) for value in wavelength_range.to(ureg.micrometer).magnitude)
        else:
            bounds = tuple(float(value) for value in wavelength_range)
        document = MaterialDocument(
            (FormulaDataset(formula_type, tuple(float(value) for value in coefficients), bounds),),
            MaterialMetadata(reference, dict(conditions or {}), comments),
        )
        material = cls.__new__(cls)
        material.filename = name
        material.file_path = None
        material._document = document
        dataset = document.formula_datasets[0]
        material.formula_type = dataset.formula_type
        material.coefficients = numpy.asarray(dataset.coefficients)
        material.wavelength_bound = (
            numpy.asarray(bounds) * ureg.micrometer if bounds is not None else None
        )
        material.reference = reference
        material.conditions = dict(conditions or {})
        material.comments = comments
        return material

    def to_yaml(self, path):
        """Export this material as a validated, reloadable YAML document."""
        return self._document.to_yaml(path)

    @validate_units
    def compute_refractive_index(self, wavelength: Length | float, out_of_range: str = "warn") -> RefractiveIndex:
        r"""
        Computes the refractive index n(\u03bb) using the appropriate
        RefractiveIndex.INFO dispersion formula (types 1 through 9).

        Parameters
        ----------
        wavelength : Length | float
            The wavelength \u03bb in meters, can be a single float or a numpy array.
        out_of_range : {"warn", "raise", "clip"}, optional
            Policy for wavelengths outside the source validity range.

        Returns
        -------
        RefractiveIndex
            The refractive index n(\u03bb) for the given wavelength or array of wavelengths.

        Raises
        ------
        ValueError
            If the wavelength is outside the specified range or if an unsupported formula type is encountered.
        """
        if not isinstance(wavelength, Length):
            wavelength = wavelength * ureg.meter

        return_as_scalar = numpy.isscalar(wavelength.magnitude)

        wavelength = numpy.atleast_1d(wavelength)
        self._check_wavelength(wavelength, out_of_range)
        if out_of_range == "clip":
            wavelength = self._clip_wavelength(wavelength)

        # Formula definitions follow the RefractiveIndex.INFO database
        # documentation. Wavelengths are expressed in micrometres here.
        wavelength_um = wavelength.to(ureg.micrometer).magnitude
        coefficients = self.coefficients
        padded = numpy.pad(coefficients, (0, 10))

        match self.formula_type:
            case 1:  # Formula 1 computation (standard Sellmeier)
                n_squared = 1.0 + padded[0]
                for B, C in zip(coefficients[1::2], coefficients[2::2]):
                    n_squared += B * wavelength_um**2 / (wavelength_um**2 - C**2)
                n = numpy.sqrt(n_squared)

            case 2:  # Formula 2 computation (extended Sellmeier)
                n_squared = 1 + padded[0]
                for B, C in zip(coefficients[1::2], coefficients[2::2]):
                    n_squared += B * wavelength_um**2 / (wavelength_um**2 - C)
                n = numpy.sqrt(n_squared)

            case 3:  # Polynomial
                n_squared = padded[0]
                for B, exponent in zip(coefficients[1::2], coefficients[2::2]):
                    n_squared += B * wavelength_um**exponent
                n = numpy.sqrt(n_squared)

            case 4:  # RefractiveIndex.INFO
                n_squared = padded[0]
                for index in range(1, min(8, len(coefficients)), 4):
                    B, exponent, C, power = padded[index:index + 4]
                    n_squared += B * wavelength_um**exponent / (wavelength_um**2 - C**power)
                for B, exponent in zip(coefficients[9::2], coefficients[10::2]):
                    n_squared += B * wavelength_um**exponent
                n = numpy.sqrt(n_squared)

            case 5:  # Formula 5 computation (extended Sellmeier)
                n = padded[0]
                for B, exponent in zip(coefficients[1::2], coefficients[2::2]):
                    n += B * wavelength_um**exponent

            case 6:
                n = 1 + padded[0]
                for B, C in zip(coefficients[1::2], coefficients[2::2]):
                    n += B / (C - wavelength_um**-2)

            case 7:  # Herzberger
                n = padded[0] + padded[1] / (wavelength_um**2 - 0.028)
                n += padded[2] / (wavelength_um**2 - 0.028)**2
                for index, coefficient in enumerate(coefficients[3:], start=3):
                    n += coefficient * wavelength_um**(2 * (index - 2))

            case 8:  # Retro
                temporary = padded[0] + padded[1] * wavelength_um**2 / (wavelength_um**2 - padded[2])
                temporary += padded[3] * wavelength_um**2
                n = numpy.sqrt((2 * temporary + 1) / (1 - temporary))

            case 9:  # Exotic
                n = numpy.sqrt(
                    padded[0]
                    + padded[1] / (wavelength_um**2 - padded[2])
                    + padded[3] * (wavelength_um - padded[4])
                    / ((wavelength_um - padded[4])**2 + padded[5])
                )

            case _:
                raise ValueError(f"Unsupported formula type: {self.formula_type}")

        return n[0] if return_as_scalar else n

    def plot(self, axes=None, samples: int = 100) -> None:
        """
        Plots the refractive index as a function of wavelength over a specified range.

        Parameters
        ----------
        axes : matplotlib.axes.Axes, optional
            Axes on which to draw the dispersion curve. A compact, styled
            figure is created when omitted.
        samples : int
            The number of samples to use for the wavelength range.

        Returns
        -------
        None
            The supplied axes are modified in place.

        Raises
        ------
        ValueError
            If the wavelength is not a 1D array or list of float values.
        """
        if axes is None:
            figure, axes = plt.subplots(figsize=(7, 4.5), layout="constrained")
        else:
            figure = axes.figure
        figure.set_size_inches(7, 4.5, forward=True)
        wavelength = numpy.linspace(
            self.wavelength_bound[0].magnitude,
            self.wavelength_bound[1].magnitude,
            samples
        ) * self.wavelength_bound.units

        # Calculate the refractive index over the wavelength range
        refractive_index = self.compute_refractive_index(wavelength)

        axes.set(
            ylabel='Refractive Index',
            xlabel=r'Wavelength [$\mu$m]',
            title=f"Refractive index: {self.filename}",
        )
        axes.set_title(axes.get_title(), fontsize=14, pad=12)
        axes.set_xlabel(axes.get_xlabel(), fontsize=11)
        axes.set_ylabel(axes.get_ylabel(), fontsize=11)
        axes.tick_params(labelsize=10)
        axes.grid(alpha=0.25, linewidth=0.7)
        axes.plot(wavelength.to(ureg.micrometer).magnitude, refractive_index.real, linewidth=2, label='n')
        axes.legend()
        return None

    def print(self) -> str:
        """
        Provides a formal string representation of the Material object, including key attributes.

        Returns
        -------
        str
            Formal representation of the Material object.
        """
        return (
            f"\nMaterial: '{self.filename}',\n"
            f"coefficients: {self.coefficients},\n"
            f"wavelength_range: {self.wavelength_bound},\n"
            f"formula_type: {self.formula_type},\n"
            f"reference: '{self.reference}')"
        )
