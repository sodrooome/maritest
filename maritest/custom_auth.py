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
    by Postman authorization
    """

    def __init__(
        self, key: Optional[str], value: Optional[str], add_to: str = "headers"
    ) -> None:
        self.key = key
        self.value = value
        self.add_to = add_to

        if not isinstance(add_to, str):
            raise TypeError("`add_to` parameter must be string object")

    def __eq__(self, other) -> bool:
        return all([
            self.key == getattr(other, "key"),
            self.value == getattr(other, "value")
        ])

    def __call__(self, r: models.Request) -> models.Request:
        if self.key and self.value is not None:
            if self.add_to == "headers":
                r.headers["Authorization"] = self.key, self.value
            elif self.add_to == "query_params":
                r.params = {f"{self.key} : {self.value}"}
            else:
                raise ValueError("There is no option to add API key")
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
