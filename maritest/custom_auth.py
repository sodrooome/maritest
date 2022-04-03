from base64 import b64encode
from typing import Optional
from requests.auth import AuthBase, HTTPDigestAuth, HTTPBasicAuth
from requests import models


class BearerAuth(AuthBase):
    """
    Custom bearer authentication
    that sub-classes from requests module
    """

    def __init__(self, token: str) -> None:
        self.token = token

        if not isinstance(token, str):
            raise TypeError("Bearer token must be string of object")

    def __call__(self, r: models.PreparedRequest) -> models.PreparedRequest:
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


class BasicAuthToken(AuthBase):
    """
    Custom basic auth with token,
    its differ with requests BasicAuth
    """

    def __init__(self, token: str) -> None:
        self.token = token

        if not isinstance(token, str):
            raise TypeError("Basic auth token must be string of object")

    def __call__(self, r: models.PreparedRequest) -> models.PreparedRequest:
        encode = b64encode(f"token: {self.token}".encode("utf-8")).decode("utf-8")
        r.headers["Authorization"] = f"Basic {encode}"
        return r


class ApiKeyAuth(AuthBase):
    """
    Custom API key auth that will append
    into headers, this one is influenced
    by Postman QueryApiKey authorization
    :param key: set API key if present, string type
    :param value: set API value for related key
    if present, string type
    :param add_to: mandatory argument to describes
    what kind of method that wants to be add. Support
    add to HTTP headers and add url with given by
    query params.
    :param header_name: give valid HTTP header name
    to related field, If its not set the header name, then
    by default will be directed into X-API-KEY field
    """

    def __init__(
        self,
        key: Optional[str],
        value: Optional[str],
        add_to: str = "headers",
        header_name: str = None,
    ) -> None:
        self.key = key
        self.value = value
        self.add_to = add_to
        self.header_name = header_name

        if not isinstance(add_to, str):
            raise TypeError("`add_to` parameter must be string object")

        if self.add_to not in ["headers", "query_params"]:
            raise ValueError("There's no option to add into API Key Auth")

    def __eq__(self, other) -> bool:
        return all(
            [self.key == getattr(other, "key"), self.value == getattr(other, "value")]
        )

    def __call__(self, r: models.PreparedRequest) -> models.PreparedRequest:
        if self.key and self.value is not None:
            if self.add_to == "headers" and self.header_name is not None:
                r.headers[self.header_name] = f"{self.key} : {self.value}"
            else:
                # by default set to X-API-KEY
                # if heades name wasnt set at all
                r.headers["X-API-KEY"] = f"{self.key} : {self.value}"

            if self.add_to == "query_params":
                params_payload = {f"{self.key}": f"{self.value}"}
                r.prepare_url(url=r.url, params=params_payload)
        return r


class BasicAuth(HTTPBasicAuth):
    """
    this only inherit from requests module,
    and wrapped it into new method.
    """

    pass


class DigestAuth(HTTPDigestAuth):
    """
    this only inherit from requests module,
    and wrapped it into new method
    """

    pass
