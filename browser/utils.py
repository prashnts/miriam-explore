import pandas as pd
import os
import json
import yaml

SAMPLE_COLUMNS = [
    'mirna', 'gene', 'host', 'dg', 'exp_gene', 'exp_host',
    'score', 'ont_fnc_x', 'ont_mol_fn_x', 'ont_fnc_y', 'ont_mol_fn_y',
    's_keq', 's_deg', 's_ont',
]

SAMPLE_PATH = os.env['SAMPLE_PICKLES_PATH']


def get_fixture(fixture):
    '''Load a fixture file from fixture dir.

    fixture format is `<app>.<file>.<ext>`. json or yaml are used to load
    the file depending upon the `ext`.
    '''
    app, fname, ext = fixture.split('.')
    file_path = os.path.abspath('./{}/fixtures/{}.{}'.format(app, fname, ext))
    with open(file_path, 'r') as fp:
        if ext == 'json':
            return json.load(fp)
        elif ext == 'yaml':
            return yaml.load(fp)
        raise ValueError('Either json or yaml fixture supported.')


def get_sample(sample_id):
    df = pd.read_pickle(f'{SAMPLE_PATH}/{sample_id}.pkl')
    return df[SAMPLE_COLUMNS]
