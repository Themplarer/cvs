import unittest
from collections import namedtuple

from commands import Init, Branch
from commitobject import CommitObject
from message_writer import MessageWriter
from repository import Repository
from repositorynotinitedexception import RepositoryNotInitedException
from tests.testcases import RepositoryTestCase
from utils.file_utils import write_file
from utils.main_file_utils import write_main_file


class TestBranch(RepositoryTestCase):
    def setUp(self):
        super().setUp()
        self._args = namedtuple('BranchArgs', ['branch', 'd'])


class TestBranchNotInited(TestBranch):
    def test(self):
        with self.assertRaises(RepositoryNotInitedException):
            Branch().execute(Repository(), self._args('a', False),
                             self._writer)

        self.assertFileContentsEqual(self._log,
                                     ('goodgit repository is not initiated!',))


class TestBranchInited(TestBranch):
    def setUp(self):
        super().setUp()

        # как будто пишем в /dev/null, эта часть логов не нужна
        Init().execute(Repository(), None, MessageWriter())

        _commits_dir = self._root_path / 'commits'
        _commit1 = CommitObject('', '', [], None, 1)
        _commit2 = CommitObject('', '', [], [_commit1], 2)
        _commits = {1: _commit1, 2: _commit2}

        for i, j in _commits.items():
            (_commits_dir / str(i)).mkdir()
            write_file(_commits_dir / f'{i}_info', (str(j),))

        _branches = {'master': _commits[1],
                     'head': _commits[1],
                     'develop': _commits[2]}
        write_main_file('master', _branches, dict())

        self._repo = Repository()

    def test_write_branches(self):
        self._test_common(None, False, 'master', 'head', 'develop')

    def test_create_existent(self):
        self._test_common('master', False, 'this branch has already existed!')

    def test_create_branch(self):
        self._test_common('test', False, 'branched!')

    def test_delete_not_marked(self):
        self._test_common(None, True, 'called to delete a branch '
                                      'but branch is not specified')

    def test_delete_head(self):
        self._test_delete_protected_branch('head')

    def test_delete_master(self):
        self._test_delete_protected_branch('master')

    def test_delete_other(self):
        self._test_common('develop', True, 'deleted!')

    def test_delete_nonexistent(self):
        self._test_common('gneg', True, 'there is no such branch!')

    def _test_delete_protected_branch(self, branch_name):
        self._test_common(branch_name, True,
                          'it\'s impossible to delete protected branch!')

    def _test_common(self, branch, delete, *message):
        Branch().execute(self._repo, self._args(branch, delete), self._writer)
        self.assertFileContentsEqual(self._log, message)


if __name__ == '__main__':
    unittest.main()
