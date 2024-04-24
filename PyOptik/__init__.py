from PyOptik.experiment_material import DataMeasurement
from PyOptik.sellmeier_material import Sellmeier


class UsualMaterial:
    BK7 = Sellmeier('BK7')
    FusedSilica = Sellmeier('silica')
    SodaLimeGlass = DataMeasurement('sodalimeglass')
    Silver = DataMeasurement('silver')
    Gold = DataMeasurement('gold')
    Aluminium = DataMeasurement('aluminium')
    SI = Sellmeier('silica')
    SIO2 = DataMeasurement('sio2')
    TIO2 = DataMeasurement('tio2')
    Polystyrene = DataMeasurement('polystyrene')
    Water = DataMeasurement('water')
    Ethanol = DataMeasurement('ethanol')

# -
