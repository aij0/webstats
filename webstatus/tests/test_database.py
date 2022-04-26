import unittest
from common.validators import validate_schema_details
from database.config import databaseSchema


class TestDataBaseConfigurationValidation(unittest.TestCase):
    '''
    Test database server config validation
    '''

    def test_valid_json(self):
        valid_json = {"server": "local",
                      "address": "127.0.0.1",
                      "port": 1234,
                      "user": "admin",
                      "password": "hash"
                      }

        returnvalue = validate_schema_details(valid_json, databaseSchema)

        self.assertEqual(returnvalue, True)

    def test_empty_json(self):
        empty_json = {
        }
        validate_schema_details(empty_json, databaseSchema)

        self.assertRaises(Exception)

    def test_invalid_json(self):
        invalid_json = {"server": "local",
                        "address": "127.0.0.1",
                        "port": "3306",
                        "wrongkey": "wrong"
                        }
        validate_schema_details(invalid_json, databaseSchema)

        self.assertRaises(Exception)


if __name__ == '__main__':
    unittest.main()
