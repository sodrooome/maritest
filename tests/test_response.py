import unittest
from maritest.response import Response


class TestHttpResponse(unittest.TestCase):
    def test_http_response_format(self):
        response = Response(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/1",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        response.retriever(fmt="json")
        response.retriever(fmt="content")
        response.retriever(fmt="text")

        # no redirection, just checking the other output
        response.history_response()
        response.http_response()

    def test_http_history_redirects(self):
        response = Response(
            method="GET",
            url="http://github.com/",
            headers={},
            allow_redirects=True,
            logger=True,
        )
        response.history_response()

    @unittest.expectedFailure
    def test_invalid_format_argument(self):
        response = Response(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/1",
            headers={},
            proxies=None,
            logger=False,
        )
        response.retriever(fmt="headers")

    @unittest.expectedFailure
    def test_invalid_type_argument(self):
        response = Response(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/1",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        response.retriever(fmt=1234)


if __name__ == "__main__":
    unittest.main()
