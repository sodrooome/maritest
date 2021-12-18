## Maritest

Maritest is an API testing framework that is used internally in the MauKerja tester team which aims to make it easier for QA to make assertions when doing the API testing layer. The writing design for test script itself is highly influence by Postman test script scenario (you can refer to this [one](https://learning.postman.com/docs/writing-scripts/script-references/test-examples/#testing-response-body))

### Rationale

As the development process began to iterate quickly, our QA teams needs to step up again when writing automation tests especially during assertions or API validation while in integration testing. Think of it, before using this framework, usually (and most of it) for writing own API testing will be like this :

```python
class TestApiB(unittest.TestCase):
    def setUp(self):
        # some code goes here

    def test_services_a(self):
        request = requests.get("foobar")
        response = request.json()

        # write all of assertion that we need
        # with custom message for indicates that
        # testing is pass or not
        self.assertEqual(response, expected_result), "this one is in the bag!"
        self.assertIn(request.status_code, [201, 204, 203]), "its success bro"
        self.assertAlmostEquals(response["data"], [index for index in response]), "success bro"
        self.assertIn(request.headers["content-type"], "WAHOO"), "sukses!"
        ...
```

And thus it becomes problematic when there are many test scenarios that need to be validated, especially from those scenarios what will definitely be written is to asserting headers, response body, status code or content-type. With **Maritest**, it will make it easier to write iterative assertions and make it easier to maintainable API tests module. From there, we can actually write it with much simpler function (or just plain variables) :

```python
class TestApiB:
    def test_services_a(self):
        request = Http("GET", "base_url", headers)

        # directly instantiate the assertion
        # with existing error message or custom message
        request.assert_is_failed
        request.assert_is_ok("sukses!")
        request.assert_is_2xx_status
        request.assert_status_code_in([200,201,204])
        request.assert_is_has_json
```

### Limitation

The main concern is about since our assertion is only limited to the assertions that we have defined previously, so it is very difficult to create and leveraging other custom validations such as parameterization, mocking, stubbing or so on. Other than that, another problem is when you want to do custom validation in a complex response body or want to validate the data type of an object

### Basic Usage

Basic usage for using **Maritest** its just declare like using normal variable without create new class for that 

```python
from client import Http

request = Http("GET", "http://localhost", {"key":"value"})
request.assert_is_2xx_status(message="sukses")
request.assert_is_dict(message="sukses")
```

If assertion for that request is success and according to what we expected, then it will returned with custom message
that we've already set before. If not success, then t will print a formatted error message that is already available 
(without you needing to customize it again).

For now, Maritest already have prepared several kinds of assertions which include a common assertion that is always used
in testing scenario

### Extending Usage

for extending usage of this framework itself, it's actually similar to the built-in APIs already in the requests package 
(Maritest built on top of [that](https://docs.python-requests.org/en/latest/user/quickstart/)), so the behavior for 
advanced use cases will depend on that. For example

- Leveraging request hooks

```python
from client import Http

request = Http(..., event_hooks=True) # enable event hooks

# using normal assertion will return like this
> AssertionError: The status got 4xx

# with event_hooks set to True become like this
> requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://jsonplaceholder.typicode.com/postss
```

- Using retry instead timeout mechanism

```python
from client import Http

request = Http(..., retry=True) # enable this retry

# there's indicator that we're using retry
# if we also set the logger parameter to True
> 19-12-2021 12:12:30 : Maritest Logger : __init__ : [INFO] HTTP retry method might be turned it off
```

- Enable logger stream handler

```python
from client import Http

request = Http(..., logger=True) # enable this logger

# without logger
> The status code was : 200

# with logger enabled
> 19-12-2021 12:12:30 : Maritest Logger : __init__ : [INFO] HTTP Request GET | https://jsonplaceholder.typicode.com/posts
> 19-12-2021 12:12:30 : Maritest Logger : __init__ : [DEBUG] HTTP Request None, None
> 19-12-2021 12:12:31 : Maritest Logger : __init__ : [INFO] HTTP Response 200
```

### Upcoming Features

- [x] Allow redirects and checking up for certs
- [x] Handling connection timeout
- [ ] Assertion for data type of object (could it be Array properties, dict, etc)
- [ ] Decorators for storing testing events (from start - finish)
- [ ] Several enhancements and improvements from missing property in HTTP client