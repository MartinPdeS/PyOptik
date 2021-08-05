from .ExpData import ExpData
from .Sellmeier import Sellmeier
import json


def data_bank():
    with open("pyri/Data/meta_expdata.json", "r") as f:
        expdata = json.load(f)
        material_expdata = []
        for material_e in expdata["local_data"]:
            material_expdata.append(material_e)

    with open("pyri/Data/meta_sellmeier.json", "r") as f:
        sellmeier = json.load(f)
        material_sellmeier = []
        for material_s in sellmeier["sellmeier_formula"]:
            material_sellmeier.append(material_s)
    print(f"Material with experimental data: {material_expdata}")
    print(f"Material with Sellmeier's formula: {material_sellmeier}")
