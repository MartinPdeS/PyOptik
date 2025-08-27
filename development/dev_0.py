import numpy
from PyOptik import MaterialBank
MaterialBank.build_library('classics', remove_previous=True)
# MaterialBank.print_available()  # <- this will provide a table of Tabulated and Sellmeier materials name (usually metals are tabulated)
# material = MaterialBank.gold  # <- this should be a TabulatedMaterial instance

# wavelength = numpy.linspace(300e-9, 500e-9, 100)

# ri = material.compute_refractive_index(wavelength)
