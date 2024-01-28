"""
Add hoc docstring
=================

"""

from PyOptik import DataBank, ExpData

print(DataBank())

dat = ExpData('BK7')

dat.GetRI([5e-7])

