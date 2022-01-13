#!/usr/bin/python3

import argparse

from commands import *
from message_writer import ConsoleMessageWriter
from repository import Repository
from repositorynotinitedexception import RepositoryNotInitedException


def main():
    parser = argparse.ArgumentParser(description='works like the git!')
    subparsers = parser.add_subparsers(title='goodgit commands', metavar='')

    commands_list = [Init(), Add(), Commit(), Branch(), Checkout(), Status(),
                     Tag(), Stash(), Diff(), Log(), Merge(), CherryPick()]
    easter_eggs_list = [Credits(), Joke(), Push(), Pull(), Fetch(), Clone()]
    for i in commands_list + easter_eggs_list:
        i.configure(subparsers)

    args = parser.parse_args()
    if hasattr(args, 'obj'):
        r = Repository()
        w = ConsoleMessageWriter()

        try:
            args.obj.execute(r, args, w)
        except RepositoryNotInitedException:
            pass

        r.save_main_file()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
