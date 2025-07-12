from typing import Optional
import pint

ureg = pint.UnitRegistry()
pint.set_application_registry(ureg)

# Define a list of base units to scale
BASE_UNITS = [
    'meter'
]

# Define prefixes for scaling units
SCALES = ['nano', 'micro', 'milli', '', 'kilo', 'mega']


def initialize_registry(ureg: Optional[pint.UnitRegistry] = None) -> None:
    """Initialise the unit registry used by :mod:`PyOptik`.

    Parameters
    ----------
    ureg : Optional[pint.UnitRegistry], optional
        A preconfigured :class:`~pint.UnitRegistry` instance. When ``None`` (the
        default) a new registry is created and configured.

    Notes
    -----
    The registry is configured for matplotlib integration and a number of unit
    shortcuts (``nano``/``micro``/``milli``/... ``meter``) as well as commonly
    used units are leaked into the module's global namespace for convenience.
    """

    # If no unit registry is provided, use the default
    ureg = ureg or pint.UnitRegistry()

    # Set up matplotlib integration and unit formatting
    ureg.setup_matplotlib()
    ureg.formatter.default_format = '~P'  # Compact format without units like 'meter'

    # Leak scaled units into the global namespace
    for unit in BASE_UNITS:
        for scale in SCALES:
            scaled_unit_name = scale + unit
            globals()[scaled_unit_name] = getattr(ureg, scaled_unit_name)

    # Leak commonly used specific units into the global namespace
    common_units = {
        'RIU': ureg.refractive_index_unit,
        'refractive_index_unit': ureg.refractive_index_unit,
        'AU': ureg.dimensionless,
        'distance': ureg.meter.dimensionality,
        'Quantity': ureg.Quantity
    }

    # Leak the common units into the global namespace
    globals().update(common_units)

    globals()['ureg'] = ureg


initialize_registry(ureg)
