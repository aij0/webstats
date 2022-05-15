import unittest
import os
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


class TestDataBaseCreationInMemory(unittest.TestCase):
    '''
    Test database creation in RAM
    '''

    ram_database = {
        "type": "local",
        "name": ":memory:",
        "user": "postgres",
        "password": "password",
        "address": "127.0.0.1",
        "port": "5432"
    }

    def test_database_creation_in_ram(self):
        local_db = database.local.SqliteDatabase()
        temp_db = local_db.setup_database(self.ram_database)
        self.assertEqual(type(temp_db), Connection)
        temp_db.close()


class TestDataBaseCreationInFile(unittest.TestCase):
    '''
    Test database creation in filesystem
    '''

    temp_database = {
        "type": "local",
        "name": "testdb",
        "user": "postgres",
        "password": "password",
        "address": "127.0.0.1",
        "port": "5432"
    }

    def setUp(self):
        local_db = database.local.SqliteDatabase()
        local_db.setup_database(self.temp_database)

    def tearDown(self):
        if os.path.exists(self.temp_database["name"]):
            os.remove(self.temp_database["name"])

    def test_database_connection_to_file(self):
        '''This test creates the local db file and writes to it'''
        local_db = database.local.SqliteDatabase()
        temp_db = local_db.create_connection(self.temp_database)
        self.assertEqual(type(temp_db), Connection)
        self.assertIs(os.path.exists(self.temp_database["name"]), True)
        temp_db.close()

    def test_database_init_succesful(self):
        ''' This test also reads the database with the local-module'''

        table_query = "SELECT name FROM sqlite_master WHERE type='table'"
        local_db = database.local.SqliteDatabase()
        raw_read_string = local_db.execute_query(self.temp_database,
                                                 "pull", table_query)
        read_list = []
        # remove special characters from the query with join/filter
        read_list.append(''.join(filter(str.isalnum, raw_read_string[0])))
        # second table "sqlite_sequence" is something from sqlite.
        read_list.append(''.join(filter(str.isalnum, raw_read_string[2])))
        print(read_list)
        self.assertEquals(["servers", "stats"], read_list)


if __name__ == '__main__':
    unittest.main()
