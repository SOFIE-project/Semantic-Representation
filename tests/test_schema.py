import jsonschema
import json
import sys
import unittest

sys.path.append(".")  # Adds higher directory to python modules path.

from project import semantic_json_validator


class ValidatorTestClass(unittest.TestCase):

    def test_json_validation_schema(self):
        iot_schema = json.loads(open('project/static/W3C_IoT_ThingDescription_schema.json').read())
        smaug_schema = json.loads(open('project/static/smaug_test_sofie_schema.json').read())
        smaug_obj_invalid = json.loads(open('project/static/smaug_locker_invalid_obj.json').read())
        smaug_obj_invalid_price_low = json.loads(open('project/static/smaug_locker_invalid_price_low.json').read())
        smaug_obj_invalid_price_high = json.loads(open('project/static/smaug_locker_invalid_price_high.json').read())
        smaug_obj_valid = json.loads(open('project/static/smaug_locker_valid_obj.json').read())
        smaug_obj_invalid_volume = json.loads(open('project/static/smaug_locker_invalid_volume.json').read())

        self.assertIsNone(semantic_json_validator.validate_schema(smaug_schema, iot_schema))
        self.assertIsNone(semantic_json_validator.validate_schema(smaug_obj_valid, smaug_schema))
        self.assertRaises(jsonschema.exceptions.ValidationError, semantic_json_validator.validate_schema,
                          smaug_obj_invalid, smaug_schema)
        self.assertRaises(jsonschema.exceptions.ValidationError, semantic_json_validator.validate_schema,
                          smaug_obj_invalid_price_low, smaug_schema)
        self.assertRaises(jsonschema.exceptions.ValidationError, semantic_json_validator.validate_schema,
                          smaug_obj_invalid_price_high, smaug_schema)
        self.assertRaises(jsonschema.exceptions.ValidationError, semantic_json_validator.validate_schema,
                          smaug_obj_invalid_volume, smaug_schema)


# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
