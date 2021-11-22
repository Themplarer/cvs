from commands.command import Command


class Credits(Command):
    def configure(self, subparsers):
        subparsers.add_parser('credits').set_defaults(func=self.execute)

    def execute(self, caller, args):
        print('''
KHOROSHiy_git v.1.0
Copyright (c) 2021 Evgeny Khoroshavin (github.com/Themplarer)
All rights reserved

CVS project for Python course

Special thanks to Vladimir Zverev for 20 points''')
