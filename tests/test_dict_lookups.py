import unittest
from maritest.utils.dict_lookups import keys_in_dict


class TestDictLookupUtils(unittest.TestCase):
    def test_search_simple_dict(self):
        data = {"key": "value", "key1": "value1"}
        search = keys_in_dict(lookup=data, keys=["key"])
        self.assertTrue(search)

    def test_nested_dict(self):
        data = {
            "Liverpool": {
                "Midfield": {
                    "Henderson": "backpass",
                    "Thiago": "maestro",
                    "Fabinho": "better than fred",
                }
            }
        }
        search_one = keys_in_dict(lookup=data, keys=["Liverpool", "Midfield"])
        search_two = keys_in_dict(lookup=data, keys=["Liverpool", "Midfield", "Thiago"])
        self.assertTrue(search_one)
        self.assertTrue(search_two)

    @unittest.expectedFailure
    def test_invalid_argument(self):
        data = [{"key": "value", "key1": "value1"}]
        keys_in_dict(lookup=data, keys=["key"])

    def test_return_false_search(self):
        data = {"key": "value", "key1": "value1"}
        search = keys_in_dict(lookup=data, keys=["Liverpool"])
        self.assertFalse(search)


if __name__ == "__main__":
    unittest.main()
