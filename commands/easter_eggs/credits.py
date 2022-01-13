from commands.command import Command


class Credits(Command):
    def configure(self, subparsers):
        subparsers.add_parser('credits').set_defaults(obj=self)

    def execute(self, repository, args, writer):
        writer.write('''
KHOROSHiy_git v.1.0
Copyright (c) 2021-2022 Evgeny Khoroshavin (github.com/Themplarer)
All rights reserved

CVS project for Python course

Special thanks to Vladimir Zverev for 20 points''')
