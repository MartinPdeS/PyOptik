"""
Compare the Refractive Index of BK7 and Fused Silica
====================================================

This example compares two common optical glasses available in
:class:`~PyOptik.catalog.MaterialCatalog`. It computes and plots the
refractive index of BK7 and fused silica over the visible to near
infrared wavelength range.
"""

# %%
import numpy
import matplotlib.pyplot as plt
from MPSPlots.styles import mps
from TypedUnit import ureg

from PyOptik import MaterialCatalog


# Retrieve materials
catalog = MaterialCatalog.from_snapshot()
bk7 = catalog.get("specs/SCHOTT-optical/P-BK7").load()
silica = catalog.get("main/SiO2/Malitson").load()

# Prepare wavelength range
wavelengths = numpy.linspace(0.4, 1.6, 300) * ureg.micrometer

n_bk7 = bk7.compute_refractive_index(wavelengths)
n_silica = silica.compute_refractive_index(wavelengths)

# %% Plot comparison
with plt.style.context(mps):
    fig, ax = plt.subplots()

ax.set(
    title="BK7 vs Fused Silica",
    xlabel="Wavelength [µm]",
    ylabel="Refractive index",
)
ax.plot(wavelengths, n_bk7.real, label="BK7")
ax.plot(wavelengths, n_silica.real, label="Fused Silica")
ax.legend()

plt.show()
