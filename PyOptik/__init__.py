try:
    from ._version import version as __version__  # noqa: F401

except ImportError:
    __version__ = "0.0.0"

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())


from .material_type import MaterialType  # noqa: E402
from .catalog import MaterialCatalog, MaterialId, MaterialPage, download_snapshot  # noqa: E402

from .material import TabulatedMaterial  # noqa: E402
from .material import SellmeierMaterial  # noqa: E402
from .material import (  # noqa: E402
    FormulaDataset, MaterialDocument, MaterialMetadata, TabulatedDataset, parse_material,
)
from .thin_film import (  # noqa: E402
    FresnelResult,
    ThinFilmLayer,
    ThinFilmResult,
    brewster_angle,
    critical_angle,
    fresnel_coefficients,
    thin_film_stack,
)
from .material import base_class  # noqa: E402


TIMEOUT = 10  # Default timeout for requests in seconds
