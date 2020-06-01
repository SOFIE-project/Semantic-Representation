# !/usr/bin/env python
import sys
import unittest
import json
import requests
sys.path.append(".")
from project import create_app, db
from project.models import Schema
from config import Config


# ToDo refactor to be shared with test_run
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = '5000'


class SchemaModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.schemas = {
            'schema1': {
                'name': 'test1',
                'schema': json.loads(open('tests/static/test_schema.json').read())
                },
            'schema2': {
                'name': 'test2',
                'schema': json.loads(open('tests/static/test_schema2.json').read())
                }
        }
        self.valid_msg = json.loads(open('tests/static/default_valid_requests.json').read())
        self.invalid_msg = json.loads(open('tests/static/default_invalid_requests.json').read())
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_schema(self):
        s1 = Schema(name=self.schemas['schema1']['name'], schema=str(self.schemas['schema1']['schema']))
        db.session.add(s1)
        db.session.commit()
        return True

    def test_api_add_schema(self):
        data = {'name': self.schemas['schema1']['name'], 'schema': self.schemas['schema1']['schema']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/add_schema'

        response_ok = requests.post(url, json=data)
        response_already_existent = requests.post(url, json=data)
        response_data_empty = requests.post(url, json={})

        self.assertEqual(response_ok.status_code, 200)
        self.assertEqual(json.loads(response_ok.text)['schema'],
                         str(data['schema']))
        self.assertEqual(response_already_existent.status_code, 400)
        self.assertEqual(json.loads(response_already_existent.text),
                         json.loads('{ "error": "Bad Request", "message": "schema name already saved"}'))
        self.assertEqual(response_data_empty.status_code, 400)
        self.assertEqual(json.loads(response_data_empty.text),
                         json.loads('{ "error": "Bad Request", "message": "must include schema and schema name"}'))

        # Remove entry
        data = {'name': self.schemas['schema1']['name']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/remove_schema'
        remove_entry = requests.post(url, json=data)

    def test_api_update_schema(self):
        # Add entry
        data = {'name': self.schemas['schema1']['name'], 'schema': self.schemas['schema1']['schema']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/add_schema'

        add_entry = requests.post(url, json=data)

        # Update schema
        data = {'name': self.schemas['schema1']['name'], 'schema': self.schemas['schema2']['schema']}
        data2 = {'name': 'not_found', 'schema': self.schemas['schema2']['schema']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/update_schema'

        response_ok = requests.post(url, json=data)
        response_not_found = requests.post(url, json=data2)
        response_data_empty = requests.post(url, json={})

        self.assertEqual(response_ok.status_code, 200)
        self.assertEqual(json.loads(response_ok.text)['schema'],
                         str(data['schema']))
        self.assertEqual(json.loads(response_not_found.text),
                         json.loads('{ "error": "Bad Request", "message": "schema not found"}'))
        self.assertEqual(response_data_empty.status_code, 400)
        self.assertEqual(json.loads(response_data_empty.text),
                         json.loads('{ "error": "Bad Request", "message": "must include schema and schema name"}'))

        # Remove entry
        data = {'name': self.schemas['schema1']['name']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/remove_schema'
        remove_entry = requests.post(url, json=data)

    def test_api_remove_schema(self):
        # Add entry
        data = {'name': self.schemas['schema1']['name'], 'schema': self.schemas['schema1']['schema']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/add_schema'

        add_entry = requests.post(url, json=data)

        data = {'name': self.schemas['schema1']['name']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/remove_schema'

        response_ok = requests.post(url, json=data)
        response_not_found = requests.post(url, json=data)
        response_data_empty = requests.post(url, json={})

        self.assertEqual(response_ok.status_code, 200)
        self.assertEqual(json.loads(response_ok.text),
                         json.loads('{"message": "schema removed"}'))
        self.assertEqual(response_not_found.status_code, 400)
        self.assertEqual(json.loads(response_not_found.text),
                         json.loads('{ "error": "Bad Request", "message": "schema not found"}'))
        self.assertEqual(response_data_empty.status_code, 400)
        self.assertEqual(json.loads(response_data_empty.text),
                         json.loads('{ "error": "Bad Request", "message": "must include the schema name"}'))

    def test_api_get_schema(self):
        # Add first entry
        data = {'name': self.schemas['schema1']['name'], 'schema': self.schemas['schema1']['schema']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/add_schema'
        add_entry = requests.post(url, json=data)

        # Add second entry
        data2 = {'name': self.schemas['schema2']['name'], 'schema': self.schemas['schema2']['schema']}
        add_entry = requests.post(url, json=data2)

        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/get_schema'
        data_name = {'name': self.schemas['schema1']['name']}
        data_not_found = {'name': 'not found'}
        data_gete_all = {}

        response_schema_name = requests.post(url, json=data_name)
        response_all_schemas = requests.post(url, json=data_gete_all)
        response_schema_not_found = requests.post(url, json=data_not_found)

        self.assertEqual(response_schema_name.status_code, 200)
        self.assertEqual(json.loads(response_schema_name.text)['name'],
                         data['name'])

        # Remove entries
        data = {'name': self.schemas['schema1']['name']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/remove_schema'
        remove_entry = requests.post(url, json=data)
        data = {'name': self.schemas['schema2']['name']}
        remove_entry = requests.post(url, json=data)

    def test_api_validate(self):
        # Add schema
        data = {'name': self.schemas['schema1']['name'], 'schema': self.schemas['schema1']['schema']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/add_schema'
        add_entry = requests.post(url, json=data)

        # validate
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/validate'
        for msg in self.valid_msg:
            data = {'message': msg, 'schema_name': self.schemas['schema1']['name']}
            response_valid = requests.post(url, json=data)
            self.assertEqual(response_valid.status_code, 200)
            self.assertEqual(json.loads(response_valid.text),
                             json.loads('{"message": "valid"}'))
        for msg in self.invalid_msg:
            data = {'message': msg, 'schema_name': self.schemas['schema1']['name']}
            response_valid = requests.post(url, json=data)
            self.assertEqual(response_valid.status_code, 400)
            self.assertEqual(json.loads(response_valid.text)['message'],
                             'not valid')

        # Remove entries
        data = {'name': self.schemas['schema1']['name']}
        url = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT'] + '/api/remove_schema'
        remove_entry = requests.post(url, json=data)


if __name__ == '__main__':
    unittest.main(verbosity=2)