import getpass
import os
import re
from sys import argv

from argsparseerror import ArgsParseError
from commands.add import Add
from commands.branch import Branch
from commands.commit import Commit
from commands.help import Help
from commands.init import Init


class Main:
    _branch = re.compile(r'^(.*):(.*)')
    author = getpass.getuser()
    dir_path = './.goodgit/'
    oper_dict = dict(init=Init, help=Help, add=Add, commit=Commit,
                     branch=Branch)
    branches = dict()

    def is_initiated(self):
        return os.path.exists(self.dir_path) and \
               os.path.exists(self.dir_path + 'main')

    def _fill_branches(self):
        with open(self.dir_path + 'main') as f:
            for line in f:
                match = self._branch.match(line)
                if match:
                    self.branches[match.group(1)] = None
                    if len(match.groups()) == 2:
                        self.branches[match.group(1)] = match.group(2)

    def main(self):
        if len(argv) < 2:
            Help.execute(self, dict())
        else:
            if argv[1] != 'init' and not self.is_initiated():
                print('not a goodgit repository')
            else:
                if argv[1] != 'init':
                    self._fill_branches()

                command = self.oper_dict[argv[1]]()
                args = argv[2:]
                try:
                    parsed_args = command.parse_args(args)
                    command.execute(self, parsed_args)
                except ArgsParseError:
                    print('Incorrect arguments!')
                    print(command.help_string)


if __name__ == '__main__':
    Main().main()
