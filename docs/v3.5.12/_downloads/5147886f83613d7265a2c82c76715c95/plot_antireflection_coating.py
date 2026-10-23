"""
Quarter-wave antireflection coating
===================================

Design the ideal single-layer coating for an air-to-glass interface and compare
its spectrum with the uncoated substrate.
"""

# %%
import matplotlib.pyplot as plt
import numpy
from TypedUnit import ureg

from PyOptik import ThinFilmLayer, thin_film_stack


design_wavelength = 550 * ureg.nanometer
substrate_index = 1.52
coating_index = numpy.sqrt(substrate_index)
coating_thickness = design_wavelength / (4 * coating_index)
wavelengths = numpy.linspace(350, 900, 600) * ureg.nanometer

uncoated = thin_film_stack(
    wavelengths,
    [],
    substrate_index=substrate_index,
)
coated = thin_film_stack(
    wavelengths,
    [ThinFilmLayer(coating_index, coating_thickness)],
    substrate_index=substrate_index,
)

# %%
figure, axis = plt.subplots(layout="constrained")
axis.plot(wavelengths.magnitude, 100 * uncoated.reflectance, label="Uncoated glass")
axis.plot(wavelengths.magnitude, 100 * coated.reflectance, label="Quarter-wave coating")
axis.axvline(design_wavelength.magnitude, color="black", linestyle="--", alpha=0.6)
axis.set(
    xlabel="Wavelength [nm]",
    ylabel="Reflectance [%]",
    title="Single-layer antireflection coating",
)
axis.grid(alpha=0.25)
axis.legend()
plt.show()
