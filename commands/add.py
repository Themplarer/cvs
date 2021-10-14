import pathlib
import re
from argsparseerror import ArgsParseError
from commands.command import Command


class Add(Command):
    # todo refactor all
    # todo переделать проверку файлов на включение в список

    help_string = '''Usage: python ./main.py add [path]
    path - kind of filter for directories and files, compulsory argument
    
    Adds specified files and directories to the index'''

    def parse_args(self, args):
        res = dict()
        if len(args) == 0:
            raise ArgsParseError
        res['path'] = args[0]
        return res

    _comments = re.compile(r'^(#.*)| $')

    def _ignore(self, ignore_set, x):
        res = [re.compile(i.replace('\\', '/')) for i in ignore_set]
        return list(filter(lambda s: self._filter(s, res),
                           map(lambda i: str(i).replace('\\', '/'), x)))

    @staticmethod
    def _filter(s, res):
        for i in res:
            if i.match(s):
                return False

        return True

    def execute(self, caller, args):
        with open('.gitignore') as f:
            ignore_set = {i.replace('\\', '/').replace('*', '.*') + '.*' for i
                          in (filter(
                    lambda x: not len(x) == 0 and not self._comments.match(x),
                    f.read().splitlines()))}

        _path = pathlib.Path(args['path'])
        _f = [_path] if _path.is_file() else list(filter(lambda x: x.is_file(), _path.rglob('*')))
        files = {str(i) for i in self._ignore(ignore_set, _f)}

        with open(caller.dir_path + 'index') as f:
            files = files.union(set(f.read().splitlines()))

        with open(caller.dir_path + 'index', 'w') as f:
            f.writelines('\n'.join(files))

        print('added')
