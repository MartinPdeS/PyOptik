import pytest
from PyOptik import MaterialBank
from PyOptik.material import SellmeierMaterial, TabulatedMaterial

@pytest.mark.parametrize('material_name', MaterialBank.all, ids=lambda name: f'{name}')
def test_usual_material(material_name):
    """
    Test each usual material defined in UsualMaterial to ensure that it can be instantiated without errors.
    """
    material_instance = getattr(MaterialBank, material_name)

    assert isinstance(material_instance, (SellmeierMaterial, TabulatedMaterial)), f"{material_name} instantiation failed."


if __name__ == "__main__":
    pytest.main(["-W error", __file__])
