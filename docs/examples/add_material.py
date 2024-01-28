"""
Add hoc docstring
=================

"""

from PyOptik import DataBank
from PyOptik.ExpData import SaveData

print(DataBank())

url = 'https://refractiveindex.info/data_csv.php?datafile=data/main/Si/Aspnes.yml'

SaveData(name='SI', url=url)

print(DataBank())
