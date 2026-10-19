"""
Search materials and inspect provenance
=======================================

Find locally available BK7 datasets, inspect their canonical identities, and
compare representative glass pages at a standard wavelength.
"""

# %%
import matplotlib.pyplot as plt
from TypedUnit import ureg

from PyOptik import MaterialCatalog


catalog = MaterialCatalog.from_snapshot()
matches = catalog.search("BK7", shelf="specs", available=True)

print(f"Found {len(matches)} cached BK7 pages")
for page in matches[:5]:
    print(page.id.key, "—", page.description)

# %%
# Canonical IDs make source selection explicit and reproducible.
identifiers = [
    "specs/SCHOTT-optical/N-BK7",
    "specs/OHARA-optical/S-BSL7",
]
wavelength = 587.6 * ureg.nanometer
labels, indices = [], []

for identifier in identifiers:
    page = catalog.get(identifier)
    material = page.load()
    labels.append(page.id.page)
    indices.append(float(material.n(wavelength, out_of_range="raise")))
    print(material.provenance)

# %%
figure, axis = plt.subplots(figsize=(6, 3.5), layout="constrained")
axis.bar(labels, indices, color=["tab:blue", "tab:orange"])
axis.set(
    ylabel="Refractive index at 587.6 nm",
    title="Catalog-backed glass comparison",
    ylim=(1.50, 1.54),
)
axis.grid(axis="y", alpha=0.25)
plt.show()
