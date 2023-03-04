import json

from typing import Any, Optional
from lxml import html

from .client import Http
from .utils.dict_lookups import keys_in_dict


class Assert(Http):
    """
    Base class for collection assertion
    test. All of these listing method are implemented
    based on abstract method in Http class
    """

    def assert_is_ok(self, message: str):
        """Assert request is ok"""
        if self.response.status_code != 200:
            return AssertionError("The request didn't success")
        return message

    def assert_is_failed(self, message: str):
        """Assert request is failed"""
        if self.response.status_code == 200:
            raise AssertionError("The request should be failed")
        return message

    def assert_is_headers(self, message: str):
        """Assert response has headers"""
        if not self.response.headers:
            raise AssertionError("There's no headers in that request")
        return message

    def assert_is_content_type(self, message: str):
        """Assert response has content-type header"""
        # this one is much more specific
        # to body information
        if not self.response.headers["Content-Type"]:
            raise AssertionError("Perhaps 'content-type' wasn't set")
        return message

    def assert_content_type_to_equal(self, value: str, message: str):
        """Assert content-type header equal to expected result"""
        # validate expected content-type
        # with actual result in response
        if value != self.response.headers["Content-Type"]:
            raise AssertionError(
                "The value of content-type doesn't match with the actual result"
            )
        return message

    def assert_is_2xx_status(self, message: str):
        """Assert response in range 2xx status code"""
        if not 200 <= self.response.status_code < 300:
            raise AssertionError("The status not 2xx")
        return message

    def assert_is_3xx_status(self, message: str):
        """Assert response in range 3xx status code"""
        if not 300 <= self.response.status_code < 400:
            raise AssertionError("The status not 3xx")
        return message

    def assert_is_4xx_status(self, message: str):
        """Assert response in range 4xx status code"""
        if not 400 <= self.response.status_code < 500:
            raise AssertionError("The status not 4xx")
        return message

    def assert_is_5xx_status(self, message: str):
        """Assert response in range 5xx status code"""
        if not 500 <= self.response.status_code < 600:
            raise AssertionError("The status not 5xx")
        return message

    def assert_has_content(self, message: str):
        """Assert response has content"""
        if self.response.content:
            return message, f"The content was => {self.response.content}"
        raise AssertionError("There's no content in the body")

    def assert_has_json(self, message: str):
        """Assert response has JSON body"""
        if self.response.json:
            return message, f"The JSON body was => {self.response.json}"
        raise AssertionError("The request has no JSON object")

    def assert_has_text(self, message: str):
        """Assert response has text"""
        if self.response.text:
            return message, f"The request has text => {self.response.text}"
        raise AssertionError("The request has no text object")

    def assert_status_code_in(self, status_code: list[int], message: str):
        """Assert response status code in range expected result"""
        expected_result = [str(code) for code in status_code]
        actual_result = str(self.response.status_code)
        if actual_result in expected_result:
            return message
        raise AssertionError("The expected status code didn't match with actual result")

    def assert_status_code_not_in(self, status_code: list[int], message: str):
        """Assert response status code not in range expected result"""
        expected_result = [str(code) for code in status_code]
        actual_result = str(self.response.status_code)
        if actual_result not in expected_result:
            return message
        raise AssertionError(
            "The expected status code (actually) did matched with actual result"
        )

    def assert_json_to_equal(self, obj, message: str):
        """Assert JSON response equal to expected result"""
        response_data = self.response.json()
        dumps = json.dumps(response_data, sort_keys=False)
        loads = json.loads(dumps)
        if loads == obj:
            return message
        raise AssertionError("There's no object that match")

    def assert_content_to_equal(self, obj, message: str):
        if self.response.content == obj:
            return message
        raise AssertionError("There's no content that match")

    def assert_response_time(self, duration: int, message: str):
        """Assert response time is less with set of duration"""
        if self.response.elapsed.total_seconds() <= duration:
            return message
        raise AssertionError("The duration exceeds the limit")

    def assert_text_to_equal(self, obj: Optional[bytes], message: str):
        if self.response.text:
            return isinstance(obj, str), message
        raise AssertionError(f"Str type doesn't match with {obj}")

    def assert_dict_to_equal(self, obj: dict, message: str):
        if self.response.json:
            return isinstance(obj, dict), message
        raise AssertionError(f"Dict type doesn't match with {obj}")

    def assert_response_time_less(self, message: str):
        """Assert response time is less with maximum duration"""
        # this one actually inspired from postman
        # collection test script about getting response
        # whenever calling an API
        max_duration = 200
        if self.response.elapsed.total_seconds() <= max_duration:
            return message
        raise AssertionError("The duration exceeds the limit")

    def assert_expected_to_fail(self, message: str):
        """Assert request expected to be failed"""
        if self.response.status_code in [200, 201]:
            return message
        raise AssertionError("Expected to be failed, but got success instead")

    def assert_content_length(self, message: str = None):
        """Assert response has content-length header"""
        if message is None:
            if self.response.headers["Content-Length"]:
                message = "Request have content-length"
                return message
            else:
                message = "Request doesn't have content-length"
                raise AssertionError(message)
        else:
            return message

    def assert_tls_secure(self, message: str = None):
        """Assert request was TLS secure or invalid"""
        if message is None:
            if self.url.startswith("https://"):
                message = "Your connection to the request was secure"
                return message
            if self.url.startswith("http://"):
                message = "Your connection to the request wasn't secure"
                return message
        else:
            return AssertionError("It seems you've inputted invalid URLs")

    def assert_keys_in_response(self, keys, message: str = None):
        """Assert request if keys has in JSON response"""
        key_in_response = self.response.json()
        expected_keys = keys_in_dict(lookup=key_in_response, keys=keys)
        if not expected_keys:
            raise AssertionError("There's no any key in JSON response")
        return message

    def assert_xpath_data(self, query_path: str, expected_data: Any, message: str):
        """Assert that expected data contains in XPATH response"""
        # this assertion came up after reading built-in
        # assertion in Assertible documentation, please read here:
        # https://assertible.com/docs/guide/assertions#assert-xml/html-data
        response_content = self.response.content
        parsing = html.fromstring(response_content)
        find_element = parsing.xpath(query_path)
        if find_element != expected_data:
            raise AssertionError("Data not equals or not found within XPATH response")
        return message

    def assert_link_data(self, expected_values: str = None, message: str = None):
        """Assert for checking href link attribute in HTTP response"""
        response_content = self.response.content
        parsing = html.fromstring(response_content)
        url_link = parsing.xpath("//a/@href")
        for find_element in url_link:
            if (
                find_element.startswith(("https", "http"))
                and find_element not in expected_values
            ):
                raise AssertionError(
                    "Link not equals or not found within content response"
                )
        return message
