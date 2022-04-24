import unittest

from common.validators import validate_schema_details
from server.servers import serverSchema


class TestJSONValidation(unittest.TestCase):
    '''
    Test JSON validation with server list
    '''

    def test_valid_json(self):
        valid_json = {
            "servers": [
                {"server": "first",
                    "address": "127.0.0.1:5000",
                    "poll_period": 60,
                    "regex": "Weight"
                 },
                {"server": "fourth",
                    "address": "127.0.0.1:5000",
                    "poll_period": 120,
                    "regex": ""
                 }
            ]
        }
        returnvalue = validate_schema_details(valid_json, serverSchema)

        self.assertEqual(returnvalue, True)

    def test_empty_json(self):
        empty_json = {
        }
        validate_schema_details(empty_json, serverSchema)

        self.assertRaises(Exception)

    def test_invalid_json(self):
        invalid_json = {
            "servers": [
                {"server": "first",
                    "address": "127.0.0.1:5000",
                    "poll_period": 60,
                    "regex": "Weight"
                 },
                {"server": "fourth",
                    "address": "127.0.0.1:5000",
                    "poll_period": 120,
                    "regex": ""
                 }
            ]
        }
        validate_schema_details(invalid_json, serverSchema)

        self.assertRaises(Exception)


if __name__ == '__main__':
    unittest.main()
