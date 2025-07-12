try:
    from ._version import version as __version__  # noqa: F401

except ImportError:
    __version__ = "0.0.0"


from .material_bank import MaterialBank
from .material_type import MaterialType

from .material import TabulatedMaterial
from .material import SellmeierMaterial
from .material import base_class

Material = MaterialBank  # For retro-compatiibility

TIMEOUT = 10 # Default timeout for requests in seconds