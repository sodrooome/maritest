import unittest
import requests
import requests_mock  # type: ignore
from maritest.custom_auth import (
    ApiKeyAuth,
    BasicAuth,
    BearerAuth,
    BasicAuthToken,
    DigestAuth,
)


class TestCustomAuth(unittest.TestCase):
    def test_bearer_auth(self):
        with requests_mock.mock() as m:
            m.get(
                "https://github.com",
                request_headers={"Authorization": "Bearer testtest"},
            )

        bearer_auth = BearerAuth("testtest")
        response = requests.get("https://httpbin.org/bearer", auth=bearer_auth)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.json(), "{'authenticated': true, 'token': 'testtest'}")

    def test_basic_auth_token(self):
        with requests_mock.mock() as m:
            m.get(
                "https://github.com",
                request_headers={"Authorization": "Basic password token"},
            )

        basic_auth = BasicAuthToken(token="password token")
        response = requests.get("https://github.com", auth=basic_auth)

        self.assertTrue(response.status_code, 200)

    def test_api_key_auth(self):
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, text="Success Mock API Key Auth")

        api_key_auth = ApiKeyAuth(
            add_to="headers", key="key-1", value="value-1", header_name="Authorization"
        )
        response = requests.get("https://github.com", auth=api_key_auth)

        self.assertTrue(response.status_code, 200)

    def test_query_api_auth(self):
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, text="Success Mock API with Query Params")

        query_api_auth = ApiKeyAuth(add_to="query_params", key="key1", value="value2")
        response = requests.get("https://github.com", auth=query_api_auth)

        self.assertTrue(response.status_code, 200)
        self.assertEqual(
            response.url, "https://github.com/?key1=value2", "Full-path url is equal"
        )

    def test_basic_auth(self):
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, text="Success Mock HTTP")

        basic_auth = BasicAuth(username="ryan", password="1234")
        response = requests.get(
            "https://httpbin.org/basic-auth/ryan/1234", auth=basic_auth
        )

        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.json(), "{'authenticated': True, 'user': 'ryan'}")

    def test_digest_auth(self):
        with requests_mock.mock() as m:
            m.get("https://httpbin.org/digest-auth/auth/user/pass")

        digest_auth = DigestAuth(username="user", password="pass")
        response = requests.get(
            "https://httpbin.org/digest-auth/auth/user/pass", auth=digest_auth
        )

        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.json(), "'authenticated': True, 'user': 'user'")

    @unittest.expectedFailure
    def test_invalid_bearer_token(self):
        with requests_mock.mock() as m:
            m.get(
                "https://httpbin.org/bearer",
                request_headers={"Authorization": "Bearer 1234"},
            )

        BearerAuth(1234)  # invalid token

    @unittest.expectedFailure
    def test_invalid_basic_token(self):
        with requests_mock.mock() as m:
            m.get(
                "https://github.com",
                request_headers={"Authorization": "Basic password token"},
            )

        BasicAuthToken(token=12345678)  # invalid token

    @unittest.expectedFailure
    def test_invalid_add_to_headers(self):
        with requests_mock.mock() as m:
            m.get(
                requests_mock.ANY, text="Invalid mock API Key Auth due invalid add to"
            )

        ApiKeyAuth(add_to=1234, key="key1", value="value2")

    @unittest.expectedFailure
    def test_invalid_add_type_headers(self):
        with requests_mock.mock() as m:
            m.get(
                requests_mock.ANY, text="Invalid mock API Key Auth due invalid add to"
            )

        ApiKeyAuth(add_to="query-params", key="key1", value="value2")


if __name__ == "__main__":
    unittest.main()
