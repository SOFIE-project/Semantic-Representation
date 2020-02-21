import unittest

from project import app


class BasicTests(unittest.TestCase):

    # Execute prior to each test
    def setUp(self):
        app.config['DEBUG'] = False

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
