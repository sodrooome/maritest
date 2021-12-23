"""
Copyright 2021 A Job Thing Sdn Bhd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Initial code: Ryan Febriansyah, 20-12-2021
"""
from .client import Http


class Assert(Http):
    """
    Base class for collection assertion
    test. All of these listing method are implemented
    based on abstract method in Http class
    """

    def assert_is_ok(self, message: str):
        if self.response.status_code != 200:
            message = "The request didn't success"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_failed(self, message: str):
        if self.response.status_code == 200:
            message = "The request should be failed"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_headers(self, message: str):
        if not self.response.headers:
            message = "There's no headers in that request"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_content_type(self, message: str):
        # this one is much more specific
        # to body information
        if not self.response.headers["Content-Type"]:
            message = "Perhaps 'content-type' wasn't set"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_content_type_to_equal(self, value: str, message: str):
        # validate expected content-type
        # with actual result in response
        if value != self.response.headers["Content-Type"]:
            message = "The value of content-type doesn't match with the actual result"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_2xx_status(self, message: str):
        if 200 <= self.response.status_code < 300:
            return print(message, f"The status code was : {self.response.status_code}")
        else:
            message = "The status got 2xx"
            raise AssertionError(message)

    def assert_is_3xx_status(self, message: str):
        if not 300 <= self.response.status_code < 400:
            message = "The status not 3xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_is_4xx_status(self, message: str):
        if not 400 <= self.response.status_code < 500:
            message = "The status not 4xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_is_5xx_status(self, message: str):
        if not 500 <= self.response.status_code < 600:
            message = "The status not 5xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_is_has_content(self, message: str):
        if self.response.content:
            print(message, f"The content was => {self.response.content}")
        else:
            message = "There's no content in the body"
            raise AssertionError(message)

    def assert_is_has_json(self, message: str):
        if self.response.json:
            print(message, f"The JSON body was => {self.response.json}")
        else:
            message = "The request has no JSON object"
            raise AssertionError(message)

    def assert_is_has_text(self, message: str):
        if self.response.text:
            print(message, f"The request has text => {self.response.text}")
        else:
            message = "The request has no text object"
            raise AssertionError(message)

    def assert_status_code_in(self, status_code: str, message: str):
        expected_result = [str(code) for code in status_code]
        actual_result = str(self.response.status_code)
        if actual_result in expected_result:
            return print(message)
        else:
            message = "The expected status code didn't match with actual result"
            raise AssertionError(message)

    def assert_status_code_not_in(self, status_code: str, message: str):
        expected_result = [str(code) for code in status_code]
        actual_result = str(self.response.status_code)
        if actual_result not in expected_result:
            return print(message)
        else:
            message = (
                "The expected status code (actually) did matched with actual result"
            )
            raise AssertionError(message)

    def assert_json_to_equal(self, obj, message: str):
        if self.response.json() == obj:
            return print(message)
        else:
            message = "There's no object that match"
            raise AssertionError(message)

    def assert_text_to_equal(self, obj, message: str):
        if self.response.text == obj:
            return print(message)
        else:
            message = "There's no (text) object that match"
            raise AssertionError(message)

    def assert_content_to_equal(self, obj, message: str):
        if self.response.content == obj:
            return print(message)
        else:
            message = "There's no content that match"
            raise AssertionError(message)

    def assert_response_time(self, duration: int, message: str):
        if self.response.elapsed.total_seconds() <= duration:
            return print(message)
        else:
            message = "The duration exceeds the limit"
            raise AssertionError(message)

    def assert_is_text(self, obj: str, message: str):
        if self.response.text:
            return print(isinstance(obj, str)), message
        else:
            message = f"Str type doesn't match with {obj}"
            raise AssertionError(message)

    def assert_is_dict(self, obj: dict, message: str):
        if self.response.json:
            return print(isinstance(obj, dict)), message
        else:
            message = f"Dict type doesn't match with {obj}"
            raise AssertionError(message)

    # TODO: write assertion for validating JSON body
