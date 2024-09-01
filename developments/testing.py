import numpy as np
from PyOptik import UsualMaterial

# Define wavelength range
wavelengths = np.linspace(0.3e-6, 2.5e-6, 100)

# Retrieve refractive index for BK7 glass
bk7 = UsualMaterial.BK7
n_values = bk7.compute_refractive_index(wavelengths)

# Plot the results
bk7.plot(wavelength_range=wavelengths)