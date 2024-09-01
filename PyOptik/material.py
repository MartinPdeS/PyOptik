from PyOptik.sellmeier_class import SellmeierMaterial
from PyOptik.tabulated_class import TabulatedMaterial



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
    ]

    @staticmethod
    @property
    def silver(self):
        return TabulatedMaterial('silver')

    @staticmethod
    @property
    def gold(self):
        return TabulatedMaterial('gold')

    @staticmethod
    @property
    def aluminium(self):
        return TabulatedMaterial('aluminium')

    @staticmethod
    @property
    def copper(self):
        return TabulatedMaterial('copper')

    @staticmethod
    @property
    def zinc(self):
        return TabulatedMaterial('zinc')

    @staticmethod
    @property
    def iron(self):
        return TabulatedMaterial('iron')

    @staticmethod
    @property
    def argon(self):
        return SellmeierMaterial('argon')

    @staticmethod
    @property
    def water(self):
        return SellmeierMaterial('water')

    @staticmethod
    @property
    def silicon(self):
        return SellmeierMaterial('silicon')

    @staticmethod
    @property
    def BK7(self):
        return SellmeierMaterial('BK7')

    @staticmethod
    @property
    def fused_silica(self):
        return SellmeierMaterial('fused_silica')

    @staticmethod
    @property
    def germanium(self):
        return SellmeierMaterial('germanium')
