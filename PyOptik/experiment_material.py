#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections.abc import Iterable
from MPSTools.material_catalogue.loader import load_material_measurements, get_material_measurment_index  # noqa: F401
from MPSPlots.render2D import SceneList


class DataMeasurement:
    """
    The DataMeasurement class is used to compute the refractive index from the
    locally saved measurement data.

    Arguments:
    material_name -- the name of the material you wish to import
    """

    def __init__(self, material_name: str) -> None:
        self.material_name = material_name

        self.configuration = load_material_measurements(self.material_name)

    @property
    def reference(self) -> str:
        return self.configuration['REFERENCES']

    def get_refractive_index(self, wavelength_range: float | Iterable) -> float | Iterable:
        """
        Gets the refractive index for the specific given wavelength range.

        :param      wavelength:  The wavelength range, units are supposed to be meters.
        :type       wavelength:  float | Iterable

        :returns:   The refractive index.
        :rtype:     float | Iterable
        """
        return get_material_measurment_index(
            material_name=self.material_name,
            wavelength=wavelength_range
        )

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

    def __repr__(self) -> str:
        return self.material_name

    def __str__(self) -> str:
        return self.__repr__()
