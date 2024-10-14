try:
    from ._version import version as __version__  # noqa: F401

except ImportError:
    __version__ = "0.0.0"


from .utils import build_default_library
from .material_bank import _MaterialBank
from .material import TabulatedMaterial
from .material import SellmeierMaterial
from .material import base_class

MaterialBank = Material = _MaterialBank()