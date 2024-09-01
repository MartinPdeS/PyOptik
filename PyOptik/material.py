from typing import Union
from PyOptik.sellmeier_class import SellmeierMaterial
from PyOptik.tabulated_class import TabulatedMaterial
from PyOptik import data

class staticproperty(property):
  def __get__(self, owner_self, owner_cls):
    return self.fget()

class UsualMaterial:
    all = [
        'silver',
        'gold',
        'aluminium',
        'copper',
        'zinc',
        'iron',
        'argon',
        'water',
        'silicon',
        'BK7',
        'fused_silica',
        'germanium',
        'polystyren'
    ]

    @staticmethod
    def get(material_name: str) -> Union[SellmeierMaterial, TabulatedMaterial]:
        if material_name in data.sellmeier.material_list:
            return SellmeierMaterial(material_name)

        if material_name in data.tabulated.material_list:
            return TabulatedMaterial(material_name)

        raise FileNotFoundError(f'Material: [{material_name}] could not be found.')


    @staticproperty
    def silver():
        return TabulatedMaterial('silver')

    @staticproperty
    def gold():
        return TabulatedMaterial('gold')

    @staticproperty
    def aluminium():
        return TabulatedMaterial('aluminium')

    @staticproperty
    def copper():
        return TabulatedMaterial('copper')

    @staticproperty
    def zinc():
        return TabulatedMaterial('zinc')

    @staticproperty
    def iron():
        return TabulatedMaterial('iron')

    @staticproperty
    def polystyren():
        return SellmeierMaterial('polystyren')

    @staticproperty
    def argon():
        return SellmeierMaterial('argon')

    @staticproperty
    def water():
        return SellmeierMaterial('water')

    @staticproperty
    def silicon():
        return SellmeierMaterial('silicon')

    @staticproperty
    def BK7():
        return SellmeierMaterial('BK7')

    @staticproperty
    def fused_silica():
        return SellmeierMaterial('fused_silica')

    @staticproperty
    def germanium():
        return SellmeierMaterial('germanium')