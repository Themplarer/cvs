import unittest
from pathlib import Path

from repository import Repository
from utils.file_utils import remove_dir_recursively
from utils.main_file_utils import write_main_file


class TestRepository(unittest.TestCase):
    def setUp(self):
        self._rep_attr = {'selected_branch': 'master',
                          'branches': {'master': None, 'head': None},
                          'tags': dict()}

    def assertRepositoryVariablesCorrect(self, repository):
        for i, j in self._rep_attr.items():
            self.assertEqual(getattr(repository, i), j)


class TestNonInitiatedRepository(TestRepository):
    def test_not_initiated_repo(self):
        r = Repository()
        self.assertFalse(r.is_initiated)
        self.assertRepositoryVariablesCorrect(r)
        self.assertFalse(hasattr(r, 'commits'))


class TestInitiatedRepository(TestRepository):
    def setUp(self):
        super().setUp()

        self._root = Path('.goodgit')
        self._root.mkdir()
        (self._root / 'commits').mkdir()
        (self._root / 'stashes').mkdir()
        (self._root / 'index').touch()
        write_main_file(self._rep_attr['selected_branch'],
                        self._rep_attr['branches'],
                        self._rep_attr['tags'])

    def test_initiated_repo(self):
        r = Repository()
        self.assertTrue(r.is_initiated)
        self.assertRepositoryVariablesCorrect(r)
        self.assertDictEqual(r.commits, dict())

    def tearDown(self):
        remove_dir_recursively(self._root)


if __name__ == '__main__':
    unittest.main()
