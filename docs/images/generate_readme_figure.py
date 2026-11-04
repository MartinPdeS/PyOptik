"""Generate the README's ideal antireflection coating figure."""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np
from TypedUnit import ureg
from PyOptik import ThinFilmLayer, thin_film_stack

wavelengths = np.linspace(350, 900, 600) * ureg.nanometer
substrate_index = 1.52
coating_index = np.sqrt(substrate_index)
coating = ThinFilmLayer(coating_index, 550 * ureg.nanometer / (4 * coating_index))
bare = thin_film_stack(wavelengths, [], substrate_index=substrate_index)
coated = thin_film_stack(wavelengths, [coating], substrate_index=substrate_index)

figure, (diagram, spectrum) = plt.subplots(1, 2, figsize=(12, 4.5), gridspec_kw={"width_ratios": [1, 1.3]}, layout="constrained")
figure.patch.set_facecolor("#f8fafc")
diagram.set_facecolor("#f8fafc")
diagram.add_patch(Rectangle((0, 0), 1, 0.35, color="#cbd5e1"))
diagram.add_patch(Rectangle((0, 0.35), 1, 0.12, color="#5eead4"))
diagram.text(0.04, 0.19, "GLASS  ·  n = 1.52", color="#334155", fontsize=11, weight="bold")
diagram.text(0.04, 0.40, "QUARTER-WAVE COATING", color="#115e59", fontsize=9, weight="bold", va="center")
diagram.text(0.04, 0.88, "AIR  ·  n = 1.00", color="#475569", fontsize=10, weight="bold")
diagram.add_patch(FancyArrowPatch((0.32, 0.82), (0.52, 0.48), arrowstyle="->", mutation_scale=18, linewidth=2.5, color="#2563eb"))
diagram.add_patch(FancyArrowPatch((0.52, 0.48), (0.72, 0.82), arrowstyle="->", mutation_scale=18, linewidth=2.5, color="#f59e0b"))
diagram.set(xlim=(0, 1), ylim=(0, 1), title="A single optical coating")
diagram.axis("off")
spectrum.plot(wavelengths.magnitude, 100 * bare.reflectance, color="#94a3b8", linewidth=2.5, label="Bare glass")
spectrum.plot(wavelengths.magnitude, 100 * coated.reflectance, color="#0f766e", linewidth=3, label="Coated glass")
spectrum.axvline(550, color="#64748b", linestyle="--", linewidth=1)
spectrum.annotate("Design wavelength\n550 nm", xy=(550, 0), xytext=(600, 0.9), color="#334155", arrowprops={"arrowstyle": "->", "color": "#64748b"})
spectrum.set(xlabel="Vacuum wavelength [nm]", ylabel="Reflectance [%]", title="Less reflection at the design wavelength", ylim=(0, 5))
spectrum.grid(alpha=0.18)
spectrum.legend(frameon=False)
figure.savefig(Path(__file__).with_name("readme_coating.png"), dpi=160, facecolor=figure.get_facecolor())
