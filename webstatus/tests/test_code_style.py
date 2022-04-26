import unittest
import subprocess


class TestCodeStyle(unittest.TestCase):
    '''
    Test for different syntax issues
    '''
    def test_flake8(self):
        process = subprocess.Popen('flake8')
        returnvalue = process.wait()
        self.assertEqual(returnvalue, 0)


if __name__ == '__main__':
    unittest.main()
