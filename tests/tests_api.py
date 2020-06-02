# !/usr/bin/env python
from project import create_app, db
from config import TestConfig
import sys
import os
import unittest
import json
import requests
sys.path.append(".")


basedir = os.path.abspath(os.path.dirname(__file__))
staticdir = os.path.join(basedir, 'static/')


class SchemaModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.baseurl = 'http://' + self.app.config['HOST'] + ':' + self.app.config['PORT']
        self.app_context = self.app.app_context()
        self.app_context.push()
        with open(os.path.join(staticdir + 'test_schema.json')) as file:
            self.schemas = json.loads(file.read())
        with open(os.path.join(staticdir + 'valid_msg.json')) as file:
            self.valid_msg = json.loads(file.read())
        with open(os.path.join(staticdir + 'invalid_msg.json')) as file:
            self.invalid_msg = json.loads(file.read())
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_api_add_schema(self):
        schema1 = {'name': self.schemas[0]['$id'], 'schema': self.schemas[0]}
        url = self.baseurl + '/api/add_schema'

        response_ok = requests.post(url, json=schema1)
        response_already_existent = requests.post(url, json=schema1)
        response_data_empty = requests.post(url, json={})

        self.assertEqual(response_ok.status_code, 200)
        self.assertEqual(json.loads(response_ok.text)['schema'],
                         str(schema1['schema']))
        self.assertEqual(response_already_existent.status_code, 400)
        self.assertEqual(json.loads(response_already_existent.text),
                         json.loads('{ "error": "Bad Request", "message": "schema name already saved"}'))
        self.assertEqual(response_data_empty.status_code, 400)
        self.assertEqual(json.loads(response_data_empty.text),
                         json.loads('{ "error": "Bad Request", "message": "must include schema and schema name"}'))

        # Remove entry
        data = {'name': self.schemas[0]['$id']}
        url = self.baseurl + '/api/remove_schema'
        remove_entry = requests.post(url, json=data)

    def test_api_update_schema(self):
        # Add entry
        data = {'name': self.schemas[0]['$id'], 'schema': self.schemas[0]}
        url = self.baseurl + '/api/add_schema'

        add_entry = requests.post(url, json=data)

        # Update schema
        data = {'name': self.schemas[0]['$id'], 'schema': self.schemas[1]}
        data2 = {'name': 'not_found', 'schema': self.schemas[1]}
        url = self.baseurl + '/api/update_schema'

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
        data = {'name': self.schemas[0]['$id']}
        url = self.baseurl + '/api/remove_schema'
        remove_entry = requests.post(url, json=data)

    def test_api_remove_schema(self):
        # Add entry
        data = {'name': self.schemas[0]['$id'], 'schema': self.schemas[0]}
        url = self.baseurl + '/api/add_schema'

        add_entry = requests.post(url, json=data)

        data = {'name': self.schemas[0]['$id']}
        url = self.baseurl + '/api/remove_schema'

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

    def test_api_post_get_schema(self):
        add_schemas(self.baseurl + '/api/add_schema', self.schemas)
        url = self.baseurl + '/api/get_schema'

        for schema in self.schemas:
            response = requests.post(url, json={'name': schema['$id']})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.text)['name'],
                             schema['$id'])
        response = requests.post(url, json={'name': 'not found'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.text),
                         json.loads(json.dumps({'error': 'Bad Request', 'message': 'schema not found'})))

        remove_schemas(self.baseurl + '/api/remove_schema', self.schemas)

    def test_api_get_get_schema(self):
        # Add first entry
        data = {'name': self.schemas[0]['$id'], 'schema': self.schemas[0]}
        url = self.baseurl + '/api/add_schema'
        add_entry = requests.post(url, json=data)

        # Add second entry
        data2 = {'name': self.schemas[1]['$id'], 'schema': self.schemas[1]}
        add_entry = requests.post(url, json=data2)

        url = self.baseurl + '/api/get_schema/1'
        url2 = self.baseurl + '/api/get_schema/2'
        url_not_found = self.baseurl + '/api/get_schema/3'
        response_schema1 = requests.get(url)
        response_schema2 = requests.get(url2)
        response_schema_not_found = requests.get(url_not_found)
        self.assertEqual(json.loads(response_schema1.text),
                         str(self.schemas[0]))
        self.assertEqual(json.loads(response_schema2.text),
                         str(self.schemas[1]))
        self.assertEqual(json.loads(response_schema_not_found.text),
                         json.loads('{"error": "Not Found"}'))

        remove_schemas(self.baseurl + '/api/remove_schema', self.schemas)

    def test_api_validate(self):
        # Add schema
        data = {'name': self.schemas[0]['$id'], 'schema': self.schemas[0]}
        url = self.baseurl + '/api/add_schema'
        add_entry = requests.post(url, json=data)

        # validate
        url = self.baseurl + '/api/validate'
        for msg in self.valid_msg:
            data = {'message': msg, 'schema_name': self.schemas[0]['$id']}
            response_valid = requests.post(url, json=data)
            self.assertEqual(response_valid.status_code, 200)
            self.assertEqual(json.loads(response_valid.text),
                             json.loads('{"message": "valid"}'))
        for msg in self.invalid_msg:
            data = {'message': msg, 'schema_name': self.schemas[0]['$id']}
            response_valid = requests.post(url, json=data)
            self.assertEqual(response_valid.status_code, 400)

        remove_schemas(self.baseurl + '/api/remove_schema', self.schemas)


def add_schemas(url, schemas):
    for schema in schemas:
        data = {'name': schema['$id'], 'schema': schemas}
        requests.post(url, json=data)


def remove_schemas(url, schemas):
    for schema in schemas:
        data = {'name': schema['$id']}
        requests.post(url, json=data)


if __name__ == '__main__':
    unittest.main(verbosity=2)