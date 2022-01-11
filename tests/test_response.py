import unittest
from maritest.response import Response


class TestHttpResponse(unittest.TestCase):
    def test_http_response_format(self):
        response = Response(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        response.retriever(format="json")
        response.retriever(format="multipart")
        response.retriever(format="text")

        # no redirection, just checking the other output
        response.history_response()

    def test_http_history_redirects(self):
        response = Response(
            method="GET",
            url="http://github.com/",
            headers={"some_key": "some_value"},
            allow_redirects=True,
            logger=False,
        )
        response.history_response()


if __name__ == "__main__":
    unittest.main()
