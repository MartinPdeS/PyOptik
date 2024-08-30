from docs.deprecated.experiment_material import DataMeasurement
from PyOptik.material import Material
import numpy
import pandas


try:
    from ._version import version as __version__  # noqa: F401

except ImportError:
    __version__ = "0.0.0"



# class UsualMaterial:
#     BK7 = Material('BK7')
#     FusedSilica = Material('silica')
#     SI = Material('silica')

#     @classmethod
#     def get_from_string(cls, material_str):
#         material_str = numpy.atleast_1d(material_str)

#         material_str = [
#             mat for mat in material_str if not pandas.isnull(mat)
#         ]

#         values = [
#             getattr(cls, string) for string in material_str
#         ]

#         values = numpy.asarray(values)

#         if values.size == 0:
#             return numpy.nan

#         return values

# -
