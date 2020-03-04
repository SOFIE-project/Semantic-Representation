import jsonschema
import json
import sys
import os


def test_custom_schema_validation():
    head, tail = os.path.split(os.path.abspath(os.path.dirname(__file__)))
    custom_schema_path = os.path.join(head, 'project/custom_schema.json')
    try:
        custom_schema = json.loads(open(custom_schema_path).read())
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    td_schema = json.loads(open(os.path.join(head, 'tests/static/W3C_IoT_ThingDescription_schema.json')).read())

    try:
        jsonschema.validate(custom_schema, td_schema)
    except (jsonschema.exceptions.SchemaError, jsonschema.exceptions.ValidationError) as validation_error:
        print(validation_error)
        sys.exit(1)
    print("The schema IS VALID")


if __name__ == '__main__':
    test_custom_schema_validation()
