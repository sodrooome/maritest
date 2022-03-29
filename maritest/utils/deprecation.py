import functools
import warnings
from maritest.version import __version__
from typing import Any


def deprecated(message: str, version: str = None) -> Any:
    """
    Decorator utility to raise and given user warning
    about deprecated method or class in all maritest modules

    :param message: required argument, message for identifying
    what method or classes has been deprecated
    :param version: optional argument, what versioning numbers
    that going deprecated
    """
    if isinstance(message, str):

        def decorator_func(func):
            @functools.wraps(func)
            def deprecated_func(*args, **kwargs):
                if version is not None:
                    warnings.warn(
                        f"This method already deprecated since {version} version, please use {message} method instead",
                        DeprecationWarning,
                        stacklevel=2,
                    )
                    warnings.simplefilter("always", DeprecationWarning)
                else:
                    # just in case that if im forgot to put deprecated
                    # versioning number, use latest version instead
                    warnings.warn(
                        f"This method already deprecated since {__version__} version, please use {message} method "
                        f"instead ",
                        DeprecationWarning,
                        stacklevel=2,
                    )
                    warnings.simplefilter("always", DeprecationWarning)
                return func(*args, **kwargs)

            return deprecated_func

        return decorator_func
    else:
        raise TypeError("message or reason must be string object")
