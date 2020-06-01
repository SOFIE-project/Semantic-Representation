from pathlib import Path
from project import app
import unittest
import requests
import os
import yaml
import json


class ApplicationTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ApplicationTest, self).__init__(*args, **kwargs)

        ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
        path = Path(ROOT_DIR)
        CONFIG_PATH = os.path.join(path.parent, 'project/config.yaml')
        yaml_config = yaml.load(open(CONFIG_PATH, 'r'), Loader=yaml.FullLoader)
        self.HOST = str(yaml_config['host'])
        self.PORT = str(yaml_config['port'])
        self.schemas = load_schemas()

    def test_add_schema(self):
        url = 'http://' + self.HOST+':'+self.PORT+'/api/v1/add_schema'
        schema = self.schemas['valid']
        payload = json.dumps({'schema_name': 'test1', 'schema': schema})
        #print(payload)
        res = requests.post(url, json=payload)
        print(res.text)


def load_schemas():
    schemas = dict()
    schemas['valid'] = json.loads(open('tests/static/test_schema.json').read())
    return schemas


# runs the unit tests in the module
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'])
    unittest.main()