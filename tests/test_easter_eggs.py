import unittest
from pathlib import Path

from commands.easter_eggs.credits import Credits
from commands.easter_eggs.remotes import Pull, Push, Fetch, Clone
from message_writer import FileMessageWriter
from tests.testcases import FileRelatedTestCase


class TestEasterEggs(FileRelatedTestCase):
    def setUp(self):
        self._logfile = Path('log').absolute()
        self._writer = FileMessageWriter(self._logfile)

    def tearDown(self):
        self._logfile.unlink()

    def test_credits(self):
        self._test(Credits,
                   '',
                   'KHOROSHiy_git v.1.0',
                   'Copyright (c) 2021-2022 Evgeny Khoroshavin ('
                   'github.com/Themplarer)',
                   'All rights reserved',
                   '',
                   'CVS project for Python course',
                   '',
                   'Special thanks to Vladimir Zverev for 20 points')

    def test_pull(self):
        self._test_remote(Pull)

    def test_push(self):
        self._test_remote(Push)

    def test_fetch(self):
        self._test_remote(Fetch)

    def test_clone(self):
        self._test_remote(Clone)

    def _test_remote(self, command):
        self._test(command, 'not available in free version!')

    def _test(self, command, *args):
        command().execute(None, None, self._writer)
        self.assertFileContentsEqual(self._logfile, args)


# class TestJokes(TestEasterEggs):
#     def setUp(self):
#         super().setUp()
#         os.chdir('..')
#         self.args = namedtuple('JokeArgs', ['number'])
#
#     def tearDown(self):
#         os.chdir('tests')
#         super().tearDown()
#
#     def test_joke_1(self):
#         self._test_joke(1)
#
#     def test_joke_2(self):
#         self._test_joke(2)
#
#     def _test_joke(self, i):
#         jokes_path = (Path('commands') / 'easter_eggs' / 'jokes').absolute()
#         Joke().execute(None, self.args(i), self._writer)
#         expected_lines = [f'Внимание, анекдот №{i}'] + \
#             list(read_file(jokes_path / f'{i}.txt'))
#         self.assertFileContentsEqual(self._logfile, expected_lines)


if __name__ == '__main__':
    unittest.main()
