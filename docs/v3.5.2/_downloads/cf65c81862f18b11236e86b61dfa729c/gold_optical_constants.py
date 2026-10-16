import matplotlib.pyplot as plt
import numpy as np
from TypedUnit import ureg
from PyOptik import material

# Use the documented default and keep the resolved identity visible.
gold = material("gold")  # main/Au/Johnson
print("Resolved source:", gold.catalog_id)
wavelengths = np.linspace(400, 1600, 300) * ureg.nanometer
index = gold.compute_refractive_index(wavelengths, out_of_range="raise")

figure, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
axes[0].plot(wavelengths.magnitude, index.real, color="tab:orange")
axes[0].set(xlabel="Vacuum wavelength [nm]", ylabel="Refractive index n",
            title="Gold: real part of the optical index")
axes[1].plot(wavelengths.magnitude, index.imag, color="tab:purple")
axes[1].set(xlabel="Vacuum wavelength [nm]", ylabel="Extinction coefficient k",
            title="Gold: imaginary part of the optical index")
for axis in axes:
    axis.grid(alpha=0.25)

print("Dataset: main/Au/Johnson (Johnson and Christy)")
print("Optical index at 550 nm:", gold.compute_refractive_index(
    550 * ureg.nanometer, out_of_range="raise"))
plt.show()
