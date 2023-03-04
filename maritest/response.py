import textwrap
import requests

from abc import ABC

from .client import Http


class Response(Http, ABC):
    """
    Formatted HTTP response and returned
    as either dict, text or binary response.
    An inheritance class that sub-classing from
    Http Client in maritest.client module
    """

    def retriever(self, fmt: str = "json"):
        """
        Collective method to retrieve HTTP response
        and returned as related argument ex: json,
        content and text

        :param fmt: Parameter for choose what kind
            of response that want to returned, by default
            set as JSON

        Returned formatted HTTP response
        """
        if not type(fmt):
            raise TypeError(
                "Parameter format must be string object"
            )  # pragma: no cover

        if fmt.lower() not in ["content", "text", "json"]:
            raise NotImplementedError("There's no format that match with argument")

        try:
            if self.response.status_code == 200:
                if fmt.lower() == "json":
                    json_response = self.response.json()
                    response_body = {
                        "response_body": json_response,
                        "response_status_code": self.response.status_code,
                        "response_time": str(self.response.elapsed.total_seconds())
                        + " ms",
                        "response_headers": self.response.headers,
                        "is_json": True,
                    }
                elif fmt.lower() == "content":
                    part_response = self.response.content
                    response_body = part_response.decode()
                elif fmt.lower() == "text":
                    response_body = self.response.text, self.response.encoding
                else:
                    # need request body to debug when the
                    # error is occur during requested HTTP target
                    response_body = {  # pragma: no cover
                        "request": {
                            "request_url": self.url,
                            "request_method": self.method,
                            "request_headers": self.headers,
                        },
                        "response": {
                            "response_body": None,
                            "response_status_code": self.response.status_code,
                            "response_time": str(self.response.elapsed.total_seconds())
                            + " ms",
                            "response_headers": self.response.headers,
                            "is_json": (False, type(self.response)),
                        },
                    }
                print(response_body)
            else:
                print((None, self.response.status_code))
        except requests.exceptions.JSONDecodeError as e:
            raise Exception(f"Unable to decode the HTTP response {e}")
        except Exception as e:
            raise Exception(f"Another exception was occurs {e}")

    def history_response(self):
        """
        Formatted string output for url redirection history
        """
        count = len(self.response.history)
        try:
            if count > 0:
                response_count = count
                response_body = [
                    print(f"URL redirects : {response.url}")
                    for response in self.response.history
                ]
            else:
                response_count = 0
                response_body = (
                    "Either there's no URL redirect that can be counted or don't enable the parameter "
                    "`allow_redirects` settings "
                )
        except Exception as e:
            raise Exception(f"Another exception was occurs {e}")  # pragma: no cover

        print(f"Count history : {response_count}", response_body)

    def http_response(self):
        """
        Formatted HTTP response as raw format (text)
        """
        format_request = "\n".join(
            f"{key} : {value}" for key, value in self.response.request.headers.items()
        )
        format_headers = "\n".join(
            f"{key} : {value}" for key, value in self.response.headers.items()
        )
        print(
            textwrap.dedent(
                """
            ------------------Maritest Request------------------
            {req.method} {req.url}
            {request_headers}

            {req.body}
            ------------------Maritest Response-----------------
            {resp.status_code} {resp.url}
            {response_headers}

            {resp.text}
            """
            ).format(
                req=self.response.request,
                resp=self.response,
                request_headers=format_request,
                response_headers=format_headers,
            )
        )
