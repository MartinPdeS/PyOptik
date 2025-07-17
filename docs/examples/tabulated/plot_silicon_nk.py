"""
Plot the Refractive Index and Absorption of Silicon
===================================================

This example uses :mod:`PyOptik` to visualise both the real and
imaginary parts of the refractive index of silicon over a typical
infrared wavelength range.
"""

# %%
import numpy
import matplotlib.pyplot as plt
from MPSPlots.styles import mps
from PyOptik import MaterialBank
from PyOptik.units import micrometer

material = MaterialBank.silicon

wavelengths = numpy.linspace(0.3, 1.1, 300) * micrometer
index = material.compute_refractive_index(wavelengths)

# %% Plot n and k
with plt.style.context(mps):
    fig, ax1 = plt.subplots()

ax1.set(
    title="Silicon Refractive Index and Absorption",
    xlabel="Wavelength [µm]",
    ylabel="n",
)
ax1.plot(wavelengths.to(micrometer).magnitude, index.real, label="n", color="tab:blue")
ax1.legend(loc="upper left")

ax2 = ax1.twinx()
ax2.set(ylabel="k")
ax2.plot(wavelengths.to(micrometer).magnitude, index.imag, color="tab:red", label="k")
ax2.legend(loc="upper right")

plt.show()
