import unittest
from pathlib import Path

from commands import Init
from message_writer import FileMessageWriter
from repository import Repository
from tests.testcases import FileRelatedTestCase, RepositoryTestCase
from utils.file_utils import remove_dir_recursively, write_file
from utils.main_file_utils import write_main_file


class TestInit(RepositoryTestCase):
    def setUp(self):
        super().setUp()
        self._dirs = {self._root_path / 'commits', self._root_path / 'stashes'}
        self._files = {self._root_path / 'index'}


class TestInitForNotInited(TestInit):
    def test_init(self):
        r = Repository()
        Init().execute(r, None, self._writer)

        self.assertDictEqual(r.branches, {'master': None, 'head': None})
        self.assertSetEqual(set(Path('.goodgit').rglob('*')),
                            self._dirs | self._files)
        self.assertTrue(self._gitignore.exists())
        self.assertFileContentsEqual(self._log, ('initiated',))

    def test_init_if_goodgit_dir_exists(self):
        self._root_path.mkdir()

        r = Repository()
        Init().execute(r, None, self._writer)

        self.assertFileContentsEqual(self._log,
                                     ('goodgit directory has already existed '
                                      'but it is not initiated! '
                                      'consider checking it out and deleting',))


class TestInitForInited(TestInit):
    def setUp(self):
        super().setUp()
        self._root_path.mkdir()

        for i in self._dirs:
            i.mkdir()

        self._gitignore.touch()
        self._files.add(self._root_path / 'main')
        for i in self._files:
            i.touch()

    def test_init_empty(self):
        write_main_file('master', {'master': None, 'head': None}, dict())

        r = Repository()
        Init().execute(r, None, self._writer)

        self.assertDictEqual(r.branches, {'master': None, 'head': None})
        self.assertSetEqual(set(Path('.goodgit').rglob('*')),
                            self._dirs | self._files)
        self.assertTrue(self._gitignore.exists())
        self.assertFileContentsEqual(self._log,
                                     ('goodgit has already been initiated!',))

    def test_init_empty_with_gitignore(self):
        write_main_file('master', {'master': None, 'head': None}, dict())

        gitignore_text = ['#test', '#da']
        write_file(self._gitignore, gitignore_text)
        r = Repository()
        Init().execute(r, None, self._writer)

        self.assertDictEqual(r.branches, {'master': None, 'head': None})
        self.assertSetEqual(set(Path('.goodgit').rglob('*')),
                            self._dirs | self._files)
        self.assertTrue(self._gitignore.exists())
        self.assertFileContentsEqual(self._log,
                                     ('goodgit has already been initiated!',))
        self.assertFileContentsEqual(self._gitignore, gitignore_text)


if __name__ == '__main__':
    unittest.main()
