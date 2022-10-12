"""generic docstring"""

from PyOptik  import DataBank, ExpData

from PyOptik.ExpData import SaveData

print(DataBank())

dat = ExpData('BK7')

dat.GetRI([5e-7])

