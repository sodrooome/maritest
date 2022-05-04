__version__ = '0.5.0'


def get_version():
    return __version__  # pragma: no cover


def get_version_as_tuple():
    return tuple(map(int, __version__.split('.')))  # pragma: no cover
