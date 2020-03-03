import json
import sys
import unittest

sys.path.append(".")  # Adds higher directory to python modules path.

from project import semantic_json_validator


class ValidatorTestClass(unittest.TestCase):

    def test_validate_semantic(self):
        pass

    def test_valid_objects(self):
        valid_jsons = json.loads(open('tests/static/default_valid_requests.json').read())
        for x in valid_jsons:
            self.assertEqual(semantic_json_validator.validate_semantic(x), True)

    def test_invalid_objects(self):
        invalid_jsons = json.loads(open('tests/static/default_invalid_requests.json').read())

        for x in invalid_jsons:
            self.assertNotEqual(semantic_json_validator.validate_semantic(x), True)


# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
