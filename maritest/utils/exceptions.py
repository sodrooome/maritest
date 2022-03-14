from typing import Any


class Matcher(Exception):
    """
    Custom exception class that will be
    raise if there's error based on
    status code
    """

    def __init__(self, actual_code: int, expected_code: str, message: str):
        self.actual = actual_code
        self.expected = expected_code
        self.message = message

    def __repr__(self):
        return repr(self.message)

    def __str__(self) -> str:
        if self.actual and self.expected is not None:
            # note: this trailing whitespace was
            # intended on the first place
            return (
                f"\n Actual status code was   => {self.actual} \n Expected status code was => {self.expected} \n "
                f"And the message is       => {self.message} "
            )

    def __eq__(self, other):
        return (
            self.actual == other.actual
            and self.expected == other.expected
            and self.message == other.message
        )


class MatcherResponse(Exception):
    """
    Custom exception class that will be
    raise if there's error related to
    response body (headers, content, etc)
    """

    def __init__(
        self, actual_response: Any, message: str, expected_response: Any = None
    ):
        self.actual = actual_response
        self.expected = expected_response
        self.message = message

    def __repr__(self) -> str:
        return repr(self.message)

    def __str__(self) -> str:
        if self.expected is not None:
            return (
                f"\n Actual response from body was   => {self.actual}, \n Expected response was => "
                f"{self.expected}, \n And the message is       => {self.message} "
            )
        else:
            return f"\n Actual response from body was   => {self.actual}, \n And the message is       => {self.message}"
