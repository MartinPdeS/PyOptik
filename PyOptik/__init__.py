try:
    from ._version import version as __version__  # noqa: F401

except ImportError:
    __version__ = "0.0.0"

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())


from .material_type import MaterialType
from .catalog import MaterialCatalog, MaterialId, MaterialPage, download_snapshot

from .material import TabulatedMaterial
from .material import SellmeierMaterial
from .material import FormulaDataset, MaterialDocument, MaterialMetadata, TabulatedDataset, parse_material
from .thin_film import (
    FresnelResult,
    ThinFilmLayer,
    ThinFilmResult,
    brewster_angle,
    critical_angle,
    fresnel_coefficients,
    thin_film_stack,
)
from .material import base_class


TIMEOUT = 10  # Default timeout for requests in seconds
