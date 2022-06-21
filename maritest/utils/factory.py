import logging
import requests
from enum import Enum


class LogEnum(str, Enum):
    """Enum class that represent for Log level"""

    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"


class HttpHandler(logging.Handler):
    def __init__(self, url: str, method: str, disabled: bool = False):
        """Constructor for construct custom HTTP Handler

        :param url: HTTP target that will be logging
        :param method: HTTP method that represent action to takes
        :param disabled: suppress HTTP response log if tend to disabled,
            otherwise it will shown in command-line
        """
        self.url = url
        self.method = method

        # potentially redundant attribute with `silent`
        # keep in mind: that these 2 attributes has
        # same functionality with slightly different
        # when HTTP target was called and emitted
        self.disabled = disabled

        super().__init__()

    def emit(self, record):
        """
        Sub-classes from `logging.Handler` that emitted
        url response based on relevant HTTP method. It will
        receive as record from HTTP target and formatted (if any)
        """
        http_log = self.format(record=record)

        # im not sure if this needed or not
        _ = requests.Request(method=self.method, url=self.url, data=http_log)

        if not self.disabled:
            print(http_log)


class Logger:
    """Private class for logger factory"""

    @staticmethod
    def __set_logger(
        url: str, method: str, log_level: str = None, silent: bool = False
    ):
        """
        Private method to create logger stream handler
        based on log_level argument. This method only
        accessible to call from static method, the entire
        method come handy to avoid repetitive or duplicate
        logging function when initialize in Http attribute

        :param url: HTTP target that will be logging
        :param method: HTTP method that represent action to takes
        :param log_level: set level for logging HTTP, argument
            value must be same with Enum class
        :param silent: suppress HTTP response log, if disabled
            then it will send as file log (maritest.log) if not,
            then it will shown as STDOUT
        """
        get_specific_logger = logging.getLogger("Maritest Logger")

        logger_formatter = logging.Formatter(
            fmt="%(asctime)s : %(filename)s : %(funcName)s : %(message)s",
            datefmt="%d-%m-%Y %I:%M:%S",
        )

        http_handler = HttpHandler(url=url, method=method, disabled=False)

        if not silent:
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            http_handler.setFormatter(logger_formatter)
            get_specific_logger.addHandler(http_handler)
            get_specific_logger.propagate = False
        else:
            logger_file = logging.FileHandler("maritest.log")
            logger_file.setFormatter(logger_formatter)
            get_specific_logger.addHandler(logger_file)
            get_specific_logger.propagate = False

        # same with this expression, do i need
        # keep this since the default of setLevel
        # will set into static values while initiate
        # in Http logger attribute
        if log_level == LogEnum.INFO:
            get_specific_logger.setLevel(logging.INFO)
        elif log_level == LogEnum.DEBUG:
            get_specific_logger.setLevel(logging.DEBUG)
        elif log_level == LogEnum.WARNING:
            get_specific_logger.setLevel(logging.WARNING)
        return get_specific_logger

    @staticmethod
    def get_logger(url: str, method: str, log_level: str = None, silent: bool = None):
        if log_level is not None:
            return Logger.__set_logger(
                url=url, method=method, log_level=log_level, silent=silent
            )
