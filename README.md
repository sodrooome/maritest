## Maritest

[![Build](https://github.com/sodrooome/maritest/actions/workflows/test.yml/badge.svg)](https://github.com/sodrooome/maritest/actions/workflows/test.yml) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/maritest) ![PyPI - Status](https://img.shields.io/pypi/status/maritest) [![codecov](https://codecov.io/gh/sodrooome/maritest/branch/master/graph/badge.svg?token=H3K1JNZBW2)](https://codecov.io/gh/sodrooome/maritest)

**Maritest** is an API testing framework that the purpose solely of simplifying assertion when doing testing in the API layer, it's an easy and convenient way to go iterative testing while keeping up the fast-paced development and being able to maintain all testing modules/scenarios without breaking change

### Rationale

As the development process began to iterate quickly, QA teams need to step up again when writing automation tests, especially during assertions or schema validation while doing API testing

And thus it becomes problematic when many test scenarios need to be validated, especially from those scenarios that most likely will be written such as assertion for headers, response body, status code, or content-type. With Maritest, it will make it easier to write iterative assertions without the need for us to write again for the expectations and actual results from the API we tested and make it easier to maintainable API tests modules. From there, we can write it with much simpler automation API testing

### Limitation

The main concern is about since our assertion is only limited to the assertions that we have defined previously, it is very difficult to create and leverage other assertion scenarios that we wanted. Other than that, another problem is when you want to do custom validation in a complex response body or want to validate the data type of an object.

Another limitation is Maritest only supports 5 HTTP methods (`GET`, `POST`, `PATCH`, `DELETE`, `PUT`) other HTTP methods are not supported yet

### Installation

To install maritest just simply using :

`pip install maritest`

### Basic Usage

After you're done with installation, you can try to use this basic feature from **Maritest** for example

```python
from maritest.assertion import Assert

request = Assert(
    method="GET",                   # required, support 5 common HTTP method
    url="https://api.services.com", # required
    headers={},                     # required, set as empty dict if not needed
    proxy={"http": "api.services"}, # not required, default set to None
    timeout=60,                     # not required, default set to 120 seconds
)

# choose several method what kind of assertion that you wanted
# 1. Assert that request is success
# 2. Assert that request is failed
request.assert_is_ok(message="Should be success")
request.assert_is_failed(message="Should be failed")
```

If the assertion for that request is successful and according to what we expected, then it will return with a custom message that you already set before based on the message argument. If not successful, then it will raise an AssertionError with a formatted error message that is already available (without you needing to customize the error message again).

For now, Maritest already have prepared several kinds of assertions method which include a common assertion that is always used in testing for API scenario, those are :

```python
request = Assert("GET", "https://api.foo.bar", headers=...)

# assert if request was success
# and you can also write custom message if success
request.assert_is_ok(message="Response is OK")

# assert if request was failed
request.assert_is_failed(message="Response is FAILED")

# assert if response has headers
request.assert_is_headers(message="Response have headers")

# assert if content-type in headers is set
request.assert_is_content_type(message="Response have content-type")

# assert to identifying content-type value was equal to
request.assert_content_type_to_equal(value="application/json", message="Value of content-type is equal")

# assert if response status code IN range 2xx
request.assert_is_2xx_status(message="Response status in 2xx")

# assert if response status code in range 3xx
request.assert_is_3xx_status(message="Response status in 3xx")

# assert if response status code in range 4xx
request.assert_is_4xx_status(message="Response status in 4xx")

# assert if response status code in range 5xx
request.assert_is_5xx_status(message="Response status in 5xx")

# assert if response body has multipart files
request.assert_has_content(message="Response has content")

# assert if response body has json object
request.assert_has_json(message="Response has JSON")

# assert if response body has text attribute, binary
request.assert_has_text(message="Response has text")

# assert to identifying status code was in expected result
request.assert_status_code_in(status_code=[200, 201], message="Response status in 2xx")

# assert to identifying status code NOT in expected result
request.assert_status_code_not_in(status_code=[400, 404], message="Response status not in 4xx")

# assert if json response body equal to expected result
request.assert_json_to_equal(obj={"this one json object"}, message="Response is equal to JSON")

# assert if multipart response equal to expected result
request.assert_content_to_equal(obj={"multipart"}, message="Response is equal to multipart")

# assert if text response body equal to expected result
request.assert_text_to_equal(obj=b'this one is bytes object', message="Response is equal to byte")

# assert to identifying whether response time API calls in max duration
request.assert_response_time(duration=200, message="Response should not exceed the duration")

# assert to check if response time API calss NOT exceeds the max durationn
request.assert_response_time_less(message="Response should not exceed the limit")

# assert that request expected to be failed in 200 or 201 status code
request.assert_expected_to_fail(message="Response expected to be failed")

# assert if TLS is secure or not, message argument is optional
request.assert_tls_secure()

# assert if response contains content-length, message argument is optional
request.assert_content_length()
```

**Extra notes** : first parameter `message` is required to be fullfiled, if its not then only returned as `None` values

### Extending Usage

for extending usage of this framework itself, it's actually similar to the built-in APIs already in the requests package
(Maritest built on top of [that](https://docs.python-requests.org/en/latest/user/quickstart/)), so the behavior for
advanced use cases will depend on that. For example in **Maritest** you can use some additional arguments based on existing `kwargs`

- Leveraging request hooks

```python
from maritest.assertion import Assert

request = Assert(..., event_hooks=True)

# using normal assertion will return like this
>>> maritest.exceptions.Matcher:
>>>  Actual status code was   => 404
>>>  Expected status code was => 200, 201
>>>  And the message is       => Sukses

# with event_hooks set to True become like this
>>> requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://jsonplaceholder.typicode.com/postss
```

- Using retry instead timeout mechanism

```python
from maritest.assertion import Assert

request = Assert(..., retry=True)

# there's indicator that we're using retry on
# if we also set the logger parameter to True
>>> 19-12-2021 12:12:30 : Maritest Logger : __init__ : [INFO] HTTP retry method might be turned it off
```

- Enable logger stream handler. If `logger` argument is enabled, you will receive the output like this example but if you tend
to disabled the `logger` argument, you will get the log file instead in your local (the file named is "maritest.log")

```python
from maritest.assertion import Assert

request = Assert(..., logger=True)

# without logger
>>> The status code was : 200

# with logger enabled
>>> 19-12-2021 12:12:30 : Maritest Logger : __init__ : [INFO] HTTP Request GET | https://jsonplaceholder.typicode.com/posts
>>> 19-12-2021 12:12:30 : Maritest Logger : __init__ : [DEBUG] HTTP Request None, None
>>> 19-12-2021 12:12:31 : Maritest Logger : __init__ : [INFO] HTTP Response 200
```

- Suppressed warning message about SSL. Particulary, this one is not advise to do it, its strongly advise to add certification path

```python
from maritest.assertion import Assert

# if enable this, then warning message
# about unverified request will be hide
request = Assert(..., suppress_warning=True)
```

- Allow location redirection for HTTP target, supported for all HTTP methods. for example :

```python
from maritest.client import Http

# set to `True` for allow_redirection argument
request = Http(method="GET", url="http://github.com", allow_redirects=True)
```

**Extra notes** : You can actually see several times or history the URL that you input does redirection using the retriever method that has been provided with this framework. To do this you can perform with :

```python
# import Response module from maritest
from maritest.response import Response

request = Response(...)
request.history_response()

# the output will be like this
>>> URL redirects : http://github.com/
>>> Count history : 1 [None]
```

- Create customization assertion for your own. For this one, you can achieve it with inherited `Http` base class and afterwads. For example :

```python
from maritest.http import Http


class CustomAssertion(Http):
    def assert_tls_secure(self):
        if self.url.startswith("http://"):
            raise AssertionError("do your own message")
        elif self.url.startswith("https://"):
            return print("do it again")
        else:
            ...

# leverage your custom assertion
request = CustomAssertion("GET", "do something about it", {"headers":"headers_value"})
request.assert_tls_secure()
```

- Printed HTTP response with format that given : `json`, `multipart` and `text`

```python
from maritest.response import Response

resp = Response("https://github.com", None, False)

# printed HTTP response as JSON object
# with call this `retriever()` method and
# change the parameter format with `json`
resp.retriever(format="json")

# or, printed as multipart object
resp.retriever(format="multipart")

# or, printed as binary / text object
resp.retriever(format="text")
```

- Using extended custom authentication when requested API calls. For this one, Maritest already provided built-in APIs that can be use for HTTP authentication. The usage is straightforwad and simple like that `requests` package used for, such as :

```python
from maritest.assertion import Assert
from maritest.custom_auth import BasicAuth, DigestAuth, BearerAuth, BasicAuthToken

# calls the auth argument
# and pass the built-in APIs for
# HTTP authentication, eg:
# using `BasicAuth()`
resp = Assert(method=..., url=..., headers=..., auth=BasicAuth(username="some username", password="some password"))

# using `DigestAuth()`
resp = Assert(method=..., url=..., headers=..., auth=DigestAuth(username="some username", password="some password"))

# using `BearerAuthToken()`
resp = Assert(method="GET", url=..., headers=..., auth=BearerAuth(token="bearer token"))

# using `BasicAuthToken()`
resp =  Assert(method="GET", url=..., headers=..., auth=BasicAuthToken(token="basic token"))

# using `APIKeyAuth()`
# parameter `add_to` is required
# to fullfilled, the choice
# between `headers` or `query_params`
resp = Assert(method="GET", url=..., headers=..., auth=ApiKeyAuth(key="some key", value="some value", add_to="headers"))
```

### Features

- [x] Allow redirects, handling connection timeout and backoff mechanism
- [ ] Assertion for data type of object (could it be Array properties, dict, etc)
- [x] Several enhancements and improvements from missing property in HTTP client
- [x] Error message improvements in assertion test and parameter customization

### Acknowledgements

- [requests](https://docs.python-requests.org/en/latest/user/quickstart/), as base building to create and extending custom HTTP client.
- [Postman scripts](https://learning.postman.com/docs/writing-scripts/intro-to-scripts/), as idea to make assertion scenario
