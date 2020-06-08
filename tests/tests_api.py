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


class SemanticRepresentationAPI(unittest.TestCase):

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
        with open(os.path.join(staticdir + 'schema_extension.json')) as file:
            self.schema_extension = json.loads(file.read())
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    '''
    The function add a schema into the SR component's DBs and tests if the schema is inserted correctly
    '''
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

    '''
    This function test the schema extension functionality. 
    
    The db is populated with a schema, then the test add a schema extension that refers to it and everything is expected
     to work.
    Then, the test tries to add a schema extension to a schema that does not exist in the db and the component is expect
    to notify that the schema to be extended does not exist
    '''
    def test_api_add_extension(self):
        url = self.baseurl + '/api/add_schema'

        # Add schema to be extended
        schema_name = self.schemas[0]['$id']
        extended_schema = self.schemas[0]
        data = {'name': schema_name, 'schema': extended_schema}
        requests.post(url, json=data)

        # Add valid schema extension
        data = {'name': self.schema_extension['$id'], 'schema': self.schema_extension, 'extended': schema_name}
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text)['name'],
                         self.schema_extension['$id'])
        self.assertEqual(json.loads(response.text)['schema'],
                         str(self.schema_extension))

        # Add a not valid schema extension
        data = {'name': 'new schema extension', 'schema': self.schema_extension, 'extended': 'I dont exist'}
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.text)['message'],
                         'Extended schema not in the DB')

        # Clean the db for other tests
        url = self.baseurl + '/api/remove_schema'
        data = {'name': schema_name}
        requests.post(url, json=data)
        data = {'name': self.schema_extension['$id']}
        requests.post(url, json=data)

    '''
    This function test the update schema functionality of the SR component. First a schema is added, then its updated 
    dynamically with a new schema version 
    '''
    def test_api_update_schema(self):
        # Add entry
        data = {'name': self.schemas[0]['$id'], 'schema': self.schemas[0]}
        url = self.baseurl + '/api/add_schema'

        requests.post(url, json=data)

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
        requests.post(url, json=data)

    '''
    This function tests the remove schema functionality of the SR component. A schema is added to the SR component's DB 
    then removed
    '''
    def test_api_remove_schema(self):
        # Add entry
        data = {'name': self.schemas[0]['$id'], 'schema': self.schemas[0]}
        url = self.baseurl + '/api/add_schema'

        requests.post(url, json=data)

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

    '''
        This function tests SR component post functionality.
        A schema is added to the component's db, the this schema is retrieved with a post request
    '''
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

    '''
    This function tests SR component get functionality.
    A schema is added to the component's db, then this schema is retrieved with a get request using its URL 
    '''
    def test_api_get_get_schema(self):
        # Add first entry
        data = {'name': self.schemas[0]['$id'], 'schema': self.schemas[0]}
        url = self.baseurl + '/api/add_schema'
        requests.post(url, json=data)

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

    '''
    This test shows the message validation functionality of the SR component.
    First is added the schema to validate the messages against.
    A set of valid messages are validated against that 
    schema and the component informs that the messages are validated
    Then, a set of invalid messages are validated against the schema, in this case the component informs that 
    the messages are not valid and why they are not valid. 
    '''
    def test_api_validate(self):
        # Add schema
        data = {'name': self.schemas[0]['$id'], 'schema': self.schemas[0]}
        url = self.baseurl + '/api/add_schema'
        requests.post(url, json=data)

        # Validate valid msg
        url = self.baseurl + '/api/validate'
        for msg in self.valid_msg:
            data = {'message': msg, 'schema_name': self.schemas[0]['$id']}
            response_valid = requests.post(url, json=data)
            self.assertEqual(response_valid.status_code, 200)
            self.assertEqual(json.loads(response_valid.text),
                             json.loads('{"message": "valid"}'))
        # Validate not valid msg
        for msg in self.invalid_msg:
            data = {'message': msg, 'schema_name': self.schemas[0]['$id']}
            response_valid = requests.post(url, json=data)
            self.assertEqual(response_valid.status_code, 400)

        # Clear DB for the next tests
        remove_schemas(self.baseurl + '/api/remove_schema', self.schemas)

    '''
    This test shows how validation works on extended schemas. 
    A message is valid if its semantic defines the mandatory fields of the schema and if the values of all fields 
    (mandatory and not) are correct. If a message contains fields that are not defined in the schema, the message is valid.
    
    First, a valid messaged is validated against a schema extension and the extended schema, expecting valid results
    
    Second, a message is validated against a schema and its proven valid. The same message is validated against the 
    extended schema and its proven not valid. This because the message contains a field that is not correct, is not
     defined in the original schema, but is defined in its extension.
     
    A message to be proven valid against a schema extension must be valid for the original schema first. 
    '''
    def test_api_extended_validation(self):
        # Add schema
        schema_name = self.schemas[0]['$id']
        data = {'name': schema_name, 'schema': self.schemas[0]}
        url = self.baseurl + '/api/add_schema'
        requests.post(url, json=data)

        # Add valid schema extension
        data = {'name': self.schema_extension['$id'], 'schema': self.schema_extension, 'extended': schema_name}
        requests.post(url, json=data)

        url = self.baseurl + '/api/validate'

        # Validate the valid message
        extension_mgs = json.loads(json.dumps({"lockerId": 1234, "price": 35, "volume": 15, "extended": 2}))
        data = {'message': extension_mgs, 'schema_name': self.schema_extension['$id']}
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text),
                         json.loads('{"message": "valid"}'))

        # Invalid message for the extended schema (volume is required in the extended schema, not in the extension)
        extension_mgs = json.loads(json.dumps({"lockerId": 1234, "price": 35, "extended": 2}))
        data = {'message': extension_mgs, 'schema_name': self.schema_extension['$id']}
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.text)['message'],
                         "not valid, 'volume' is a required property")

        # Invalid message for the schema extension (extension is required in the schema extension, not in the extended schema)
        extension_mgs = json.loads(json.dumps({"lockerId": 1234, "price": 35, "volume": 15}))
        data = {'message': extension_mgs, 'schema_name': self.schema_extension['$id']}
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.text)['message'],
                         "not valid, 'extended' is a required property")

        # Clear db for the next tests
        url = self.baseurl + '/api/remove_schema'
        data = {'name': self.schemas[0]['$id']}
        requests.post(url, json=data)
        data = {'name': self.schema_extension['$id']}
        requests.post(url, json=data)


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