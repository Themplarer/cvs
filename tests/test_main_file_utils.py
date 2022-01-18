import unittest
from pathlib import Path

from commitobject import CommitObject
from utils.file_utils import remove_dir_recursively, write_file, read_file
from utils.main_file_utils import write_main_file, read_main_file

_sep = '__________'


class TestMainFileUtils(unittest.TestCase):
    def setUp(self):
        self.dir_path = Path('.goodgit')
        self.dir_path.mkdir()
        commits_dir_path = self.dir_path / 'commits'
        commits_dir_path.mkdir()

        commits = {1: CommitObject('', '', list(), None, 1),
                   12: CommitObject('', '', list(), None, 12)}

        write_file(commits_dir_path / '1_info', (str(commits[1]),))
        write_file(commits_dir_path / '12_info', (str(commits[12]),))

        self.branches = {'master': commits[1], 'head': commits[1],
                         'develop': commits[12]}
        self.tags = {'release-1': commits[1], 'beta-2.0': commits[12]}

    def tearDown(self):
        remove_dir_recursively(self.dir_path)

    def test_write_main_file_empty(self):
        branches = {'master': None, 'head': None}
        lines = ['master|', _sep, 'master:', 'head:']
        self._test_write_main_file('master', branches, dict(), lines)

    def test_write_main_file_with_selected_not_from_overall_branches(self):
        with self.assertRaises(AttributeError) as a:
            write_main_file('some_branch', self.branches, self.tags)

        self.assertEqual(a.exception.args[0], 'bad selected branch!')

    def test_write_main_file_corrects_head(self):
        lines = ['develop|', _sep, 'master:1', 'head:12', 'develop:12']
        self._test_write_main_file('develop', self.branches, dict(), lines)

    def test_write_main_file_with_selected_from_overall_branches(self):
        lines = ['master|', _sep, 'master:1', 'head:1', 'develop:12']
        self._test_write_main_file('master', self.branches, dict(), lines)

    def test_write_main_file_with_tags(self):
        lines = ['master|', _sep, 'master:1', 'head:1', 'develop:12', _sep,
                 'release-1:1', 'beta-2.0:12']
        self._test_write_main_file('master', self.branches, self.tags, lines)

    def test_read_main_file_empty(self):
        branches = {'master': None, 'head': None}
        lines = ['master|', _sep, 'master:', 'head:']
        self._test_read_main_file(lines, 'master', branches, dict())

    def test_read_main_file(self):
        lines = ['develop|', _sep, 'master:1', 'head:1', 'develop:12']
        self._test_read_main_file(lines, 'develop', self.branches, dict())

    def test_read_main_file_with_tags(self):
        lines = ['develop|', _sep, 'master:1', 'head:1', 'develop:12', _sep,
                 'release-1:1', 'beta-2.0:12']
        self._test_read_main_file(lines, 'develop', self.branches, self.tags)

    def _test_write_main_file(self, selected_branch, branches, tags,
                              lines_add):
        write_main_file(selected_branch, branches, tags)
        lines = ['KHOROSHiy_git v.1.0', _sep] + lines_add
        self.assertMainFileContentsEqual(Path('.goodgit') / 'main', lines)

    def _test_read_main_file(self, lines_add, selected_branch, branches, tags):
        lines = ['KHOROSHiy_git v.1.0', _sep] + lines_add
        write_file(Path('.goodgit') / 'main', lines)
        selected_branch_read, branches_read, tags_read = read_main_file()
        self.assertEqual(selected_branch_read, selected_branch)
        self.assertDictEqual(branches_read, branches)
        self.assertDictEqual(tags_read, tags)

    def assertMainFileContentsEqual(self, path, expected_lines):
        index = 0
        sep_counter = 0
        grouped_strs = set()
        grouped_strs_file = set()

        for line in read_file(path):
            if line == _sep:
                self.assertEqual(expected_lines[index], _sep)
                sep_counter += 1
                index += 1

                self.assertSetEqual(grouped_strs, grouped_strs_file)
                grouped_strs.clear()
                grouped_strs_file.clear()
                continue

            if sep_counter < 2:
                self.assertEqual(line.strip(), expected_lines[index])
            else:
                grouped_strs.add(expected_lines[index])
                grouped_strs_file.add(line)
            index += 1

        self.assertSetEqual(grouped_strs, grouped_strs_file)
        self.assertEqual(index, len(expected_lines))


if __name__ == '__main__':
    unittest.main()
