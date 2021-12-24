import unittest
from unittest.case import expectedFailure
from maritest.assertion import Assert


class TestHttpAssertion(unittest.TestCase):
    @expectedFailure
    def test_assert_failed(self):
        # this test case supposed to be failed
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_is_failed("should be failed")
        request.assert_is_4xx_status("404 status perhaps?")

    def test_assert_success(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_is_2xx_status("Status was raised")
        request.assert_is_ok("it's okay")

    def test_assert_content_type(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_content_type_to_equal(
            "application/json; charset=utf-8", "sukses"
        )
        request.assert_is_content_type(
            f"The content type is {request.response.headers} "
        )

    def test_assert_response(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_is_has_content("yeah it has content")
        request.assert_is_has_json("yeah, it must be right?")
        request.assert_is_has_text("yeah it perhaps has text")
        request.assert_is_headers("HTTP headers it a must!")

    def test_assert_other_assertion(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_response_time(200, "should be not exceed the limit")
        request.assert_status_code_in(
            [200, 201], "should be exactly match with the status code"
        )
        request.assert_status_code_not_in([404, 403], "should not be in status code")

    def test_assert_to_equal(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/100",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        expected_body = {
            "userId": 10,
            "id": 100,
            "title": "at nam consequatur ea labore ea harum",
            "body": "cupiditate quo est a modi nesciunt soluta\nipsa voluptas error itaque dicta in\nautem qui minus magnam et distinctio eum\naccusamus ratione error aut",
        }
        expected_body_content = b'{\n  "userId": 10,\n  "id": 100,\n  "title": "at nam consequatur ea labore ea harum",\n  "body": "cupiditate quo est a modi nesciunt soluta\\nipsa voluptas error itaque dicta in\\nautem qui minus magnam et distinctio eum\\naccusamus ratione error aut"\n}'
        request.assert_json_to_equal(expected_body, "This one should be success")
        request.assert_content_to_equal(expected_body_content, "sukses")

    def test_assert_type_to_equal(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/100",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_is_dict({"some_key": "some_value"}, "this one is a dict object")
        request.assert_is_text(b"", "this one is text object")

    # TODO: write assertion test for 3xx and 5xx status code
    @expectedFailure
    def test_assert_other_status(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/postsa/100",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_is_3xx_status("supposed to be fail, but not receive 3xx status")
        request.assert_is_5xx_status("supposed to be fail, but not receive 5xx status")


if __name__ == "__main__":
    unittest.main()
