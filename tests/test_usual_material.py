import pytest
from PyOptik import UsualMaterial

@pytest.mark.parametrize('material_name', UsualMaterial.all, ids=lambda name: f'Test {name}')
def test_usual_material(material_name):
    """
    Test each usual material defined in UsualMaterial to ensure that it can be instantiated without errors.
    """
    material_instance = getattr(UsualMaterial, material_name)

    assert material_instance is not None, f"{material_name} instantiation failed."

if __name__ == "__main__":
    pytest.main([__file__])
