import unittest
from maritest.utils.factory import Logger


# purpose to write this unittest
# only for coverage missing LoC
# in factory module
class TestFactoryLogger(unittest.TestCase):
    def test_get_logger_debug(self):
        get_logger = Logger.get_logger(
            url="https://github.com", method="GET", log_level="DEBUG"
        )
        self.assertTrue(get_logger)

    def test_get_logger_warning(self):
        get_logger = Logger.get_logger(
            url="https://github.com", method="GET", log_level="WARNING"
        )
        self.assertTrue(get_logger)


if __name__ == "__main__":
    unittest.main()
