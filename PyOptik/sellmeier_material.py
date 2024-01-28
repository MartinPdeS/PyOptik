#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from collections.abc import Iterable
from MPSTools.material_catalogue.loader import load_material_parameters, get_material_index, list_materials  # noqa: F401
from MPSPlots.render2D import SceneList


class Sellmeier:
    """
    The Sellmeier class is used to compute the refractive index from the
    locally saved Sellmeier formula.

    Arguments:
    name -- the name of the material you wish to import
    unit -- unit use for the wavelength
    """

    def __init__(self, material_name: str) -> None:
        self.material_name = material_name

        self.sellmeier_coeffcients = load_material_parameters(self.material_name)

    @property
    def reference(self) -> str:
        """
        Returns the reference of the coefficents value for the Sellmeier

        :returns:   The reference
        :rtype:     str
        """
        return self.sellmeier_coeffcients['sellmeier']['reference']

    def get_refractive_index(self, wavelength: float | Iterable) -> float | Iterable:
        """
        Gets the refractive index for the specific given wavelength range.

        :param      wavelength:  The wavelength range, units are supposed to be meters.
        :type       wavelength:  float | Iterable

        :returns:   The refractive index.
        :rtype:     float | Iterable
        """
        return_scalar = True if numpy.isscalar(wavelength) else False

        wavelength = numpy.atleast_1d(wavelength).astype(float)

        refractive_index = get_material_index(
            material_name=self.material_name,
            wavelength=wavelength
        )

        if return_scalar:
            return refractive_index[0]

        return refractive_index

    def plot(self, wavelength_range: Iterable) -> SceneList:
        """
        Plot the refractive index as a function of the wavelength.

        :param      wavelength_range:  The wavelength range
        :type       wavelength_range:  Iterable

        :returns:   The scene list.
        :rtype:     SceneList
        """
        scene = SceneList()
        ax = scene.append_ax(
            x_label='Wavelength [m]',
            y_label='Refractive index'
        )

        refractive_index = self.get_refractive_index(wavelength_range)

        ax.add_line(
            x=wavelength_range,
            y=refractive_index,
            line_width=2
        )

        return scene
