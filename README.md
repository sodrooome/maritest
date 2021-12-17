## Maritest

Maritest is an API testing framework that is used internally in the MauKerja tester team which aims to make it easier for QA to make assertions when doing the API testing layer. The writing for test script design itself highly influence by Postman test script scenario (you can refer to this [one](https://learning.postman.com/docs/writing-scripts/script-references/test-examples/#testing-response-body))

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

### Upcoming Features

- [ ] Allow redirects and checking up for certs
- [ ] Handling connection timeout
- [ ] Assertion for data type of object (could it be Array properties, dict, etc)
- [ ] Decorators for storing testing events (from start - finish)
- [ ] Several enhancements and improvements from missing property in HTTP client