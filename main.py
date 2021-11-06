#!/usr/bin/python3

import argparse
import getpass
import re

from commands.add import Add
from commands.branch import Branch
from commands.checkout import Checkout
from commands.commit import Commit
from commands.init import Init
from commitobject import CommitObject
from utils import exists


class Main:
    _branch = re.compile(r'^(.*):(.*)')
    _selected_branch = re.compile(r'(.*?)\|')
    author = getpass.getuser()
    dir_path = './.goodgit'
    selected_branch = "master"
    branches = dict()

    def is_initiated(self):
        return exists(self.dir_path) and exists(self.dir_path + '/main')

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
        if self.is_initiated():
            self._fill_branches()


commands_list = [Init(), Add(), Commit(), Branch(), Checkout()]

if __name__ == '__main__':
    m = Main()
    m.main()
    parser = argparse.ArgumentParser(prog='test',
                                     description='works like the git!')
    subparsers = parser.add_subparsers(title='goodgit commands', required=True)
    for i in commands_list:
        i.configure(subparsers)

    args = parser.parse_args()
    args.func(m, args)
