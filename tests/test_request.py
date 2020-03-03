import requests
import yaml
import unittest
import json


class FunctionalTestClass(unittest.TestCase):

    def test_valid_requests(self):
        yaml_config = yaml.load(open('tests/static/config.yaml'), Loader=yaml.FullLoader)
        try:
            valid_jsons = json.loads(open('tests/static/custom_valid_requests.json').read())
        except FileNotFoundError:
            valid_jsons = json.loads(open('tests/static/default_valid_requests.json').read())

        url = 'http://'+str(yaml_config['host'])+':'+str(yaml_config['port'])+'/api/v1/validate'

        for x in valid_jsons:
            res = json.loads(requests.post(url, json=x, headers={}).text)
            self.assertEqual("success", res['status'])

    def test_invalid_requests(self):
        yaml_config = yaml.load(open('tests/static/config.yaml'), Loader=yaml.FullLoader)
        try:
            invalid_jsons = json.loads(open('tests/static/custom_invalid_requests.json').read())
        except FileNotFoundError:
            invalid_jsons = json.loads(open('tests/static/default_invalid_requests.json').read())

        url = 'http://'+str(yaml_config['host'])+':'+str(yaml_config['port'])+'/api/v1/validate'

        for x in invalid_jsons:
            res = json.loads(requests.post(url, json=x, headers={}).text)
            self.assertEqual("fail", res['status'])


if __name__ == '__main__':
    unittest.main()
