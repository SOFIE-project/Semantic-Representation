import os
import json

class Error(object):
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    CONFIG_PATH = os.path.join(ROOT_DIR, 'error_messages.json')
    errors = json.loads(open(CONFIG_PATH).read())