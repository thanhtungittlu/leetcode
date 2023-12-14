from nanoid import generate
import inspect


def generate_nano_id(short=False):
    return generate("1234567890abcxsz", size=12) if short else generate()


class SingletonArgs(type):
    """Singleton that keep single instance for single set of arguments. E.g.:
    assert SingletonArgs('spam') is not SingletonArgs('eggs')
    assert SingletonArgs('spam') is SingletonArgs('spam')
    """

    _instances = {}
    _init = {}

    def __init__(cls, name, bases, dct):
        super().__init__(cls)
        cls._init[cls] = dct.get("__init__", None)

    def __call__(cls, *args, **kwargs):
        init = cls._init[cls]
        if init is not None:
            key = (
                cls,
                frozenset(
                    [
                        x.__str__()
                        for x in inspect.getcallargs(
                            init, None, *args, **kwargs
                        ).items()
                    ]
                ),
            )
        else:
            key = cls

        if key not in cls._instances:
            cls._instances[key] = super(SingletonArgs, cls).__call__(*args, **kwargs)
        return cls._instances[key]
