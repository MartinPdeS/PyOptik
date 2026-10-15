"""
Fresnel reflectance versus incidence angle
==========================================

Compare s and p polarization at an air-to-glass interface and identify the
Brewster angle where p-polarized reflection vanishes.
"""

# %%
import matplotlib.pyplot as plt
import numpy
from TypedUnit import ureg

from PyOptik import brewster_angle, fresnel_coefficients


angles = numpy.linspace(0, 89, 500) * ureg.degree
reflectance_s = numpy.array([
    fresnel_coefficients(1.0, 1.5, angle, polarization="s").reflectance
    for angle in angles
])
reflectance_p = numpy.array([
    fresnel_coefficients(1.0, 1.5, angle, polarization="p").reflectance
    for angle in angles
])
brewster = brewster_angle(1.0, 1.5).to(ureg.degree).magnitude

# %%
figure, axis = plt.subplots(layout="constrained")
axis.plot(angles.magnitude, reflectance_s, label="s polarization")
axis.plot(angles.magnitude, reflectance_p, label="p polarization")
axis.axvline(brewster, color="black", linestyle="--", label=f"Brewster: {brewster:.1f}°")
axis.set(
    xlabel="Incidence angle [degree]",
    ylabel="Reflectance",
    title="Air–glass Fresnel reflectance",
    xlim=(0, 90),
    ylim=(0, 1),
)
axis.grid(alpha=0.25)
axis.legend()
plt.show()
