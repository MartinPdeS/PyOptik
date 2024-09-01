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

    @property
    def silver(self):
        return TabulatedMaterial('silver')

    @property
    def gold(self):
        return TabulatedMaterial('gold')

    @property
    def aluminium(self):
        return TabulatedMaterial('aluminium')

    @property
    def copper(self):
        return TabulatedMaterial('copper')

    @property
    def zinc(self):
        return TabulatedMaterial('zinc')

    @property
    def iron(self):
        return TabulatedMaterial('iron')

    @property
    def argon(self):
        return SellmeierMaterial('argon')

    @property
    def water(self):
        return SellmeierMaterial('water')

    @property
    def silicon(self):
        return SellmeierMaterial('silicon')

    @property
    def BK7(self):
        return SellmeierMaterial('BK7')

    @property
    def fused_silica(self):
        return SellmeierMaterial('fused_silica')

    @property
    def germanium(self):
        return SellmeierMaterial('germanium')
