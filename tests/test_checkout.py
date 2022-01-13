import unittest
from collections import namedtuple
from pathlib import Path

from commands import Init, Branch, Checkout
from commitobject import CommitObject
from message_writer import MessageWriter
from repository import Repository
from repositorynotinitedexception import RepositoryNotInitedException
from tests.testcases import RepositoryTestCase
from utils.file_utils import write_file
from utils.main_file_utils import write_main_file


class TestCheckout(RepositoryTestCase):
    def setUp(self):
        super().setUp()
        self._args = namedtuple('CheckoutArgs', ['pointer'])


class TestTagNotInited(TestCheckout):
    def test(self):
        with self.assertRaises(RepositoryNotInitedException):
            Branch().execute(Repository(), self._args('a'), self._writer)

        self.assertFileContentsEqual(self._log,
                                     ('goodgit repository is not initiated!',))


class TestTagInited(TestCheckout):
    def setUp(self):
        super().setUp()

        # как будто пишем в /dev/null, эта часть логов не нужна
        Init().execute(Repository(), None, MessageWriter())

        _commits_dir = Path('.goodgit') / 'commits'
        _commit1 = CommitObject('', '', [], None, 1)
        _commit2 = CommitObject('', '', [], [_commit1], 2)
        _commit3 = CommitObject('', '', [], [_commit1], 3)
        _commits = {1: _commit1, 2: _commit2, 3: _commit3}

        for i, j in _commits.items():
            (_commits_dir / str(i)).mkdir()
            write_file(_commits_dir / f'{i}_info', (str(j),))

        _branches = {'master': _commits[1],
                     'head': _commits[1],
                     'develop': _commits[3]}
        _tags = {'release-1': _commits[2]}
        write_main_file('master', _branches, _tags)

        self._repo = Repository()

    def test_checkout_branch(self):
        self._test_common('develop', 'checked out branch develop')

    def test_checkout_tag(self):
        self._test_common('release-1', 'checked out tag release-1',
                          'be careful: it\'s impossible to commit '
                          'at this pointer!')

    def test_checkout_commit(self):
        self._test_common('1', 'checked out commit 1',
                          'be careful: it\'s impossible to commit '
                          'at this pointer!')

    def test_no_pointer(self):
        self._test_common('asdasd', 'there is no suitable pointer '
                                    '(commit, tag or branch) to checkout!')

    def _test_common(self, pointer, *message):
        Checkout().execute(self._repo, self._args(pointer), self._writer)
        self.assertFileContentsEqual(self._log, message)


if __name__ == '__main__':
    unittest.main()
