import sys


def with_argv(content):
    def decorator(wrapped):
        def wrapper(*args, **kwargs):
            original = sys.argv
            sys.argv = ["program"] + content

            wrapped(*args, **kwargs)

            sys.argv = original

        return wrapper

    return decorator


def auto_parse(wrapped):
    def wrapper(self, *args, **kwargs):
        self.config = self.parser.parse()

        wrapped(self, *args, **kwargs)

    return wrapper
