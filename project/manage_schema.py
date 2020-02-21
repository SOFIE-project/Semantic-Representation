import json
import os

from project import app


def get_schema():
    basedir = os.path.abspath(os.path.dirname(__file__))
    schema_path = os.path.join(basedir, app.config['SCHEMA_PATH'])
    try:
        print('schema path: ', app.config['SCHEMA_PATH'])
        return json.load(open(schema_path, 'r'))
    except FileNotFoundError:
        raise
