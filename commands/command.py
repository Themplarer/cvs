from repositorynotinitedexception import RepositoryNotInitedException


class Command:
    def configure(self, subparsers):
        pass

    def execute(self, repository, args, writer):
        pass


class RepositoryDependentCommand(Command):
    def execute(self, repository, args, writer):
        if not repository.is_initiated:
            writer.write('goodgit repository is not initiated!')
            raise RepositoryNotInitedException
