import re

import utils
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

    def execute(self, caller, args):
        _comments = re.compile(r'^(#.*|)$')
        ignore_paths = set()
        with open('.gitignore') as f:
            for line in f.read().splitlines():
                if not _comments.match(line):
                    ignore_paths.add(line)

        with open(caller.dir_path + '/index') as f:
            files = set(f.read().splitlines())

        files = utils.get_files_recursively(args['path'], files, ignore_paths)
        with open(caller.dir_path + '/index', 'w') as f:
            f.writelines('\n'.join(files))

        print('added')
