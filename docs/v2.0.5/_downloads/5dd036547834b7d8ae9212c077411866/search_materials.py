"""
Searching the MaterialBank
==========================

This example shows how to locate materials using patterns with
:func:`~PyOptik.material_bank.MaterialBank.search` and then load a
material for analysis.
"""

# %%
from PyOptik import MaterialBank
from TypedUnit import ureg

# Find materials containing the substring 'si'
materials = MaterialBank.search("si")
print("Matches:")
for name in materials:
    print("-", name)

# Use the first match
material = MaterialBank.get(materials[0])
print("\nRefractive index at 1 µm:")
print(material.compute_refractive_index(1 * ureg.micrometer))
