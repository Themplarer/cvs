#!/usr/bin/python3

import argparse

from commands.add import Add
from commands.branch import Branch
from commands.checkout import Checkout
from commands.cherry_pick import CherryPick
from commands.commit import Commit
from commands.diff import Diff
from commands.easter_eggs.credits import Credits
from commands.easter_eggs.joke import Joke
from commands.easter_eggs.remotes import Push, Pull, Fetch, Clone
from commands.init import Init
from commands.log import Log
from commands.merge import Merge
from commands.stash import Stash
from commands.status import Status
from commands.tag import Tag
from repository import Repository


def main():
    parser = argparse.ArgumentParser(description='works like the git!')
    subparsers = parser.add_subparsers(title='goodgit commands', metavar='')

    commands_list = [Init(), Add(), Commit(), Branch(), Checkout(), Status(),
                     Tag(), Stash(), Diff(), Log(), Merge(), CherryPick()]
    for i in commands_list:
        i.configure(subparsers)

    easter_eggs_list = [Credits(), Joke(), Push(), Pull(), Fetch(), Clone()]
    for i in easter_eggs_list:
        i.configure(subparsers)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        r = Repository()
        args.func(r, args)
        r.save_main_file()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
