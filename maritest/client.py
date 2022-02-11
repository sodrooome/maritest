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
try:
    import requests
except ImportError as e:
    raise Exception(f"Unable to importerd `requests` package {e}")

import logging
import warnings
import urllib3
import json
import urllib.parse
from .version import __version__
from abc import abstractmethod
from requests.sessions import CaseInsensitiveDict
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


# TODO: also split this function callable
def default_headers():
    return CaseInsensitiveDict(
        {
            "User-Agent": f"maritest, {__version__}",
            "Accept": "*/*",
            "Connection": "keep-alive",
        }
    )


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
        supress_warning: bool = None,
        proxy: dict = None,
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
        set False, will suppressed warning message
        :param proxy: HTTP proxies configuration, by default
        always set to None, and must be configured in HTTPS
        :param kwargs: given by keyword argument
        :param auth: Authentication configuration for using
        HTTP client, by default set to None

        Returned as HTTP response
        """
        # missing attributes :
        # session, certs, file, json, data
        self.method = method
        self.url = url
        self.headers = headers

        assert isinstance(method, str), "method must be string object"
        assert isinstance(url, str), "url schema must be string object"
        assert isinstance(headers, dict), "headers must be dict object"

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
        self.proxy = proxy
        self.allow_redirects = allow_redirects
        self.stream = False
        self.cert = None
        self.suppress_warning = (
            supress_warning  # by default set to True due staging environment
        )
        self.verify = None
        self.session = None
        self.auth = None

        if logger:
            # why the heck am i validate
            # the logger twice ??
            self.logger.info(f"[INFO] HTTP Request {self.method} => {self.url}")
            self.logger.debug(f"[DEBUG] HTTP Request {self.headers} => {self.url}")

        if headers is None:
            # enforcing headers alwasy
            # wrap themselves with dict type
            # merge with pre-defined headers
            self.headers = default_headers()

        if self.timeout is None:
            self.timeout = 120

        if method is not None:
            self.method = method.upper()

        if self.method not in iter(ALLOWED_METHODS):
            raise NotImplementedError(f"Currently {self.method} method not supported")

        if self.response is None:
            self.response = requests.Response

        if self.data is None:
            self.data = {}

        if self.params is None:
            self.params = {}

        if self.files is None:
            self.files = {}

        if self.json is None:
            self.json = {}
        else:
            # printed JSON response with formatted output
            self.json = json.dumps(self.json, indent=2, sort_keys=False)

        # new attribute to call the request session instance
        if self.session is None:
            self.session = requests.Session()

        # by default, using proxies only
        # for HTTPS over HTTP connection
        if proxy is not None:
            if "https" not in [key for key in self.proxy.keys()]:
                raise ConnectionError(
                    "Proxy connection must be configured HTTPS over HTTP"
                )
            else:
                # elsewhere, update the new conf
                # for proxy before merge into request
                # TODO: differentiate the sessions attribute itself
                self.proxy = self.session.proxies.update(proxy)

        if supress_warning is not None:
            if supress_warning:
                warnings.warn(
                    "parameter `suppressed_warning` will be deprecated and no longer use in the next release "
                    "consider to add certification path instead or always enable the SSL verification issue "
                )
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
            auth=self.auth,
        )
        prepare_request = request.prepare()

        # before final request, check
        # whether environment has proxies protocol or not
        # if yes, then merged it as one
        update_request = self.session.merge_environment_settings(
            url=self.url,
            proxies=self.proxy,
            stream=self.stream,
            verify=self.suppress_warning,
            cert=self.cert,
        )
        kwargs = {"allow_redirects": self.allow_redirects, "timeout": self.timeout}
        kwargs.update(update_request)

        try:
            with self.session as s:
                if retry:
                    self.retry = Retry(
                        total=3,
                        status_forcelist=[429, 500, 502, 503, 504],
                        method_whitelist=["GET", "POST"],
                        backoff_factor=0.3,
                    )
                    adapter = HTTPAdapter(max_retries=self.retry)
                    if urllib.parse.urlparse(self.url).scheme == "http":
                        s.mount("https://", adapter)
                    else:
                        # only given a log warning for user
                        s.mount("http://", adapter)
                        self.logger.warning(
                            f"[WARNING] you're going to mounted unverified (HTTP) protocol"
                        )
                else:
                    self.logger.info("[INFO] HTTP retry method might be turned it off")
                self.response = s.send(request=prepare_request, **kwargs)
                self.response.encoding = "utf-8"
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
        return f"<Http:{self.method}=>{self.url}>"

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
    @abstractmethod
    def assert_is_ok(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_is_failed(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_is_headers(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_is_content_type(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_content_type_to_equal(self, value: str, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_is_2xx_status(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_is_3xx_status(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_is_4xx_status(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_is_5xx_status(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_has_content(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_has_json(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_has_text(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_status_code_in(self, status_code: str, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_status_code_not_in(self, status_code: str, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_json_to_equal(self, obj, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_text_to_equal(self, obj, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_content_to_equal(self, obj, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_response_time(self, duration: int, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_dict_to_equal(self, obj: dict, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_response_time_less(self, message: str):
        raise NotImplementedError

    @abstractmethod
    def assert_expected_to_fail(self, message: str):
        raise NotImplementedError
