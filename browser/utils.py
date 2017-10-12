import os
import json
import yaml


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
