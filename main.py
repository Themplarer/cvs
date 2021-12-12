#!/usr/bin/python3

import argparse

from commands.add import Add
from commands.branch import Branch
from commands.checkout import Checkout
from commands.commit import Commit
from commands.easter_eggs.credits import Credits
from commands.easter_eggs.joke import Joke
from commands.init import Init
from commands.status import Status
from repository import Repository


def main():
    parser = argparse.ArgumentParser(description='works like the git!')
    subparsers = parser.add_subparsers(title='goodgit commands', metavar='')

    commands_list = [Init(), Add(), Commit(), Branch(), Checkout(), Status()]
    for i in commands_list:
        i.configure(subparsers)

    easter_eggs_list = [Credits(), Joke()]
    for i in easter_eggs_list:
        i.configure(subparsers)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(Repository(), args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
