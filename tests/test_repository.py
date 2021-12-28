import unittest
from pathlib import Path

from repository import Repository
from utils.main_file_utils import write_main_file


class TestRepository(unittest.TestCase):
    def setUp(self):
        self._rep_attr = {'selected_branch': 'master',
                          'branches': {'master': None},
                          'tags': dict(),
                          'commits': dict()}
        self.path = Path('.goodgit')

    def test_not_initiated_repo(self):
        repository = Repository()
        self.assertFalse(repository.is_initiated)
        for i in self._rep_attr:
            self.assertFalse(hasattr(repository, i))

    def test_initiated_repo(self):
        self._init_repo()
        repository = Repository()
        self.assertTrue(repository.is_initiated)
        self.assertEqual(repository.selected_branch,
                         self._rep_attr['selected_branch'])
        self.assertDictEqual(repository.branches, self._rep_attr['branches'])
        self.assertDictEqual(repository.tags, self._rep_attr['tags'])
        self.assertDictEqual(repository.commits, self._rep_attr['commits'])
        self._rm_dir_recursively(self.path)

    def _init_repo(self):
        self.path.mkdir(exist_ok=True)
        (self.path / 'commits').mkdir()
        (self.path / 'stashes').mkdir()
        (self.path / 'index').touch()
        write_main_file(self._rep_attr['selected_branch'],
                        self._rep_attr['branches'],
                        self._rep_attr['tags'])

    def _rm_dir_recursively(self, path):
        for child in path.glob('*'):
            if child.is_file():
                child.unlink()
            else:
                self._rm_dir_recursively(child)
        path.rmdir()


if __name__ == '__main__':
    unittest.main()
