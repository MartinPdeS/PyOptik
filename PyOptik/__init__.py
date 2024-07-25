from PyOptik.experiment_material import DataMeasurement
from PyOptik.sellmeier_material import Sellmeier
import numpy
import pandas


try:
    from ._version import version as __version__  # noqa: F401

except ImportError:
    __version__ = "0.0.0"


class UsualMaterial:
    BK7 = Sellmeier('BK7')
    FusedSilica = Sellmeier('silica')
    SodaLimeGlass = DataMeasurement('sodalimeglass')
    Silver = DataMeasurement('silver')
    Gold = DataMeasurement('gold')
    Aluminium = DataMeasurement('aluminium')
    SI = Sellmeier('silica')
    SIO2 = DataMeasurement('sio2')
    TIO2 = DataMeasurement('tio2')
    Polystyrene = DataMeasurement('polystyrene')
    Water = DataMeasurement('water')
    Ethanol = DataMeasurement('ethanol')

    @classmethod
    def get_from_string(cls, material_str):
        material_str = numpy.atleast_1d(material_str)

        material_str = [
            mat for mat in material_str if not pandas.isnull(mat)
        ]

        values = [
            getattr(cls, string) for string in material_str
        ]

        values = numpy.asarray(values)

        if values.size == 0:
            return numpy.nan

        return values

# -
