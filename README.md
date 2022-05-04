## Maritest

[![Build](https://github.com/sodrooome/maritest/actions/workflows/test.yml/badge.svg)](https://github.com/sodrooome/maritest/actions/workflows/test.yml) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/maritest) ![PyPI - Status](https://img.shields.io/pypi/status/maritest) [![codecov](https://codecov.io/gh/sodrooome/maritest/branch/master/graph/badge.svg?token=H3K1JNZBW2)](https://codecov.io/gh/sodrooome/maritest)

**Maritest** is an API testing framework that the purpose solely of simplifying assertion when doing testing in the API layer, it's an easy and convenient way to go iterative testing while keeping up the fast-paced development and being able to maintain all testing modules/scenarios without breaking change

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

For now, Maritest already have prepared several kinds of assertions method which include a common assertion that is always used in testing for API scenario. For further detail, please read the [documentation](https://maritest.readthedocs.io/en/latest/)
