import unittest
import requests
import requests_mock  # type: ignore
from maritest.custom_auth import ApiKeyAuth, BasicAuth, BearerAuth, BasicAuthToken


class TestCustomAuth(unittest.TestCase):
    def test_bearer_auth(self):
        with requests_mock.mock() as m:
            m.get(
                "https://github.com",
                request_headers={"Authorization": "Bearer testtest"},
            )

        bearer_auth = BearerAuth("testtest")
        response = requests.get("https://github.com", auth=bearer_auth)

        self.assertTrue(response.status_code, 200)

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

        basic_auth = BasicAuth(username="fake username", password="fake password")
        response = requests.get("https://github.com", auth=basic_auth)

        self.assertTrue(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
