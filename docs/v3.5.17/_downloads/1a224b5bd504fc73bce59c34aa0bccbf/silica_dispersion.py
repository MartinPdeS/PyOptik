import matplotlib.pyplot as plt
import numpy as np
from TypedUnit import ureg
from PyOptik import material

# First run downloads the material snapshot; subsequent runs reuse it.
silica = material("fused silica")  # Documented default: main/SiO2/Malitson
wavelengths = np.linspace(500, 1600, 300) * ureg.nanometer
length = 1 * ureg.millimeter

phase_index = silica.n(wavelengths, out_of_range="raise")
group_index = silica.compute_group_index(wavelengths)
gdd = silica.compute_group_delay_dispersion(wavelengths, length=length)

figure, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
axes[0].plot(wavelengths.magnitude, phase_index, label="Phase index n")
axes[0].plot(wavelengths.magnitude, group_index, label="Group index n_g")
axes[0].set(xlabel="Vacuum wavelength [nm]", ylabel="Refractive index",
            title="Fused silica: phase and group index")
axes[0].legend()
axes[1].plot(wavelengths.magnitude, gdd.to(ureg.femtosecond**2).magnitude)
axes[1].axhline(0, color="black", linewidth=0.8)
axes[1].set(xlabel="Vacuum wavelength [nm]", ylabel="GDD [fs²]",
            title="Dispersion through 1 mm of fused silica")
for axis in axes:
    axis.grid(alpha=0.25)

sample = 800 * ureg.nanometer
print(f"Group index at 800 nm: {silica.compute_group_index(sample):.4f}")
print(f"GDD at 800 nm through 1 mm: "
      f"{silica.compute_group_delay_dispersion(sample, length=length).to(ureg.femtosecond**2):.2f}")
plt.show()
