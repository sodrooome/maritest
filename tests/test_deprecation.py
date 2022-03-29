import unittest
from maritest.utils.deprecation import deprecated


@deprecated(message="method deprecated", version=None)
def method_deprecated():
    return "this method already deprecated without version"


@deprecated(message="method deprecated", version="0.4.0")
def method_deprecated_with_version():
    return "this method already deprecated"


class TestDeprecationHelper(unittest.TestCase):
    def test_deprecation_version(self):
        self.assertTrue(method_deprecated_with_version(), "deprecated with version")
        self.assertEqual(
            method_deprecated_with_version(), "this method already deprecated"
        )

        # unsure whether this assertion its correct
        # or not, what i wanted is test the decorator input
        self.assertTrue(
            method_deprecated_with_version.__closure__[1].cell_contents, "0.4.0"
        )

    def test_deprecation_without_version(self):
        self.assertTrue(method_deprecated(), "deprecated with version")
        self.assertEqual(
            method_deprecated(), "this method already deprecated without version"
        )
        self.assertTrue(method_deprecated.__closure__[1].cell_contents, None)


if __name__ == "__main__":
    unittest.main()
