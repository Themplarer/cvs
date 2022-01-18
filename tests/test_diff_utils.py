import unittest
from pathlib import Path

from commands import Init
from commitobject import CommitObject
from message_writer import MessageWriter
from repository import Repository
from tests.testcases import FileRelatedTestCase, RepositoryTestCase
from utils.diff_utils import write_diffs, merge_file, get_diffs, restore_state
from utils.file_utils import remove_dir_recursively, write_file


class TestDiffUtilsWriteDiffs(FileRelatedTestCase):
    def setUp(self):
        self.test_path = Path('test')

        _1_txt = self.test_path / '1.txt'
        _2_txt = self.test_path / '2.txt'
        _gneg_M = self.test_path / 'gneg' / 'M'
        _python_main_py = self.test_path / 'python' / 'main.py'

        self.diffs = dict()

        self.diffs[_1_txt] = ['--- ',
                              '+++ ',
                              '@@ -0,0 +1,11 @@',
                              '+from setuptools import setup',
                              '+',
                              '+setup(',
                              '+    name="goodgit",',
                              '+    author="Evgeny Khoroshavin",',
                              '+    entry_points={',
                              '+        \'console_scripts\': [',
                              '+            \'goodgit = main:main\'',
                              '+        ]',
                              '+    }',
                              '+)']
        self.diffs[_2_txt] = ['--- ',
                              '+++ ',
                              '@@ -0,0 +1,6 @@',
                              '+gnegnegnegnegnegnegnegnegne',
                              '+egnegnengnegnengnengneg',
                              '+wnweqqwe',
                              '+qweqweqwe',
                              '+qwe',
                              '+qefffdddd']
        self.diffs[_gneg_M] = ['--- ',
                               '+++ ',
                               '@@ -0,0 +1,1 @@',
                               '+1']
        self.diffs[_python_main_py] = ['--- ',
                                       '+++ ',
                                       '@@ -0,0 +1,1 @@',
                                       '+if __name__ == \'__main__\':',
                                       '+    pass',
                                       '+']

    def test_simple(self):
        write_diffs(self.diffs, Path('.'))

        for i, j in self.diffs.items():
            self.assertFileContentsEqual(i, j)

    def test_subdir(self):
        p = Path('subdir')
        write_diffs(self.diffs, p)

        for i, j in self.diffs.items():
            self.assertFileContentsEqual(p / i, j)

    def tearDown(self):
        remove_dir_recursively(Path('test'), ok_not_exists=True)
        remove_dir_recursively(Path('subdir'), ok_not_exists=True)


class TestDiffUtilsMergeFile(unittest.TestCase):
    def test_simple(self):
        file_before = [
            "import unittest",
            "from pathlib import Path",
            "",
            "",
            "class TestDiffUtilsWriteDiffs(unittest.TestCase):",
            "    def setUp(self):",
            "        self.test_path = Path('test')",
            "",
            "        _1_txt = self.test_path / '1.txt'",
            "        _2_txt = self.test_path / '2.txt'",
            "        _gneg_M = self.test_path / 'gneg' / 'M'",
            "        _python_main_py = self.test_path / 'python' / 'main.py'",
            "",
            "        self.diffs = dict()",
            "",
            "        self.diffs[_1_txt] = []",
            "        self.diffs[_2_txt] = []",
            "        self.diffs[_gneg_M] = []",
            "        self.diffs[_python_main_py] = []",
            "",
            "    def test(self):",
            "        self.assertEqual(True, False)  # add assertion here",
            "",
            "",
            "if __name__ == '__main__':",
            "    unittest.main()"]

        diff = [
            '--- ',
            '+++ ',
            '@@ -13,7 +13,20 @@',
            '',
            '         self.diffs = dict()',
            '',
            '-        self.diffs[_1_txt] = []',
            '+        self.diffs[_1_txt] = ["--- ",',
            '+                              "+++ ",',
            '+                              "@@ -0,0 +1,11 @@",',
            '+                              "+from setuptools import setup",',
            '+                              "+",',
            '+                              "+setup(",',
            '+                              "+    name=\"goodgit\",",',
            '+                              "+    author='
            '\"Evgeny Khoroshavin\",",',
            '+                              "+    entry_points={",',
            '+                              "+        \'console_scripts\': '
            '[",',
            '+                              "+            \'goodgit = '
            'main:main\'",',
            '+                              "+        ]",',
            '+                              "+    }",',
            '+                              "+)"]',
            '         self.diffs[_2_txt] = []',
            '         self.diffs[_gneg_M] = []',
            '         self.diffs[_python_main_py] = []']

        res = ['import unittest',
               'from pathlib import Path',
               '',
               '',
               'class TestDiffUtilsWriteDiffs(unittest.TestCase):',
               '    def setUp(self):',
               '        self.test_path = Path(\'test\')',
               '',
               '        _1_txt = self.test_path / \'1.txt\'',
               '        _2_txt = self.test_path / \'2.txt\'',
               '        _gneg_M = self.test_path / \'gneg\' / \'M\'',
               '        _python_main_py = self.test_path / \'python\' / '
               '\'main.py\'',
               '',
               '        self.diffs = dict()',
               '',
               '        self.diffs[_1_txt] = ["--- ",',
               '                              "+++ ",',
               '                              "@@ -0,0 +1,11 @@",',
               '                              "+from setuptools import '
               'setup",',
               '                              "+",',
               '                              "+setup(",',
               '                              "+    name=\"goodgit\",",',
               '                              "+    author='
               '\"Evgeny Khoroshavin\",",',
               '                              "+    entry_points={",',
               '                              "+        '
               '\'console_scripts\': [",',
               '                              "+            \'goodgit = '
               'main:main\'",',
               '                              "+        ]",',
               '                              "+    }",',
               '                              "+)"]',
               '        self.diffs[_2_txt] = []',
               '        self.diffs[_gneg_M] = []',
               '        self.diffs[_python_main_py] = []',
               '',
               '    def test(self):',
               '        self.assertEqual(True, False)  # add assertion here',
               '',
               '',
               'if __name__ == \'__main__\':',
               '    unittest.main()']

        file_after = merge_file(file_before, diff)
        self.assertListEqual(file_after, res)


class TestDiffUtilsGetDiffsRestoreStateSimple(unittest.TestCase):
    def test_create(self):
        before = {'test': []}
        after = {'test': ['123', '213', 'a']}
        diff = {
            'test': ['--- ', '+++ ', '@@ -0,0 +1,3 @@', '+123', '+213', '+a']}

        self.assertDictEqual(diff, get_diffs(before, after))

    def test_delete(self):
        before = {'test': ['123', '213', 'a']}
        after = {'test': []}
        diff = {
            'test': ['--- ', '+++ ', '@@ -1,3 +0,0 @@', '-123', '-213', '-a']}

        self.assertDictEqual(diff, get_diffs(before, after))

    def test_edit(self):
        before = {'test': ['123', '213', 'a']}
        after = {'test': ['123', '111', 'aaa']}
        diff = {'test': ['--- ',
                         '+++ ',
                         '@@ -1,3 +1,3 @@',
                         ' 123',
                         '-213',
                         '-a',
                         '+111',
                         '+aaa']}

        self.assertDictEqual(diff, get_diffs(before, after))

    def test_restore_state_simple(self):
        self.assertDictEqual(restore_state(None), dict())


class TestDiffUtilsRestoreState(RepositoryTestCase):
    def setUp(self):
        super().setUp()
        Init().execute(Repository(), None, MessageWriter())

        _commit1_files = {'1.txt': ('--- ',
                                    '+++ ',
                                    '@@ -0,0 +1,3 @@',
                                    '+123',
                                    '+213',
                                    '+a')}

        _commit2_files = {'1.txt': ('--- ',
                                    '+++ ',
                                    '@@ -1,3 +1,5 @@',
                                    ' 123',
                                    ' 213',
                                    '-a',
                                    '+b',
                                    '+1',
                                    '+1'),
                          '2.txt': ('--- ',
                                    '+++ ',
                                    '@@ -0,0 +1,1 @@',
                                    '+лень уже тесты писать')}

        _commits_dir = self._root_path / 'commits'
        self._commit1 = CommitObject('', '', [], None, 1)
        self._commit2 = CommitObject('', '', [], [self._commit1], 2)

        for i, j in ((self._commit1, _commit1_files),
                     (self._commit2, _commit2_files)):
            commit_dir = _commits_dir / str(i.hash)
            commit_dir.mkdir()

            for k, l in j.items():
                write_file(commit_dir / k, l)

            write_file(_commits_dir / f'{i.hash}_info', (str(i),))

    def test_commit_1(self):
        self.assertDictEqual(restore_state(self._commit1),
                             {Path('1.txt'): ['123', '213', 'a']})

    def test_commit_2(self):
        self.assertDictEqual(restore_state(self._commit2),
                             {Path('1.txt'): ['123', '213', 'b', '1', '1'],
                              Path('2.txt'): ['лень уже тесты писать']})


if __name__ == '__main__':
    unittest.main()
