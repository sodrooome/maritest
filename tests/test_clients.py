import unittest
from abc import ABC
from unittest.case import expectedFailure
from maritest.client import Http
from maritest.custom_auth import (
    BasicAuth,
    DigestAuth,
    BasicAuthToken,
    ApiKeyAuth,
    BearerAuth,
)


class MockMethod(Http, ABC):
    # this is only way that testing
    # for method that supposed
    # to be implemented already
    def assert_is_ok(self, message: str):
        raise NotImplementedError

    @staticmethod
    def concrete_method():
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
            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut "
            "quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
        }
        request = Http(
            method="POST",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            json=request_body,
            logger=False,
            timeout=True,
        )
        self.assertEqual("POST", request.method)
        self.assertEqual(201, request.response.status_code)
        self.assertEqual(None, request.proxy)

    def test_put_method(self):
        request_body = {
            "userId": 1,
            "id": 1,
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut "
            "quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
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
            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut "
            "quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
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

        self.assertRaises(NotImplementedError, request.method)  # pragma: no cover

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
        self.assertFalse(request.suppress_warning)  # validate this param set to True
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

    def test_http_basic_auth(self):
        request = Http(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            logger=False,
            auth=BasicAuth("this is some username", "this is some password"),
        )
        assert request.response.status_code == 200

    def test_http_digest_auth(self):
        request = Http(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            logger=False,
            auth=DigestAuth("some username", "some password"),
        )
        assert request.response.status_code == 200

    def test_http_token_auth(self):
        request = Http(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            logger=False,
            auth=BasicAuthToken(token="some key of token"),
        )
        assert request.response.status_code == 200

    def test_http_bearer_auth(self):
        request = Http(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            logger=False,
            auth=BearerAuth(token="some bearer token"),
        )
        assert request.response.status_code == 200

    def test_http_api_auth(self):
        request = Http(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            logger=False,
            auth=ApiKeyAuth(key="some key", value="some value", add_to="headers"),
        )
        assert request.response.status_code == 200

    def test_send_data(self):
        # hacky way: possibility found a bug (raise 400 status)
        # when send request files with headers inside
        # right now only set headers without key-value
        request = Http(
            method="POST",
            url="https://httpbin.org/post",
            headers={},
            data={"some key": "some value"},
            timeout=True,
        )
        self.assertEqual(200, request.response.status_code)

    def test_files_data(self):
        request = Http(
            method="POST",
            url="https://httpbin.org/post",
            headers={},
            files={"file": ("report.csv", "some,data,to,send\nanother,row,to,send\n")},
            timeout=True,
        )
        self.assertEqual(200, request.response.status_code)

    def test_url_with_params(self):
        payload_params = {"key1": "value1", "key2": "value2"}
        request = Http(
            method="GET",
            url="https://httpbin.org/get",
            headers={},
            timeout=False,
            params=payload_params,
        )

        expected_url = "https://httpbin.org/get?key1=value1&key2=value2"
        self.assertEqual(200, request.response.status_code)
        self.assertEqual(request.response.url, expected_url)
        self.assertTrue(request.url, expected_url)

    def test_url_with_params_data(self):
        payload_params = {"key1": "value1", "key2": "value2"}
        payload_data = {"key-1": "value-1"}
        request = Http(
            method="POST",
            url="https://httpbin.org/post",
            headers={"content-type": "application/json"},
            timeout=False,
            params=payload_params,
            data=payload_data,
        )

        expected_url = "https://httpbin.org/get?key1=value1&key2=value2"
        self.assertEqual(200, request.response.status_code)
        self.assertTrue(request.url, expected_url)

    def test_proxies_request(self):
        request = Http(
            method="GET",
            url="http://github.com",
            headers={},
            proxy={"https": "https://github.com"},
            retry=True,
        )
        self.assertTrue(request.response.status_code, 200)

    def test_suppress_warning_on(self):
        request = Http(
            method="GET",
            url="https://httpbin.org/stream/20",
            headers={},
            logger=True,
            supress_warning=True,
        )
        self.assertTrue(request.suppress_warning, True)
        self.assertTrue(request.response.status_code, 200)

    def test_suppress_warning_off(self):
        request = Http(
            method="GET",
            url="https://httpbin.org/stream/20",
            headers={},
            logger=True,
            supress_warning=False,
        )
        self.assertFalse(request.suppress_warning, False)
        self.assertTrue(request.response.status_code, 200)

    @expectedFailure
    def test_proxy_with_http(self):
        request = Http(
            method="GET",
            url="https://httpbin.org/stream/20",
            headers={},
            logger=True,
            proxy={"http": "http://httpbin.org/stream/20"},
        )
        self.assertTrue(request.proxy, True)  # pragma: no cover
        self.assertEqual(request.proxy.keys(), "http")  # pragma: no cover

    def test_send_json_argument(self):
        json_payload = {"key": "value", "array": [{"json": "array"}, 0]}
        request = Http(
            method="POST",
            url="https://httpbin.org/post",
            headers={},
            logger=True,
            json=json_payload,
        )
        self.assertTrue(request.response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
