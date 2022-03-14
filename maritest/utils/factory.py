import logging
from enum import Enum


get_specific_logger = logging.getLogger("Maritest Logger")


class LogEnum(str, Enum):
    """Enum class that represent for Log level"""

    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"


class Logger:
    """Private class for logger factory"""

    _logger = None

    @staticmethod
    def __set_logger(log_level: str = None):
        """
        Private method to create logger stream handler
        based on log_level argument. This method only
        accessible to call from static method, the entire
        method come handy to avoid repetitive or duplicate
        logging function when initialize in Http attribute
        """
        Logger._logger = get_specific_logger
        Logger._logger.propagate = False
        Logger._logger.setLevel(logging.DEBUG)

        logger_output = logging.StreamHandler()
        logger_output.setLevel(logging.DEBUG)

        logger_formatter = logging.Formatter(
            fmt="%(asctime)s | %(filename)s | %(funcName)s | %(message)s",
            datefmt="%d-%m-%Y %I:%M:%S",
        )

        logger_output.setFormatter(logger_formatter)
        Logger._logger.addHandler(logger_output)

        if log_level == LogEnum.INFO:
            Logger._logger.setLevel(logging.INFO)
        elif log_level == LogEnum.DEBUG:
            Logger._logger.setLevel(logging.DEBUG)
        elif log_level == LogEnum.WARNING:
            Logger._logger.setLevel(logging.WARNING)
        return Logger._logger

    @staticmethod
    def get_logger(log_level: str = None):
        if log_level is not None:
            return Logger.__set_logger(log_level=log_level)
