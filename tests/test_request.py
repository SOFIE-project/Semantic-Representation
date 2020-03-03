import requests
import yaml
import unittest
import json
import sys

sys.path.append(".")  # Adds higher directory to python modules path.

from project import app


class FunctionalTestClass(unittest.TestCase):

    def test_valid_requests(self):
        try:
            valid_jsons = json.loads(open('tests/static/custom_valid_requests.json').read())
        except FileNotFoundError:
            valid_jsons = json.loads(open('tests/static/default_valid_requests.json').read())

        url = 'http://'+str(app.config['HOST'])+':'+str(app.config['PORT'])+'/api/v1/validate'

        for x in valid_jsons:
            res = json.loads(requests.post(url, json=x, headers={}).text)
            self.assertEqual("success", res['status'])

    def test_invalid_requests(self):
        try:
            invalid_jsons = json.loads(open('tests/static/custom_invalid_requests.json').read())
        except FileNotFoundError:
            invalid_jsons = json.loads(open('tests/static/default_invalid_requests.json').read())

        url = 'http://'+str(app.config['HOST'])+':'+str(app.config['PORT'])+'/api/v1/validate'

        for x in invalid_jsons:
            res = json.loads(requests.post(url, json=x, headers={}).text)
            self.assertEqual("fail", res['status'])


if __name__ == '__main__':
    unittest.main()
