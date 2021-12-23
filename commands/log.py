from commands.command import Command


class Log(Command):
    _help_string = 'Writes latest commits from head'

    def configure(self, subparsers):
        log = subparsers.add_parser('log', help=self._help_string)
        log.set_defaults(func=self.execute)
        log.add_argument('count', help='number of commits to write about')

    def execute(self, repository, args):
        commit = repository.branches['head']
        n = args.count
        for i in range(int(args.count)):
            print(f'{i}: {commit.hash} "{commit.message}"')

            if commit.prev_commits:
                commit = commit.prev_commits[0]
            else:
                n = i + 1
                break

        print(f'Total: {n} commits')
