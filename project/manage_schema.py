import json
import os
import errno


class ManageSchema:

    def __init__(self, custom_schema, standard_schema):
        basedir = os.path.abspath(os.path.dirname(__file__))
        custom_schema_path = os.path.join(basedir, custom_schema)
        standard_schema_path = os.path.join(basedir, standard_schema)
        try:
            self.standard_schema = json.load(open(standard_schema_path, 'r'))
        except FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), standard_schema_path):
            raise
        try:
            self.custom_schema = json.load(open(custom_schema_path, 'r'))
        except FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), custom_schema_path):
            raise

    def get_custom_schema_json(self):
        return self.custom_schema

    def get_standard_schema_json(self):
        return self.standard_schema

    # ToDo
    def set_custom_schema(self):
        pass

    # ToDo
    def set_standard_schema(self):
        pass
