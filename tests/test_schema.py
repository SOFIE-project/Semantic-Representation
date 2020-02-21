import jsonschema
import json

from project.semantic_json_validator import validate_schema


def test_json_validation_schema():
    iot_schema = json.loads(open('project/static/W3C_IoT_ThingDescription_schema.json').read())
    smaug_schema = json.loads(open('project/static/smaug_test_sofie_schema.json').read())
    # rovio_schema = json.loads(open('project/static/rovio_test_sofie_schema.json').read())
    # smaug_obj = json.loads(open('project/static/smaug_locker_td.json').read())
    try:
        validate_schema(smaug_schema, iot_schema)
        # semantic_json_validator.validate_schema(smaug_schema, iot_schema)
        # semantic_json_validator.validate_schema(rovio_schema, iot_schema)
    except jsonschema.exceptions.ValidationError as error:
        print(error)


if __name__ == '__main__':
    test_json_validation_schema()
