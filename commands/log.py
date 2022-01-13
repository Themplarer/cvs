from commands.command import RepositoryDependentCommand


class Log(RepositoryDependentCommand):
    _help_string = 'Writes latest commits from head'

    def configure(self, subparsers):
        log = subparsers.add_parser('log', help=self._help_string)
        log.set_defaults(obj=self)
        log.add_argument('count', help='number of commits to write about')

    def execute(self, repository, args, writer):
        super().execute(repository, args, writer)

        commit = repository.branches['head']
        n = args.count
        for i in range(int(args.count)):
            writer.write(f'{i}: {commit.hash} "{commit.message}"')

            if commit.prev_commits:
                commit = commit.prev_commits[0]
            else:
                n = i + 1
                break

        writer.write(f'Total: {n} commits')
