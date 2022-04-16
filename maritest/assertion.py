import json
from typing import Optional
from .client import Http


class Assert(Http):
    """
    Base class for collection assertion
    test. All of these listing method are implemented
    based on abstract method in Http class
    """

    def assert_is_ok(self, message: str):
        """Assert request is ok"""
        if self.response.status_code != 200:
            message = "The request didn't success"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_failed(self, message: str):
        """Assert request is failed"""
        if self.response.status_code == 200:
            message = "The request should be failed"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_headers(self, message: str):
        """Assert response has headers"""
        if not self.response.headers:
            message = "There's no headers in that request"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_content_type(self, message: str):
        """Assert response has content-type header"""
        # this one is much more specific
        # to body information
        if not self.response.headers["Content-Type"]:
            message = "Perhaps 'content-type' wasn't set"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_content_type_to_equal(self, value: str, message: str):
        """Assert content-type header equal to expected result"""
        # validate expected content-type
        # with actual result in response
        if value != self.response.headers["Content-Type"]:
            message = "The value of content-type doesn't match with the actual result"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_2xx_status(self, message: str):
        """Assert response in range 2xx status code"""
        if not 200 <= self.response.status_code < 300:
            message = "The status not 2xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_is_3xx_status(self, message: str):
        """Assert response in range 3xx status code"""
        if not 300 <= self.response.status_code < 400:
            message = "The status not 3xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_is_4xx_status(self, message: str):
        """Assert response in range 4xx status code"""
        if not 400 <= self.response.status_code < 500:
            message = "The status not 4xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_is_5xx_status(self, message: str):
        """Assert response in range 5xx status code"""
        if not 500 <= self.response.status_code < 600:
            message = "The status not 5xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_has_content(self, message: str):
        """Assert response has content"""
        if self.response.content:
            print(message, f"The content was => {self.response.content}")
        else:
            message = "There's no content in the body"  # pragma: no cover
            raise AssertionError(message)

    def assert_has_json(self, message: str):
        """Assert response has JSON body"""
        if self.response.json:
            print(message, f"The JSON body was => {self.response.json}")
        else:
            message = "The request has no JSON object"  # pragma: no cover
            raise AssertionError(message)

    def assert_has_text(self, message: str):
        """Assert response has text"""
        if self.response.text:
            print(message, f"The request has text => {self.response.text}")
        else:
            message = "The request has no text object"  # pragma: no cover
            raise AssertionError(message)

    def assert_status_code_in(self, status_code: int, message: str):
        """Assert response status code in range expected result"""
        expected_result = [str(code) for code in status_code]
        actual_result = str(self.response.status_code)
        if actual_result in expected_result:
            return print(message)
        else:
            message = "The expected status code didn't match with actual result"  # pragma: no cover
            raise AssertionError(message)

    def assert_status_code_not_in(self, status_code: int, message: str):
        """Assert response status code not in range expected result"""
        expected_result = [str(code) for code in status_code]
        actual_result = str(self.response.status_code)
        if actual_result not in expected_result:
            return print(message)
        else:
            message = (
                "The expected status code (actually) did matched with actual result"  # pragma: no cover
            )
            raise AssertionError(message)

    def assert_json_to_equal(self, obj, message: str):
        """Assert JSON response equal to expected result"""
        response_data = self.response.json()
        dumps = json.dumps(response_data, sort_keys=False)
        loads = json.loads(dumps)
        if loads == obj:
            return print(message)
        else:
            message = "There's no object that match"
            raise AssertionError(message)

    def assert_content_to_equal(self, obj, message: str):
        if self.response.content == obj:
            return print(message)
        else:
            message = "There's no content that match"
            raise AssertionError(message)

    def assert_response_time(self, duration: int, message: str):
        """Assert response time is less with set of duration"""
        if self.response.elapsed.total_seconds() <= duration:
            return print(message)
        else:
            message = "The duration exceeds the limit"
            raise AssertionError(message)

    def assert_text_to_equal(self, obj: Optional[bytes], message: str):
        if self.response.text:
            return print(isinstance(obj, str)), message
        else:
            message = f"Str type doesn't match with {obj}"  # pragma: no cover
            raise AssertionError(message)

    def assert_dict_to_equal(self, obj: dict, message: str):
        if self.response.json:
            return print(isinstance(obj, dict)), message
        else:
            message = f"Dict type doesn't match with {obj}"  # pragma: no cover
            raise AssertionError(message)

    def assert_response_time_less(self, message: str):
        """Assert response time is less with maximum duration"""
        # this one actually inspired from postman
        # collection test script about getting response
        # whenever calling an API
        max_duration = 200
        if self.response.elapsed.total_seconds() <= max_duration:
            return print(message)
        else:
            message = "The duration exceeds the limit"  # pragma: no cover
            raise AssertionError(message)

    def assert_expected_to_fail(self, message: str):
        """Assert request expected to be failed"""
        if self.response.status_code in [200, 201]:
            return print(message)
        else:
            message = "Expected to be failed, but got success instead"
            raise AssertionError(message)

    def assert_content_length(self, message: str = None):
        """Assert response has content-length header"""
        if message is None:
            if self.response.headers["Content-Length"]:
                message = "Request have content-length"
                return print(message)
            else:
                message = "Request doesn't have content-length"
                raise AssertionError(message)
        else:
            return print(message)

    def assert_tls_secure(self, message: str = None):
        """Assert request was TLS secure or invalid"""
        if message is None:
            if self.url.startswith("https://"):
                message = "Your connection to the request was secure"
                return print(message)
            if self.url.startswith("http://"):
                message = "Your connection to the request wasn't secure"
                return print(message)
        else:
            return print(message)

    # TODO: write assertion for validating JSON body
