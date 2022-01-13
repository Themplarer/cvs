import copy
import unittest
from datetime import datetime
from pathlib import Path

from commitobject import CommitObject
from utils.file_utils import remove_dir_recursively


class TestCommitObject(unittest.TestCase):
    def setUp(self):
        self._root = Path('.goodgit')
        self._root.mkdir()
        commits_dir_path = self._root / 'commits'
        commits_dir_path.mkdir()
        (commits_dir_path / '1').mkdir()

        current_datetime = datetime(2222, 2, 2, 2, 2, 2, 22)
        self._commit = CommitObject('test', 'tester', list(), None, 1,
                                    current_datetime)

    def tearDown(self):
        remove_dir_recursively(self._root)

    def test_removes_milliseconds_in_timestamp(self):
        self.assertEqual(self._commit.time, datetime(2222, 2, 2, 2, 2, 2, 0))

    def test_not_eq_to_str(self):
        with self.assertRaises(ValueError) as a:
            if self._commit == 'commit kakoy-to':
                pass

        self.assertEqual(a.exception.args[0],
                         'second argument is not a CommitObject!')

    def test_eq_to_itself(self):
        self.assertEqual(self._commit, self._commit)

    def test_eq_to_its_copy(self):
        self.assertEqual(self._commit, copy.deepcopy(self._commit))

    def test_initializes_current_time_if_not_specified(self):
        new_commit = CommitObject('test', 'tester', list(), None, 1)
        # есть вероятность, что время тут будет отличаться сильнее,
        # чем на секунду, но она достаточно мала
        self.assertLess((datetime.now() - new_commit.time).total_seconds(), 1)

    def test_to_str(self):
        exp_str = '"test" "tester" "1" "2222-02-02 02:02:02" ""'
        self.assertEqual(exp_str, str(self._commit))

    def test_parse_str(self):
        self._test_parse('"test" "tester" "1" "2222-02-02 02:02:02" ""')

    def test_to_str_parse_together(self):
        self._test_parse(str(self._commit))

    def _test_parse(self, _str):
        self.assertEqual(self._commit, CommitObject.parse(_str, lambda: None))


if __name__ == '__main__':
    unittest.main()
