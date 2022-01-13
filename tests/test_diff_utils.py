import unittest
from pathlib import Path

from tests.testcases import FileRelatedTestCase
from utils.diff_utils import write_diffs, merge_file, get_diffs
from utils.file_utils import remove_dir_recursively


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
            '+                              "+        \'console_scripts\': [",',
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
               '                              "+from setuptools import setup",',
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


class TestDiffUtilsGetDiffs(unittest.TestCase):
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


class TestDiffUtilsRestoreState(unittest.TestCase):
    def test_simple(self):
        pass


if __name__ == '__main__':
    unittest.main()
