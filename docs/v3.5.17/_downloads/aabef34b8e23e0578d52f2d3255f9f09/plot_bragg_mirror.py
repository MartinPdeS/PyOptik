"""
Dielectric Bragg mirror
=======================

Build an alternating high/low-index quarter-wave stack and observe how adding
layer pairs increases reflectance around the design wavelength.
"""

# %%
import matplotlib.pyplot as plt
import numpy
from TypedUnit import ureg

from PyOptik import ThinFilmLayer, thin_film_stack


design_wavelength = 800 * ureg.nanometer
high_index, low_index = 2.25, 1.45
wavelengths = numpy.linspace(500, 1100, 700) * ureg.nanometer


def mirror_layers(pair_count):
    """Return ``pair_count`` high/low quarter-wave layer pairs."""
    pair = [
        ThinFilmLayer(high_index, design_wavelength / (4 * high_index)),
        ThinFilmLayer(low_index, design_wavelength / (4 * low_index)),
    ]
    return pair * pair_count


# %%
figure, axis = plt.subplots(layout="constrained")
for pair_count in (2, 4, 8):
    result = thin_film_stack(
        wavelengths,
        mirror_layers(pair_count),
        substrate_index=1.52,
    )
    axis.plot(wavelengths.magnitude, 100 * result.reflectance, label=f"{pair_count} pairs")

axis.axvline(design_wavelength.magnitude, color="black", linestyle="--", alpha=0.6)
axis.set(
    xlabel="Wavelength [nm]",
    ylabel="Reflectance [%]",
    title="Quarter-wave dielectric mirror",
    ylim=(0, 101),
)
axis.grid(alpha=0.25)
axis.legend()
plt.show()
