import unittest

from common.validators import validate_schema_details
from server.servers import serverSchema


class TestServerValidation(unittest.TestCase):
    '''
    Test Server JSON validation with server list
    '''

    def test_valid_json(self):
        valid_json = {"server": "first",
                      "address": "127.0.0.1:5000",
                      "poll_period": 60,
                      "regex": "Weight"
                      }
        returnvalue = validate_schema_details(valid_json, serverSchema)

        self.assertEqual(returnvalue, True)

    def test_empty_json(self):
        empty_json = {
        }
        validate_schema_details(empty_json, serverSchema)

        self.assertRaises(Exception)

    def test_invalid_json(self):
        invalid_json = {"server": 1,
                        "address": "127.0.0.1:5000",
                        "poll_period": 60,
                        "regex": "Weight"
                        }
        validate_schema_details(invalid_json, serverSchema)

        self.assertRaises(Exception)


if __name__ == '__main__':
    unittest.main()
