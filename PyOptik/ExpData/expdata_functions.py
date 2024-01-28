import json
import os
import pandas as pd
import numpy as np
from os.path import join

from PyOptik.directories import *


def LoadOnline(url):
    """Loads the data from RefractiveIndex.INFO and returns it as a
    dictionary.

    Arguments:
    url -- link to the csv file from RefractiveIndex.INFO
    """
    df = pd.read_csv(url)
    df = df.to_numpy()

    if ['wl', 'k'] in df:
        index = int(np.where(df == 'wl')[0])
        df = np.delete(df, index, axis=0)

        data = {
            'wl_n': df[:index][:, 0].astype(float),
            'n': df[:index][:, 1].astype(float),
            'wl_k': df[index:][:, 0].astype(float),
            'k': df[index:][:, 1].astype(float)
        }

    else:
        data = {'wl_n': df[:, 0].astype(float),
                'n': df[:, 1].astype(float)}

    return data


def SaveData(url, name, unit=1e-6):
    """Loads the data from RefractiveIndex.INFO and saves it in a json file.

    Arguments:
    url -- link to the csv file from RefractiveIndex.INFO
    name -- name of the material used as the index in the json file
    """
    dict_data = LoadOnline(url)
    directory = join(NPZPath, name)

    if 'k' not in dict_data:
        np.savez(directory,
                 wl_n = dict_data['wl_n'] * unit,
                 n    = dict_data['n'])
    else:
        np.savez(
            directory,
            wl_n=dict_data['wl_n'] * unit,
            n=dict_data['n'],
            wl_k=dict_data['wl_k'] * unit,
            k=dict_data['k'])

    with open(join(DataPath, 'meta_expdata.json'), 'r+') as f:
        meta_expdata=json.load(f)
        meta_expdata['remote_data'][name] = url
        meta_expdata['local_data'][name]  = name + '.npz'
        f.seek(0)
        json.dump(meta_expdata, f, indent=4)


def RemoveData(name):
    """Removes the experimental data stored locally for a given material.

    Arguments:
    name -- name of the material to remove
    """
    with open(join(DataPath, 'meta_expdata.json'), 'r+') as f:
        meta_expdata = json.load(f)
        assert name in meta_expdata['local_data'], "The material you are trying to remove is not in the local data."
        del meta_expdata['remote_data'][name]
        del meta_expdata['local_data'][name]
        
    os.remove(os.path.join(NPZPath, name + '.npz'))

    with open(join(DataPath, 'meta_expdata.json'), 'w') as f:
        json.dump(meta_expdata, f)
