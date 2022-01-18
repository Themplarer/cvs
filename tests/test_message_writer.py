import unittest
from pathlib import Path

from message_writer import MessageWriter, FileMessageWriter
from tests.testcases import FileRelatedTestCase


class TestMessageWriter(unittest.TestCase):
    def test(self):
        # there is nothing to test, but I want to increase coverage
        MessageWriter().write(1, 2, 3)


class TestFileMessageWriter(FileRelatedTestCase):
    def setUp(self):
        self._path = Path('test')
        self._writer = FileMessageWriter(self._path)

    def tearDown(self):
        self._path.unlink()

    def test_simple(self):
        self._writer.write(1)
        self.assertFileContentsEqual(self._path, ('1',))

    def test_several_args(self):
        self._writer.write(1, 2, 3, '\n', 4)
        self.assertFileContentsEqual(self._path, ('1 2 3 ', ' 4'))

    def test_appends(self):
        self._path.write_text('123\n123\n')
        self._writer.write(1, 2, 3, '\n', 4)
        self.assertFileContentsEqual(self._path, ('123', '123', '1 2 3 ',
                                                  ' 4'))


if __name__ == '__main__':
    unittest.main()
