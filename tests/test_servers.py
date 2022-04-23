import unittest
import src.webstatus.server.servers as servers


class TestCodeStyle(unittest.TestCase):
    '''
    Test server list json validation
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
        returnvalue = servers.validate_server_details(valid_json)

        self.assertEqual(returnvalue, True)

    def test_empty_json(self):
        empty_json = {
        }
        servers.validate_server_details(empty_json)

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
        servers.validate_server_details(invalid_json)

        self.assertRaises(Exception)


if __name__ == '__main__':
    unittest.main()
