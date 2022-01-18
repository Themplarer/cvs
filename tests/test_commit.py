import unittest
from collections import namedtuple
from difflib import unified_diff
from pathlib import Path

from commands import Init, Checkout, Commit, Add
from commitobject import CommitObject
from message_writer import MessageWriter
from repository import Repository
from tests.testcases import RepositoryTestCase
from utils.file_utils import write_file, get_files, read_file
from utils.main_file_utils import write_main_file


class TestCommit(RepositoryTestCase):
    def setUp(self):
        super().setUp()

        # как будто пишем в /dev/null, эта часть логов не нужна
        Init().execute(Repository(), None, MessageWriter())
        files = list(get_files('*', filter_by_gitignore=True))

        _commits_dir = Path('.goodgit') / 'commits'
        _commit1 = CommitObject('', '', files, None, 1)
        write_file(_commits_dir / '1_info', (str(_commit1),))
        _commits_dir /= '1'
        _commits_dir.mkdir()

        for i in files:
            write_file(_commits_dir / str(i),
                       (j.strip('\n')
                        for j in unified_diff(list(), list(read_file(i)))))

        _branches = {'master': _commit1, 'head': _commit1}
        _tags = {'release-1': _commit1}
        write_main_file('master', _branches, _tags)

        self._repo = Repository()
        self._args = namedtuple('CommitArgs', ['message'])

    def test_commit_to_tag_is_restricted(self):
        Checkout().execute(self._repo,
                           namedtuple('name', ['pointer'])('release-1'),
                           MessageWriter())

        Commit().execute(self._repo, self._args('1'), self._writer)
        self.assertFileContentsEqual(self._log, ('it\'s impossible to commit '
                                                 'to this pointer! checkout '
                                                 'branch before',))

    def test_commit_to_commit_is_restricted(self):
        Checkout().execute(self._repo,
                           namedtuple('name', ['pointer'])('1'),
                           MessageWriter())

        Commit().execute(self._repo, self._args('1'), self._writer)
        self.assertFileContentsEqual(self._log, ('it\'s impossible to commit '
                                                 'to this pointer! checkout '
                                                 'branch before',))

    def test_commit_when_nothing_in_index(self):
        Commit().execute(self._repo, self._args('1'), self._writer)
        self.assertFileContentsEqual(self._log, ('nothing to commit!',))

    def test_commit_if_nothing_changed(self):
        Add().execute(self._repo, namedtuple('Add', ['path'])('*'),
                      MessageWriter())

        Commit().execute(self._repo, self._args('1'), self._writer)
        self.assertFileContentsEqual(self._log, ('nothing to commit!',))


if __name__ == '__main__':
    unittest.main()
