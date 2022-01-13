import unittest
from collections import namedtuple
from pathlib import Path

from commands import Init, Tag
from commitobject import CommitObject
from message_writer import MessageWriter
from repository import Repository
from repositorynotinitedexception import RepositoryNotInitedException
from tests.testcases import RepositoryTestCase
from utils.file_utils import write_file
from utils.main_file_utils import write_main_file


class TestTag(RepositoryTestCase):
    def setUp(self):
        super().setUp()
        self._args = namedtuple('TagArgs', ['tag', 'd'])


class TestTagNotInited(TestTag):
    def test(self):
        with self.assertRaises(RepositoryNotInitedException):
            Tag().execute(Repository(), self._args('a', False), self._writer)

        self.assertFileContentsEqual(self._log,
                                     ('goodgit repository is not initiated!',))


class TestTagInited(TestTag):
    def setUp(self):
        super().setUp()

        # как будто пишем в /dev/null, эта часть логов не нужна
        Init().execute(Repository(), None, MessageWriter())

        _commits_dir = Path('.goodgit') / 'commits'
        _commit1 = CommitObject('', '', [], None, 1)
        _commit2 = CommitObject('', '', [], [_commit1], 2)
        _commits = {1: _commit1, 2: _commit2}

        for i, j in _commits.items():
            (_commits_dir / str(i)).mkdir()
            write_file(_commits_dir / f'{i}_info', (str(j),))

        _branches = {'master': _commits[1],
                     'head': _commits[1]}
        _tags = {'release-1': _commits[2]}
        write_main_file('master', _branches, _tags)

        self._repo = Repository()

    def test_write_tags(self):
        self._test_common(None, False, 'release-1')

    def test_create_existent(self):
        self._test_common('release-1', False, 'this tag has already existed!')

    def test_create_tag(self):
        self._test_common('test', False, 'taged!')

    def test_delete_not_marked(self):
        self._test_common(None, True, 'called to delete a tag '
                                      'but tag is not specified')

    def test_delete_other(self):
        self._test_common('release-1', True, 'deleted!')

    def test_delete_nonexistent(self):
        self._test_common('gneg', True, 'there is no such tag!')

    def _test_common(self, tag, delete, *message):
        Tag().execute(self._repo, self._args(tag, delete), self._writer)
        self.assertFileContentsEqual(self._log, message)


if __name__ == '__main__':
    unittest.main()
