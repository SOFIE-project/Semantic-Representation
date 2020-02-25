import jsonschema
import json

from project import app


def validate_semantic(obj_to_validate):
    try:
        json_to_validate = json.loads(json.dumps(obj_to_validate))
        validate_schema(json_to_validate, app.schema)
    except (jsonschema.exceptions.SchemaError, jsonschema.exceptions.ValidationError) as validation_error:
        return json.loads(json.dumps({'message': validation_error.message, 'schema': validation_error.schema}))
    return True


def validate_schema(json_to_validate, schema):
    jsonschema.validate(instance=json_to_validate, schema=schema)

