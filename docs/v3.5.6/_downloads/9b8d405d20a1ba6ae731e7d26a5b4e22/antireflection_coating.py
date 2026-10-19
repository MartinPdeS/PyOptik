import matplotlib.pyplot as plt
import numpy as np
from TypedUnit import ureg
from PyOptik import ThinFilmLayer, thin_film_stack

# Ideal, lossless materials at normal incidence; no catalog download needed.
design_wavelength = 550 * ureg.nanometer
substrate_index = 1.52
coating_index = np.sqrt(substrate_index)
coating_thickness = design_wavelength / (4 * coating_index)
wavelengths = np.linspace(350, 900, 600) * ureg.nanometer

uncoated = thin_film_stack(wavelengths, [], substrate_index=substrate_index)
coated = thin_film_stack(
    wavelengths,
    [ThinFilmLayer(coating_index, coating_thickness)],
    substrate_index=substrate_index,
)

figure, axis = plt.subplots(figsize=(7, 4), layout="constrained")
axis.plot(wavelengths.magnitude, 100 * uncoated.reflectance, label="Uncoated glass")
axis.plot(wavelengths.magnitude, 100 * coated.reflectance, label="Quarter-wave coating")
axis.axvline(design_wavelength.magnitude, color="black", linestyle="--", alpha=0.6)
axis.set(xlabel="Vacuum wavelength [nm]", ylabel="Reflectance [%]",
         title="Reduce glass reflection with a quarter-wave coating")
axis.grid(alpha=0.25)
axis.legend()

print(f"Ideal coating index: {coating_index:.3f}")
print(f"Coating thickness: {coating_thickness.to(ureg.nanometer):.1f}")
plt.show()
