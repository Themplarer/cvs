import unittest
from pathlib import Path

from message_writer import FileMessageWriter
from utils.file_utils import read_file, remove_dir_recursively


class FileRelatedTestCase(unittest.TestCase):
    def assertFileContentsEqual(self, path, expected_lines):
        index = 0
        for line in read_file(path):
            self.assertEqual(line.replace('\n', ''), expected_lines[index])
            index += 1

        self.assertEqual(index, len(expected_lines))


class CommandsTestCase(FileRelatedTestCase):
    def setUp(self):
        self._log = Path('test.log')
        self._writer = FileMessageWriter(self._log)

    def tearDown(self):
        if self._log.exists():
            self._log.unlink()


class RepositoryTestCase(CommandsTestCase):
    def setUp(self):
        super().setUp()
        self._root_path = Path('.goodgit')
        self._gitignore = Path('.gitignore')

    def tearDown(self):
        super().tearDown()

        if self._gitignore.exists():
            self._gitignore.unlink()

        remove_dir_recursively(self._root_path, ok_not_exists=True)
