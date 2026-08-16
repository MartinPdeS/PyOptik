try:
    from ._version import version as __version__  # noqa: F401

except ImportError:
    __version__ = "0.0.0"

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())


from .material_bank import MaterialBank
from .material_type import MaterialType
from .catalog import MaterialCatalog, MaterialId, MaterialPage

from .material import TabulatedMaterial
from .material import SellmeierMaterial
from .material import base_class

Material = MaterialBank  # For retro-compatibility

TIMEOUT = 10  # Default timeout for requests in seconds
