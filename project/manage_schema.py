import json
import os
import errno


class ManageSchema:

    def __init__(self, custom_schema):
        basedir = os.path.abspath(os.path.dirname(__file__))
        custom_schema_path = os.path.join(basedir, custom_schema)
        try:
            self.custom_schema = json.load(open(custom_schema_path, 'r'))
        except FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), custom_schema_path):
            raise

    def get_custom_schema_json(self):
        return self.custom_schema

