import pytest
from PyOptik import MaterialBank
from PyOptik.material import SellmeierMaterial, TabulatedMaterial

MaterialBank.build_library('minimal', remove_previous=True)

@pytest.mark.parametrize('material_name', MaterialBank.all, ids=lambda name: f'{name}')
def test_usual_material(material_name):
    """
    Test each usual material defined in UsualMaterial to ensure that it can be instantiated without errors.
    """
    material_instance = getattr(MaterialBank, material_name)

    MaterialBank.print_materials()

    assert isinstance(material_instance, (SellmeierMaterial, TabulatedMaterial)), f"{material_name} instantiation failed."


def test_fail_wrong_clean():
    with pytest.raises(ValueError):
        MaterialBank.clean_data_files(regex='test*', location='invalid')

if __name__ == "__main__":
    pytest.main(["-W error", __file__])
