try:
    import requests
except ImportError as e:
    raise Exception(f"Unable to imported `requests` package {e}")

import urllib.parse
import warnings
import random
from abc import abstractmethod
from contextlib import contextmanager
from typing import Tuple, Optional, Any

import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # type: ignore
from requests.sessions import CaseInsensitiveDict, RequestsCookieJar

from .utils.factory import Logger
from .version import __version__

# For our purposes,
# its only supported 5 HTTP method
ALLOWED_METHODS = ["GET", "PUT", "POST", "DELETE", "PATCH"]


# TODO: separate this function calls
@contextmanager
def disable_warnings():
    # thanks stack overflow see at: https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning
    # -unverified-https-request-is-being-made-in-pytho
    with warnings.catch_warnings():
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # type: ignore
        yield None


class Http:
    """
    This is a base class for HTTP client.
    Constructor for request HTTP target, with
    several parameter to construct it :

    :param method: HTTP method verb, string type. such as:
        "GET", "POST", and other supported HTTP method
    :param url: base url for HTTP target, string type
    :param headers: HTTP content headers, by default always set to dict object
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
    :param kwargs: given by keyword argument for allow_redirects
        or timeout
    :param auth: Authentication configuration for using
        HTTP client, by default set to None
    :param data: Append file like object in the request body,
        set to None or optional.
    :param files: Append file like object with defining
        content-type of that file. set to None or optional
    :param params: Append query string when request in url,
        set to None or optional.
    :param auth: arguments for doing authentication request
        to the HTTP target. Support common HTTP auth, and by
        default set to None.
    :param json: argument for sending a request in HTTP body
        with JSON-format. By default set to None or optional
    :param timeout: parameter to setup timeout argument whenever
        request is failed, the initial duration of timeout
        is random values, by default set to None or optional

    Returned as HTTP response object
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
        data: dict = None,
        params: dict = None,
        files: dict = None,
        auth: Tuple = None,
        json: dict = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> None:
        # missing attributes :
        # session, certs, file, json, data
        self.method = method
        self.url = url
        self.headers = headers

        assert isinstance(method, str), "method must be string object"
        assert isinstance(url, str), "url schema must be string object"
        assert isinstance(headers, dict), "headers must be dict object"

        # for right now, always set log_level into INFO
        # to avoid getting error due partial conditional
        # if-else statement in Logger factory class
        if logger:
            self.logger = Logger.get_logger(
                url=self.url, method=self.method, log_level="INFO", silent=False
            )
        else:
            self.logger = Logger.get_logger(
                url=self.url, method=self.method, log_level="INFO", silent=True
            )

        self.timeout = None
        self.response = None
        self.json = json
        self.data = data
        self.params = params
        self.files = files
        self.proxy = proxy
        self.allow_redirects = allow_redirects
        self.stream = False
        self.cert = None
        self.suppress_warning = (
            supress_warning  # by default set to True due staging environment
        )
        self.verify = None
        self.session = None
        self.auth = auth
        self.created_session = False  # flagging to close request session
        self.timeout = timeout

        if timeout is None:
            self.timeout = self.random_timeout()

        if method is not None:
            self.method = method.upper()

        if self.method not in iter(ALLOWED_METHODS):
            raise NotImplementedError(f"Currently {self.method} method not supported")

        if data is None:
            self.data = {}

        if params is None:
            self.params = {}

        if files is None:
            self.files = {}

        if json is None:
            self.json = {}

        # new attribute to call the request session instance
        # if session is emitted to None object, then should
        # be called the create_session method to handling the request
        if self.session is None:
            self.session = self.create_session(**kwargs)

        if self.response is None:
            self.response = self.make_response()
            self.created_session = True

        if headers is None:
            # enforcing headers always
            # wrap themselves with dict type
            # merge with pre-defined headers
            self.headers = self.default_headers()  # pragma: no cover

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

        # https://docs.python-requests.org/en/master/user/advanced/#session-objects
        prepare_request = self.session.prepare_request(request)

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

                self.http_log_request()

                if retry:
                    self.retry = Retry(
                        total=3,
                        status_forcelist=[429, 500, 502, 503, 504],
                        method_whitelist=frozenset(
                            {"DELETE", "GET", "HEAD", "OPTIONS", "PUT"}
                        ),
                        backoff_factor=0.3,
                    )
                    adapter = HTTPAdapter(max_retries=self.retry)
                    if urllib.parse.urlparse(self.url).scheme == "http":
                        # only given a log warning for user
                        s.mount("https://", adapter)
                        self.logger.warning(
                            f"[WARNING] you're going to mounted unverified (HTTP) protocol"
                        )
                    else:
                        s.mount("http://", adapter)
                else:
                    self.logger.info("[INFO] HTTP retry method might be turned it off")
                self.response = s.send(request=prepare_request, **kwargs)
                self.response.encoding = "utf-8"
        except requests.exceptions.Timeout as e:
            # temporary using requests exception
            # TODO: make base class for custom exceptio
            raise Exception(f"HTTP Request was timeout {e}")
        except (
            requests.exceptions.SSLError,
            requests.exceptions.MissingSchema,
        ) as e:
            raise Exception(f"HTTP Request was invalid {e}")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP Request was error {e}")
        except KeyError as e:
            raise Exception(f"There's no any key to that HTTP response => {e}")
        except requests.exceptions.JSONDecodeError as e:
            raise Exception(f"Exception occur when try to unpack the JSON => {e}")
        except Exception as e:
            raise Exception(f"Other exception was occur {e}")
        finally:
            pass

        self.http_log_response()

        if event_hooks:
            # if event hooks was set to True
            # call the valid response name instead
            # only call the message from related assertion
            self.response.raise_for_status()

    def __str__(self) -> str:
        if self.method and self.url is not None:
            return f"You're using Maritest with HTTP Request {self.url} | {self.method}"
        else:
            return f"You're using Maritest without setup URL or HTTP verbs method"  # pragma: no cover

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

    def __exit__(self, exception_type, exception_value, traceback):
        # exit the connection pooling
        # after send the final request so
        # all HTTP response can't be
        # accessible again, so for example:
        # if you tend to get the HTTP headers
        # outside Http() class scope, you
        # wont get any response for that
        self.response.close()

    def __del__(self):
        # delete all adapters based on
        # the request.session(),
        # marked by flag instance of
        # self.created_session attribute
        if self.created_session:
            self.session.close()
            self.created_session = False

    def http_log_request(self):
        """Log HTTP information when send request"""
        self.logger.info("-- Maritest Logger --")
        self.logger.info(f"[INFO] HTTP Request Information {self.method} => {self.url}")
        self.logger.info(f"[INFO] HTTP Request Header => {self.headers}, {self.params}")

    def http_log_response(self):
        """Log HTTP response information after send request"""
        self.logger.info(
            f"[INFO] HTTP Response Status Code => {self.response.status_code}"
        )
        self.logger.info(f"[INFO] HTTP Response Header => {self.response.headers}")

        # if response got other than 200, then also raise with the reason
        if self.response.status_code != 200:
            self.logger.info(f"[INFO] HTTP Response Reason => {self.response.reason}")

    @staticmethod
    def random_timeout() -> float:
        """Internal method to generate random timeout in 1-4 seconds
        of interval and returned as floating number
        """
        return float(random.uniform(1, 4))

    @property
    def get_json(self) -> Any:
        """Property method to return response in JSON format"""
        return self.response.json()

    @property
    def get_status_code(self) -> int:
        """Property method to return response in integer of status code"""
        return self.response.status_code

    @property
    def get_url(self) -> str:
        """Property method to return full-path of URL"""
        return self.response.url

    @property
    def get_headers(self) -> CaseInsensitiveDict:
        """Property method to return response headers in dict format"""
        return self.response.headers

    @property
    def get_history(self) -> list:
        """Property method to return HTTP redirection history"""
        return self.response.history

    @property
    def get_cookies(self) -> RequestsCookieJar:
        """Property method to return cookies jar response"""
        return self.response.cookies

    @property
    def get_content(self) -> bytes:
        """Property method to return content response from server"""
        return self.response.content

    @property
    def get_text(self) -> str:
        """Property method to return content response in unicode"""
        return self.response.text

    @property
    def get_duration(self) -> float:
        """Property method to return total of duration after send request in seconds"""
        return self.response.elapsed.total_seconds()

    @staticmethod
    def create_session(**kwargs):
        """Handling the session requests"""
        session = requests.Session()
        for key in kwargs:
            setattr(session, key, kwargs[key])
        return session

    @staticmethod
    def default_headers():
        """
        Given default HTTP headers for maritest
        if headers argument wasn't set at the first time
        """
        return CaseInsensitiveDict(  # pragma: no cover
            {
                "User-Agent": f"maritest, {__version__}",
                "Accept": "*/*",
                "Connection": "keep-alive",
            }
        )

    @staticmethod
    def make_response():
        """Handling the HTTP response object"""
        return requests.Response()

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

    @abstractmethod
    def assert_content_length(self, message: str = None):
        raise NotImplementedError

    @abstractmethod
    def assert_tls_secure(self, message: str = None):
        raise NotImplementedError
