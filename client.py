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
import warnings
import urllib3
from requests.sessions import session
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from contextlib import contextmanager

# For our purposes,
# its only supported 5 HTTP method
ALLOWED_METHODS = ["GET", "PUT", "POST", "DELETE", "PATCH"]

get_specific_logger = logging.getLogger("Maritest Logger")


# TODO: separate this function calls
@contextmanager
def disable_warnings():
    # thanks stack overflow see at: https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning
    # -unverified-https-request-is-being-made-in-pytho
    with warnings.catch_warnings():
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        yield None


def response_hook(response: requests.Response, *args, **kwargs):
    return response.raise_for_status(), *args, kwargs


class Http:
    """
    This is a base class for HTTP client
    """

    def __init__(
        self,
        method: str,
        url: str,
        headers: dict,
        allow_redirects: bool = None,
        logger: bool = True,
        event_hooks: bool = False,
        retry: bool = True,
        supress_warning: bool = True,
        **kwargs,
    ) -> None:
        """
        Constructur for request HTTP target, with
        several parameter to construct it :
        :param method: HTTP method verb, string type
        :param url: base url for HTTP target, string type
        :param headers: HTTP content headers, by default always
        set to dict object
        :param allow_redirects: Enable redirection to other
        HTTP target if previous one wasn't respond it. set None
        :param logger: Logger stream handler with formatted
        output of message, by default set True
        :param event_hooks: Given valid response, by default
        set to False
        :param retry: Enable retry mechanism with default total
        attempts up-to 3, by default set to True
        :param suppress_warning: Verification of SSL certificate, if
        set True, will suppressed warning message
        :param kwargs: given by keyword argument
        Returned as HTTP response
        """
        # missing attributes :
        # session, certs, file, json, data
        self.method = method
        self.url = url
        self.headers = headers

        if logger:
            self.logger = get_specific_logger
            self.logger.propagate = False
            self.logger.setLevel(logging.DEBUG)

            # handler the logging event
            # and write the standart output
            logger_output = logging.StreamHandler()
            logger_output.setLevel(logging.DEBUG)

            # format the standart output
            # with timestamp of event, class name and levels
            logger_formatter = logging.Formatter(
                fmt="%(asctime)s : %(name)s : %(funcName)s : %(message)s",
                datefmt="%d-%m-%Y %I:%M:%S",
            )

            logger_output.setFormatter(logger_formatter)
            self.logger.addHandler(logger_output)
        else:
            # if logger wasn't setup
            # only get the specific logger name
            self.logger = get_specific_logger

        self.timeout = None
        self.response = None
        self.json = None
        self.data = None
        self.params = None
        self.files = None
        self.proxies = None
        self.allow_redirects = allow_redirects
        self.stream = False
        self.cert = None
        self.suppress_warning = supress_warning  # by default set to True due staging environment
        self.verify = None

        # re-write this message
        # the output still returned as
        # interpolation format
        message = f"[DEBUG] HTTP Request {self.headers}, {self.timeout}"

        if requests is None:
            raise NotImplementedError(
                "Something error, perhaps requests package not installed?"
            )

        if logger:
            # why the heck am i validate
            # the logger twice ??
            self.logger.info(f"[INFO] HTTP Request {self.method} | {self.url}")
            self.logger.debug(msg=message)

        if self.headers is None:
            # enforcing headers alwasy
            # wrap themselves with dict type
            self.headers = {}

        if self.timeout is None:
            self.timeout = 10

        if self.method is None:
            self.method = method

        if self.method not in [index for index in ALLOWED_METHODS]:
            print(f"Currently that method not supported {self.method}")

        if self.response is None:
            self.response = requests.Response

        if self.data is None:
            self.data = {}

        if self.params is None:
            self.params = {}

        if self.proxies is None:
            self.proxies = {}

        if supress_warning:
            self.suppress_warning = True
            self.logger.warning("[WARNING] SSL verification status is disabled")
        else:
            # move disable warnings in here
            disable_warnings()
            self.suppress_warning = False
            self.logger.info("[INFO] SSL verification status is enabled")

        # wrap it our request
        # and prepare it first before
        # send it immediately
        request = requests.Request(
            method=self.method,
            url=self.url,
            headers=self.headers,
            params=self.params,
            data=self.data,
            json=self.json,
            files=self.files,
        )
        prepare_request = request.prepare()

        # before final request, check
        # whether environment has proxies protocol or not
        # if yes, then merged it as one
        update_request = requests.Session().merge_environment_settings(
            url=self.url,
            proxies=self.proxies,
            stream=self.stream,
            verify=self.suppress_warning,
            cert=self.cert,
        )
        kwargs = {"allow_redirects": self.allow_redirects}
        kwargs.update(update_request)

        try:
            with requests.Session() as s:
                if retry:
                    self.retry = Retry(
                        total=3,
                        status_forcelist=[429, 500, 502, 503, 504],
                        method_whitelist=["GET", "POST"],
                        backoff_factor=0.3,
                    )
                    adapter = HTTPAdapter(max_retries=self.retry)
                    s.mount("https://", adapter)
                    s.mount("http://", adapter)
                else:
                    self.logger.info("[INFO] HTTP retry method might be turned it off")
                self.response = s.send(
                    request=prepare_request, timeout=self.timeout, **kwargs
                )
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

        self.logger.info(f"[INFO] HTTP Response {self.response.status_code}")
        self.logger.debug(f"[DEBUG] HTTP Response Header {self.response.headers}")
        # self.logger.debug(f"[DEBUG] HTTP Response Content {self.response.content}")

        if event_hooks:
            # if event hooks was set to True
            # call the valid response name instead
            # only call the message from related assertion
            self.response.raise_for_status()
            s.hooks["response"] = [response_hook]

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

    def __enter__(self):
        return self

    def __exit__(self):
        # exit the connection pooling
        # after send the final request
        self.response.close()

    # add setter-getter only for
    # base_url or HTTP method
    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> str:
        self._url = value

    @url.deleter
    def url(self) -> None:
        del self._url

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value: str) -> str:
        self._method = value

    @method.deleter
    def method(self) -> None:
        del self._method

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
