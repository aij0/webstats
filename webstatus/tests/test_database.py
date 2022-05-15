import unittest
import database.local
from common.validators import validate_schema_details
from database.config import databaseSchema
from sqlite3 import Connection


class TestDataBaseConfigurationValidation(unittest.TestCase):
    '''
    Test database server config validation
    '''

    def test_valid_json(self):
        valid_json = {"name": "local",
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
        invalid_json = {"name": "local",
                        "address": "127.0.0.1",
                        "port": 3306,
                        "wrongkey": "wrong"
                        }
        validate_schema_details(invalid_json, databaseSchema)

        self.assertRaises(Exception)


class TestDataBaseCreation(unittest.TestCase):
    '''
    Test database creation
    '''

    tempdatabase = {
        "type": "local",
        "name": ":memory:",
        "user": "postgres",
        "password": "password",
        "address": "127.0.0.1",
        "port": "5432"
    }

    def test_database_creation(self):
        local_db = database.local.SqliteDatabase()
        temp_db = local_db.setup_database(self.tempdatabase)
        self.assertEqual(type(temp_db), Connection)
        temp_db.close()


if __name__ == '__main__':
    unittest.main()
