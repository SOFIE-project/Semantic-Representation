import jsonschema
import json
import sys
sys.path.insert(0, '')

from project import semantic_json_validator

def test_json_validation_schema():
    iot_schema = json.loads(open('project/static/W3C_IoT_ThingDescription_schema.json').read())
    smaug_schema = json.loads(open('project/static/smaug_test_sofie_schema.json').read())
    rovio_schema = json.loads(open('project/static/rovio_test_sofie_schema.json').read())
    try:
        #iot_schema_results = semantic_json_validator.validate_schema(iot_schema, 'project/static/W3C_IoT_ThingDescription_schema.json')
        smaug_schema_results = semantic_json_validator.validate_schema(smaug_schema, 'project/static/W3C_IoT_ThingDescription_schema.json')
        rovio_schema_results = semantic_json_validator.validate_schema(rovio_schema, 'project/static/W3C_IoT_ThingDescription_schema.json')
    except jsonschema.exceptions.ValidationError as error:
        print(error)
    #print('iot schema validation: ', iot_schema_results)
    #print('smaug schema validation: ', smaug_schema_results)
    #print('rovio schema validation: ', rovio_schema_results)

if __name__ == '__main__':
    test_json_validation_schema()


    
