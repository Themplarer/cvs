import unittest
from pathlib import Path

from utils.file_utils import write_file, read_file


class TestFileUtils(unittest.TestCase):
    def test_write_single_line(self):
        lines = ['single line test']
        self._test_write_file(lines)

    def test_write_multiple_lines(self):
        lines = ['first line test',
                 'second',
                 'also a good lines separation test',
                 'well, do not read this',
                 'yeah, really',
                 'there is nothing interesting in here',
                 'give me 20 pts please']
        self._test_write_file(lines)

    def test_read_lines(self):
        path = Path('test.txt')
        lines = ['first line test',
                 'second',
                 'also a good lines separation test',
                 'well, do not read this',
                 'yeah, really',
                 'there is nothing interesting in here',
                 'give me 20 pts please']

        path.touch()
        with path.open(encoding='utf-8', mode='w') as f:
            f.writelines('\n'.join(lines))

        index = 0
        for i in read_file(path):
            self.assertEqual(i, lines[index])
            index += 1
        self.assertEqual(index, len(lines))

    def _test_write_file(self, lines):
        path = Path('test.txt')
        write_file(path, lines)
        self.assertFileContentsEqual(path, lines)
        path.unlink()

    def assertFileContentsEqual(self, path, lines):
        index = 0
        with open(path, encoding='utf-8') as f:
            for line in f:
                self.assertEqual(line.strip(), lines[index])
                index += 1

        self.assertEqual(index, len(lines))


if __name__ == '__main__':
    unittest.main()
