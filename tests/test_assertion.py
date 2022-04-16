import unittest
from unittest.case import expectedFailure
from maritest.assertion import Assert


class TestHttpAssertion(unittest.TestCase):
    def test_assert_failed(self):
        # this test case supposed to be failed
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/postas",
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
        request.assert_has_content("yeah it has content")
        request.assert_has_json("yeah, it must be right?")
        request.assert_has_text("yeah it perhaps has text")
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
            "body": "cupiditate quo est a modi nesciunt soluta\nipsa voluptas error itaque dicta in\nautem qui minus "
            "magnam et distinctio eum\naccusamus ratione error aut",
        }
        expected_body_content = (
            b'{\n  "userId": 10,\n  "id": 100,\n  "title": "at nam consequatur ea '
            b'labore ea harum",\n  "body": "cupiditate quo est a modi nesciunt soluta\\nipsa '
            b"voluptas error itaque dicta in\\nautem qui minus magnam et distinctio "
            b'eum\\naccusamus ratione error aut"\n}'
        )
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
        request.assert_dict_to_equal(
            {"some_key": "some_value"}, "this one is a dict object"
        )
        request.assert_text_to_equal(b"", "this one is text object")

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
        request.assert_is_5xx_status("supposed to be fail, but not receive 5xx status")  # pragma: no cover

    def test_assert_3xx_status(self):
        request = Assert(
            method="GET",
            url="https://httpbin.org/status/301",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
            allow_redirects=False,
        )
        request.assert_is_3xx_status("This one must be 3xx status")
        self.assertFalse(request.allow_redirects)

    def test_assert_5xx_status(self):
        request = Assert(
            method="GET",
            url="https://httpstat.us/500",
            headers={"some_key": "some_value"},
            logger=False,
            allow_redirects=True,
        )
        request.assert_is_5xx_status("This one must be 5xx status")
        self.assertTrue(request.allow_redirects)

    def test_assert_proxies_3xx_status(self):
        request = Assert(
            method="GET",
            url="http://github.com",
            headers={},
            proxy={"https": "https://github.com"},
            retry=True,
        )
        request.assert_is_3xx_status(f"Moved with github proxy")
        self.assertTrue(request.response.status_code, 301)

    def test_assert_response_time_less(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/100",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_response_time_less("Shouldn't be exceed the limit")
        self.assertTrue(request.response.status_code, 200)

    def test_assert_expect_to_failed(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/100",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_expected_to_fail("This one is not failed, but must be pass")
        self.assertTrue(request.response.status_code, 200)

    def test_assert_tls_secure(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/1",
            headers={"some_key": "some_value"},
        )
        request.assert_tls_secure()  # check without input success message argument
        request.assert_tls_secure(message="Success")
        self.assertTrue(request.url.startswith("https://"))

    def test_assert_tls_insecure(self):
        request = Assert(
            method="GET",
            url="http://jsonplaceholder.typicode.com/posts/1",
            headers={"some_key": "some_value"},
        )
        request.assert_tls_secure()
        self.assertTrue(request.url.startswith("http://"))

    # TODO: find references to test socket-based
    # or certificate SSL without need to install
    @expectedFailure
    def test_assert_tls_not_valid(self):
        request = Assert(
            method="GET",
            url="httpa://jsonplaceholder.typicode.com/posts/1",
            headers={"some_key": "some_value"},
        )

    # im not sure why this test getting error,
    # since on the previous test was nothing happened
    @expectedFailure
    def test_assert_content_length(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/1",
            headers={"some_key": "some_value"},
        )
        request.assert_content_length()

    # below here is a collection of negative test scenarios
    # the opposite of the positive scenario in the assertion module
    # why would do this due to coverage all unexpected issue
    # that led to won't raise AssertionError
    @expectedFailure
    def test_assert_is_ok(self):
        request = Assert(
            method="GET",
            url="https://httpbin.org/status/404",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_is_ok(message="Not ok but success")

    @expectedFailure
    def test_assert_is_failed(self):
        request = Assert(
            method="GET",
            url="https://httpbin.org/status/200",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_is_failed(message="Supposed to be failed but okay")

    @expectedFailure
    def test_assert_expected_to_failed(self):
        request = Assert(
            method="GET",
            url="https://httpbin.org/status/404",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_expected_to_fail(message="Already failed the request")

    @expectedFailure
    def test_assert_response_time(self):
        request = Assert(
            method="GET",
            url="https://httpbin.org/status/200",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_response_time(duration=0.1, message="Should exceed the limit")

    @expectedFailure
    def test_assert_4xx_status_code(self):
        request = Assert(
            method="GET",
            url="https://httpbin.org/status/200",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_is_4xx_status(message="Should be on 4xx status code")

    @expectedFailure
    def test_assert_5xx_status_code(self):
        request = Assert(
            method="GET",
            url="https://httpbin.org/status/200",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_is_5xx_status(message="Should be on 5xx status code")

    @expectedFailure
    def test_assert_2xx_status_code(self):
        request = Assert(
            method="GET",
            url="https://httpbin.org/status/400",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_is_2xx_status(message="Should be on 2xx status code")

    @expectedFailure
    def test_assert_not_content_type(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        request.assert_content_type_to_equal(
            value="application/json", message="Content-type not equal"
        )

    @expectedFailure
    def test_assert_not_json_equal(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/100",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        expected_body = {"empty-key": "empty-value"}
        request.assert_json_to_equal(expected_body, "This one not equal with response")

    @expectedFailure
    def test_assert_not_content_equal(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts/100",
            headers={"some_key": "some_value"},
            proxies=None,
            logger=False,
        )
        expected_body_content = b'meu\\ratio ratio ratio"\n}'
        request.assert_content_to_equal(
            expected_body_content, "This one not equal with response"
        )

    @expectedFailure
    def test_response_time_more_that_duration(self):
        for index in range(5):
            request = Assert(
                method="GET",
                url=f"https://jsonplaceholder.typicode.com/posts/{index}",
                headers={},
                proxies=None,
                logger=False
            )
        request.assert_response_time_less(message="Response took much longer time")
        self.assertTrue(request.response.status_code, 200)

    @expectedFailure
    def test_assert_status_code_in(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={},
            proxies=None,
            logger=False,
        )
        request.assert_status_code_in(status_code=[404, 403], message="expected failed")

    @expectedFailure
    def test_assert_status_code_not_in(self):
        request = Assert(
            method="GET",
            url="https://httpstat.us/500",
            headers={"some_key": "some_value"},
            logger=False,
            allow_redirects=True,
        )
        request.assert_status_code_not_in(status_code=[200, 20], message="expected failed")

    @expectedFailure
    def test_invalid_dict_type(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={},
            proxies=None,
            logger=False,
        )
        request.assert_dict_to_equal(obj="string object", message="Shouldn't be matching")

    @expectedFailure
    def test_invalid_text_type(self):
        request = Assert(
            method="GET",
            url="https://jsonplaceholder.typicode.com/posts",
            headers={},
            proxies=None,
            logger=False,
        )
        request.assert_text_to_equal(obj={"key": "value"}, message="Shouldn't be matching")


if __name__ == "__main__":
    unittest.main()
