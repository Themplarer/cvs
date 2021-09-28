class Commit:
    def __init__(self, message, diff, prev_commit):
        self.message = message
        self.diff = diff
        self.prev_commit = prev_commit
        self.hash = hash(diff)
