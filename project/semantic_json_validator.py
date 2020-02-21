import jsonschema
import json
import os

from project import app

def validate_semantic(json_to_validate):
    validation_results = {'validation': True, 'error': None}
    try:
        iot_schema = json.loads(open(app.config['IOT_SCHEMA_PATH']).read())
        validate_schema(json_to_validate, iot_schema)
    except FileNotFoundError:
        validation_results['validation'] = False
        validation_results['error'] = 'schema_not_found'
    except (jsonschema.exceptions.SchemaError, jsonschema.exceptions.ValidationError) as validation_error:
        validation_results['validation'] = False
        validation_results['error'] = validation_error 
    return validation_results

def validate_schema(json_to_validate, schema):
    try:
        print('JSON to validate: \n', json_to_validate)
        print('TD schema: \n', schema)
        jsonschema.validate(instance=json_to_validate, schema=schema)
    except (jsonschema.exceptions.SchemaError, jsonschema.exceptions.ValidationError):
        raise
