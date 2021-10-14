import glob
import os
import re

from argsparseerror import ArgsParseError
from commands.command import Command


class Add(Command):
    _comments = re.compile(r'^(#.*)| $')

    help_string = '''Usage: python ./main.py add [path]
    path - kind of filter for directories and files, compulsory argument
    
    Adds specified files and directories to the index'''

    def parse_args(self, args):
        if len(args) != 1:
            raise ArgsParseError
        return {'path': args[0]}

    @staticmethod
    def _filter(files, reg_exps):
        for i in files:
            if os.path.exists(i) and os.path.isfile(i):
                res = False
                for j in reg_exps:
                    res = res or j.match(i)

                if not res:
                    yield i

    @staticmethod
    def _to_ignore_regexp(s):
        return re.compile(s.replace('\\', '/').replace('*', '.*') + '.*')

    def execute(self, caller, args):
        _comments = re.compile(r'^(#.*|)$')
        ignore_set = set()
        with open('.gitignore') as f:
            for line in f.read().splitlines():
                if not _comments.match(line):
                    ignore_set.add(self._to_ignore_regexp(line))

        with open(caller.dir_path + '/index') as f:
            files = set(f.read().splitlines())

        for i in glob.iglob(args['path'], recursive=True):
            files.add(i)

        files = self._filter(files, ignore_set)
        with open(caller.dir_path + '/index', 'w') as f:
            f.writelines('\n'.join(files))

        print('added')
