import os
import json

from project import app

def get_schema():
    # basedir = os.path.abspath(os.path.dirname(__file__))
    #schema_path = os.path.join(basedir, app.config['SCHEMA_PATH'])
    try:
        return json.load(open(app.config['SCHEMA_PATH'], 'r'))
    except FileNotFoundError:
        raise