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

Initial code: Ryan Febriansyah, 03-12-2021
"""

import logging
import requests
from requests.sessions import session


# For our purposes,
# its only supported 5 HTTP method
ALLOWED_METHODS = ["GET", "PUT", "POST", "DELETE", "PATCH"]


class Http:
    """
    This is a base class for HTTP client
    """

    def __init__(self, method: str, url: str, headers: dict, log: bool = None) -> None:
        # missing attributes :
        # session, certs, file, json, data
        self.method = method
        self.url = url
        self.headers = headers
        self.log = log
        self.timeout = None
        self.response = None

        # re-write this message
        # the output still returned as
        # interpolation format
        message = f"[DEBUG] HTTP Request {self.headers}, {self.timeout}"

        if requests is None:
            raise NotImplementedError(
                "Something error, perhaps requests package not installed?"
            )

        if log:
            logging.info(f"[INFO] HTTP Request {self.method} | {self.url}")
            logging.debug(msg=message)

        if self.headers is None:
            # enforcing headers alwasy
            # wrap themselves with dict type
            self.headers = {}

        if self.timeout is None:
            self.timeout = 10

        if self.method is None:
            self.method = method
        elif self.method not in [index for index in ALLOWED_METHODS]:
            return f"Currently that method not supported {self.method}"

        if self.response is None:
            self.response = requests.Response

        # wrap it our request
        # and prepare it first before
        # send it immediately
        request = requests.Request(
            method=self.method, url=self.url, headers=self.headers
        )
        prepare_request = request.prepare()

        try:
            with requests.Session() as s:
                self.response = s.send(request=prepare_request, timeout=self.timeout)
        except requests.exceptions.Timeout as e:
            # temporary using requests exception
            # TODO: make base class for custom exceptio
            raise Exception(f"HTTP Request was timeout {e}")
        except requests.exceptions.ConnectionError as e:
            raise Exception(f"HTTP Request was failed {e}")
        except Exception as e:
            raise Exception(f"Other exception was occur {e}")
        finally:
            pass

        logging.info(f"[INFO] HTTP Response {self.response.status_code}")
        logging.debug(f"[DEBUG] HTTP Response Header {self.response.headers}")

        return None

    def __str__(self) -> str:
        if self.method and self.url is not None:
            return f"You're using Maritest with HTTP Request {self.url} | {self.method}"

    def __repr__(self) -> str:
        return f"<Http:{self.method}=>{self.url}"

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.method == other.method
            and self.url == other.url
            and self.headers == other.headers
            and self.timeout == other.timeout
            and self.response == other.response
        )

    def __exit__(self):
        # exit the connection pooling
        # after send the final request
        self.response.close()

    # this one act as an
    # instances for assertion tests
    # that have similar function like in pytest, unittest
    # or in postman testscript. For example:
    # test_foo = Http().assert_is_ok()
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

    def assert_is_2xx_status(self, message: str):
        if self.response.status_code < 300:
            return print(message)
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
        if actual_result not in expected_result:
            message = "The expected status code didn't match with actual result"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_json_to_equal(self, obj, message: str):
        if self.response.json in [value for value in obj]:
            return print(message)
        else:
            message = "There's no object that match"
            raise AssertionError(message)

    def assert_text_to_equal(self, obj, message: str):
        if self.response.text in [value for value in obj]:
            return print(message)
        else:
            message = "There's no (text) object that match"
            raise AssertionError(message)

    def assert_content_to_equal(self, obj, message: str):
        if self.response.content in [value for value in obj]:
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

    # TODO: write assertion for validating JSON body