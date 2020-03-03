import jsonschema
import json

from project import app


def validate_semantic(obj_to_validate):
    try:
        json_to_validate = json.loads(json.dumps(obj_to_validate))
        jsonschema.validate(instance=json_to_validate, schema=app.custom_schema)
    except (jsonschema.exceptions.SchemaError, jsonschema.exceptions.ValidationError) as validation_error:
        return json.loads(json.dumps({'message': validation_error.message, 'schema': validation_error.schema}))
    return True



