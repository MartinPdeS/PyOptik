from .base_class import BaseMaterial
from .sellmeier_class import SellmeierMaterial
from .tabulated_class import TabulatedMaterial
from .dataset import FormulaDataset, MaterialDocument, MaterialMetadata, TabulatedDataset, parse_material

# Preserve the existing material package and dotted imports while making the
# beginner-facing `from PyOptik import material` shortcut callable.
import sys as _sys
from types import ModuleType as _ModuleType


class _MaterialModule(_ModuleType):
    """The material package with a convenience loader as its call interface."""

    def __call__(
        self, name, *, source=None, catalog=None, data_root=None, interpolation="linear",
        use_default=True,
    ):
        """Load a material; see :func:`PyOptik.load_material` for selection rules."""
        from PyOptik.discovery import load_material

        return load_material(
            name, source=source, catalog=catalog, data_root=data_root,
            interpolation=interpolation, use_default=use_default,
        )


_sys.modules[__name__].__class__ = _MaterialModule
