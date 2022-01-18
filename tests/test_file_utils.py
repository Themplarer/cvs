import unittest
from pathlib import Path

from tests.testcases import FileRelatedTestCase
from utils.file_utils import write_file, remove_dir_recursively, get_files


class TestFileUtilsReadWrite(FileRelatedTestCase):
    lines = ['first line test',
             'second',
             'also a good lines separation test',
             'well, do not read this',
             'yeah, really',
             'there is nothing interesting in here',
             'give me 20 pts please']

    def setUp(self):
        self.path = Path('test.txt')

    def tearDown(self):
        self.path.unlink()

    def test_write_single_line(self):
        self._test_write_file(self.path, self.lines[:1])

    def test_write_multiple_lines(self):
        self._test_write_file(self.path, self.lines)

    def test_read_lines(self):
        self.path.touch()
        with self.path.open(encoding='utf-8', mode='w') as f:
            f.writelines('\n'.join(self.lines))

        self.assertFileContentsEqual(self.path, self.lines)

    def _test_write_file(self, path, lines):
        write_file(path, lines)
        self.assertFileContentsEqual(path, lines)


class TestFileUtilsRemoveDirectoryRecursivelySimple(unittest.TestCase):
    def setUp(self):
        self.p = Path('test')
        self.p.mkdir()

    def tearDown(self):
        remove_dir_recursively(self.p, ok_not_exists=True)

    def test_remove_empty_dir(self):
        remove_dir_recursively(self.p)
        self.assertFalse(self.p.exists())

    def test_remove_nonexistent_dir_if_ok_flag_is_not_set(self):
        with self.assertRaises(FileNotFoundError):
            remove_dir_recursively(self.p / '1')

    def test_remove_nonexistent_dir_if_ok_flag_is_set(self):
        remove_dir_recursively(self.p / '1', ok_not_exists=True)


class TestWithInitiatedDir(unittest.TestCase):
    def setUp(self):
        self._p = Path('test')
        self._p.mkdir()

        self._p_1 = self._p / '1'
        self._p_1.mkdir()

        self._p_1_file_py = self._p_1 / 'file.py'
        self._p_1_file_py.touch()

        self._p_1_not_a_file_py = self._p_1 / 'not_a_file.py'
        self._p_1_not_a_file_py.touch()

        self._p_1_virus_exe = self._p_1 / 'virus.exe'
        self._p_1_virus_exe.touch()

        self._p_a = self._p / 'a'
        self._p_a.mkdir()

        self._p_a_a = self._p_a / 'a'
        self._p_a_a.mkdir()

        self._p_a_a_a = self._p_a_a / 'a'
        self._p_a_a_a.touch()

        self._p_a_b = self._p_a / 'b'
        self._p_a_b.mkdir()

        self._contents = {self._p_1, self._p_1_file_py,
                          self._p_1_not_a_file_py, self._p_1_virus_exe,
                          self._p_a, self._p_a_a, self._p_a_a_a, self._p_a_b}

        self._files = {i for i in self._contents if i.is_file()}
        self._test_files = Path('.').glob('test_*.py')
        self._other_files = {Path('testcases.py')}

    def tearDown(self):
        remove_dir_recursively(self._p, ok_not_exists=True)


class TestFileUtilsRemoveDirectoryRecursivelyNested(TestWithInitiatedDir):
    def test_remove_nested_dir(self):
        remove_dir_recursively(self._p_1)
        self._contents.remove(self._p_1)
        self._contents.remove(self._p_1_file_py)
        self._contents.remove(self._p_1_not_a_file_py)
        self._contents.remove(self._p_1_virus_exe)
        self.assertSetEqual(set(self._p.rglob('*')), self._contents)

        remove_dir_recursively(self._p_a)
        self.assertSetEqual(set(self._p.rglob('*')), set())


class TestFileUtilsGetFiles(TestWithInitiatedDir):
    def test_all_files(self):
        self._files.update(self._test_files)
        self._files.update(self._other_files)
        self.assertEqual(get_files('*'), self._files)

    def test_all_files_from_subdir(self):
        self.assertEqual(get_files('*', path='test'), self._files)

    def test_all_files_with_non_intersecting_initials(self):
        self._test_all_files_with_initial(Path('../main.py'))

    def test_all_files_with_intersecting_initials(self):
        self._test_all_files_with_initial(Path('test_file_utils.py'))

    def test_mask_exe(self):
        self.assertEqual(get_files('*.exe', path='test'),
                         {self._p_1_virus_exe})

    def test_mask_py(self):
        self.assertEqual(get_files('*.py', path='test'),
                         {self._p_1_file_py, self._p_1_not_a_file_py})

    def _test_all_files_with_initial(self, initial):
        self._files.add(initial)
        self.assertEqual(get_files('*', path='test', initials=(initial,)),
                         self._files)


if __name__ == '__main__':
    unittest.main()
