import unittest
from maritest.serializable import JsonSerializer


class TestJsonSerializable(unittest.TestCase):
    def test_basic_json(self):
        setup = JsonSerializer(object={"key": "value"})
        self.assertTrue(setup, {"key": "value"})
        self.assertIsInstance(setup, dict)

    def test_empty_object(self):
        setup = JsonSerializer(object={})
        self.assertTrue(setup, {})

    def test_array_json(self):
        json_object = {
            "key": "value",
            "properties": [{"key-1": "value-1", "option-1": "option-2"}],
            "emptyness": [],
            "key-2": "value-2",
        }
        setup = JsonSerializer(object=json_object)
        self.assertIsInstance(setup, dict)
        self.assertTrue(setup, json_object)


if __name__ == "__main__":
    unittest.main()
