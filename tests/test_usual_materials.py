import pytest
from PyOptik import MaterialBank
from PyOptik.material import SellmeierMaterial, TabulatedMaterial

# MaterialBank.build_library('minimal', remove_previous=True)
MaterialBank.set_filter(use_sellmeier=True, use_tabulated=True)


@pytest.mark.parametrize('material_name', MaterialBank.all, ids=lambda name: f'{name}')
def test_usual_material(material_name):
    """
    Test each usual material defined in UsualMaterial to ensure that it can be instantiated without errors.
    """
    material_instance = getattr(MaterialBank, material_name)

    MaterialBank.print_available()

    assert isinstance(material_instance, (SellmeierMaterial, TabulatedMaterial)), f"{material_name} instantiation failed."

    assert getattr(MaterialBank, material_name) == MaterialBank.get(material_name), 'Both __getattr__ and get() method should return the same Material instance.'


def tests_material_api():
    material_0 = MaterialBank.zinc
    material_1 = MaterialBank.water
    material_2 = MaterialBank.silicon

    assert material_0 != material_1, "Two different material [Tabulated vs Sellmeier] are evaluated as equal"
    assert material_2 != material_1, "Two different material [Sellmeier vs Sellmeier] are evaluated as equal"


def test_material_bank_filter():
    MaterialBank.set_filter(use_sellmeier=True, use_tabulated=False)

    MaterialBank.print_available()

    MaterialBank.set_filter(use_sellmeier=False, use_tabulated=True)

    MaterialBank.print_available()

    MaterialBank.set_filter(use_sellmeier=True, use_tabulated=True)


def test_fail_wrong_clean():
    with pytest.raises(ValueError):
        MaterialBank.clean_data_files(regex='test*', save_location='invalid')


if __name__ == "__main__":
    pytest.main(["-W error", "-s", __file__])

