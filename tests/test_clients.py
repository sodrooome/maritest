import unittest
from unittest.case import expectedFailure
from maritest.client import Http


class MockMethod(Http):
    # this is only way that testing
    # for method that supposed
    # to be implemented already
    def assert_is_ok(self):
        raise NotImplementedError

    def concrete_method(self):
        return True


class TestHttpClient(unittest.TestCase):
    def test_get_method(self):
        request = Http(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        self.assertEqual("GET", request.method)
        self.assertEqual(200, request.response.status_code)

    def test_post_method(self):
        request_body = {
            "userId": 1,
            "id": 1,
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
        }
        request = Http(
            method="POST",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies={"https": "https://google.com"},
            json=request_body,
            logger=False,
        )
        self.assertEqual("POST", request.method)
        self.assertEqual(201, request.response.status_code)
        self.assertEqual(None, request.proxies)

    def test_put_method(self):
        request_body = {
            "userId": 1,
            "id": 1,
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
        }
        request = Http(
            method="PUT",
            url="https://jsonplaceholder.typicode.com/posts/1",
            headers={"some_key": "some_value"},
            proxies=None,
            json=request_body,
            logger=False,
        )
        self.assertEqual("PUT", request.method)
        self.assertEqual(200, request.response.status_code)

    def test_patch_method(self):
        request_body = {
            "userId": 1,
            "id": 1,
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
        }
        request = Http(
            method="PATCH",
            url="https://jsonplaceholder.typicode.com/posts/1",
            headers={"some_key": "some_value"},
            proxies=None,
            json=request_body,
            logger=False,
        )
        self.assertEqual("PATCH", request.method)
        self.assertEqual(200, request.response.status_code)

    def test_delete_method(self):
        request = Http(
            method="DELETE",
            url="https://jsonplaceholder.typicode.com/posts/1",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        self.assertEqual("DELETE", request.method)
        self.assertEqual(200, request.response.status_code)

    # negative test for validate
    # "OPTIONS" method is supported or not
    # expected to fail
    @expectedFailure
    def test_options_method(self):
        request = Http(
            method="OPTIONS",
            url="https://jsonplaceholder.typicode.com/posts/1",
            headers={"some_key": "some_value"},
            proxies={"http": "http://google.com"},  # failed proxy
            logger=False,
        )

        self.assertRaises(NotImplementedError, request.method)

    def test_http_attribute(self):
        request = Http(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        self.assertIn("", request.__str__())  # this one only checking for string type?
        self.assertIn("", request.__repr__())
        self.assertEqual("https://jsonplaceholder.typicode.com/posts", request.url)
        self.assertEqual("GET", request.method)
        self.assertEqual({"some_key": "some_value"}, request.headers)
        self.assertTrue(request.suppress_warning)  # validate this param set to True
        self.assertTrue(request.logger)

    def test_mock_http_method(self):
        mock_method = MockMethod(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        self.assertTrue(mock_method.concrete_method())

    def test_abstract_http_method(self):
        # Http.__abstractmethods__ = set()

        request = Http(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            logger=False,
        )

        # intentionally to be failed because
        # we tested for abstractmethod in Http class
        # not the real assertion method in Assert class
        with self.assertRaises(NotImplementedError):
            request.assert_is_failed("failed")
            request.assert_is_ok("supposed to be ok, but failed")


if __name__ == "__main__":
    unittest.main()
