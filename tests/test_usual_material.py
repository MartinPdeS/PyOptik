import pytest
from PyOptik import UsualMaterial
from PyOptik.material import SellmeierMaterial, TabulatedMaterial

@pytest.mark.parametrize('material_name', UsualMaterial.all_materials, ids=lambda name: f'Test {name}')
def test_usual_material(material_name):
    """
    Test each usual material defined in UsualMaterial to ensure that it can be instantiated without errors.
    """
    material_instance = getattr(UsualMaterial, material_name)

    assert isinstance(material_instance, (SellmeierMaterial, TabulatedMaterial)), f"{material_name} instantiation failed."

@pytest.mark.parametrize('material_name', UsualMaterial.all_materials, ids=lambda name: f'Test {name}')
def test_get_material(material_name):
    """
    Test each usual material defined in UsualMaterial to ensure that it can be instantiated without errors.
    """
    material_instance = UsualMaterial.get('silver')

    assert isinstance(material_instance, TabulatedMaterial), f"{material_name} instantiation failed."


if __name__ == "__main__":
    pytest.main([__file__])
