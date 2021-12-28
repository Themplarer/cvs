import unittest

from commands.init import Init
from repository import Repository


class TestMainFileUtils(unittest.TestCase):
    def setUp(self):
        self.repository = Repository()
        Init().execute(self.repository)

    def test_read_main_file(self):
        pass

    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
