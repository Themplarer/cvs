class MessageWriter:
    """Logging abstraction"""
    def write(self, *args):
        """Does nothing without realisation"""
        pass


class ConsoleMessageWriter(MessageWriter):
    """Realisation of logger using stdout"""
    def write(self, *args):
        """Writes given objects to the console separating by space and ending
        by newline"""
        print(*args)


class FileMessageWriter(MessageWriter):
    """Realisation of logger using file output"""
    def __init__(self, path):
        self._file = path

    def write(self, *args):
        """Writes given objects to the file separating by space and ending
        by newline"""
        with self._file.open(mode='a', encoding='utf-8') as f:
            is_first_line = True
            args_iter = iter(args)

            try:
                while True:
                    arg = next(args_iter)
                    if not is_first_line:
                        f.write(' ')

                    is_first_line = False
                    f.write(str(arg))
            except StopIteration:
                f.write('\n')
