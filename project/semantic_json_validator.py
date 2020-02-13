import jsonschema
import json
import os

from project import app

def validate_semantic(json_to_validate):
    validation_results = {'validation': True, 'error': None}
    try:
        # First validate against IoT TD general schema
        validate_schema(json_to_validate, app.config['IOT_SCHEMA_PATH'])
        #Second validate against application proprietary schema 
        validate_schema(json_to_validate, app.config['SCHEMA_PATH'])
    except FileNotFoundError:
        validation_results['validation'] = False
        validation_results['error'] = 'schema_not_found'
    except jsonschema.exceptions.ValidationError as schema_error:
        validation_results['validation'] = False
        validation_results['error'] = schema_error 
    return validation_results

def validate_schema(json_to_validate, schema_path):
    try:
        schema = json.loads(open(schema_path).read())
        jsonschema.validate(instance=json_to_validate, schema=schema)
    except (FileNotFoundError, jsonschema.exceptions.ValidationError):
        raise
