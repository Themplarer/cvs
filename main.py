import getpass
import os
import re
from sys import argv

from argsparseerror import ArgsParseError
from commands.add import Add
from commands.branch import Branch
from commands.checkout import Checkout
from commands.commit import Commit
from commands.help import Help
from commands.init import Init
from commitobject import CommitObject


class Main:
    _branch = re.compile(r'^(.*):(.*)')
    _selected_branch = re.compile(r'(.*?)\|')
    author = getpass.getuser()
    dir_path = './.goodgit'
    oper_dict = dict(init=Init, help=Help, add=Add, commit=Commit,
                     branch=Branch, checkout=Checkout)
    selected_branch = "master"
    branches = dict()

    def is_initiated(self):
        return os.path.exists(self.dir_path) and \
               os.path.exists(self.dir_path + '/main')

    def get_commit(self, commit_hash):
        if not commit_hash:
            return None

        with open(f'{self.dir_path}/commits/{commit_hash}_info') as f:
            s = f.readline()

        return CommitObject.parse(s, self)

    def _fill_branches(self):
        with open(self.dir_path + '/main') as f:
            for line in f:
                match = self._branch.match(line)
                if match:
                    self.branches[match.group(1)] = None
                    if len(match.groups()) == 2:
                        self.branches[match.group(1)] = self.get_commit(
                            match.group(2))
                else:
                    match = self._selected_branch.match(line)

                    if match:
                        self.selected_branch = match.group(1)

    def main(self):
        if len(argv) < 2:
            Help().execute(self, dict())
        else:
            if argv[1] != 'init' and not self.is_initiated():
                print('not a goodgit repository')
            else:
                if argv[1] != 'init':
                    self._fill_branches()

                command_name = argv[1]
                if command_name not in self.oper_dict:
                    Help().execute(self, dict())
                else:
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
