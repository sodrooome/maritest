from abc import ABC
from json.decoder import JSONDecodeError
import textwrap

from .client import Http


class Response(Http, ABC):
    """
    Formatted HTTP response and returned
    as either dict, text or binary
    """

    def retriever(self, format: str = "json"):
        """
        Collective method to retrieve HTTP response
        and returned as related argument ex: json,
        multipart and text

        :param format: Parameter for choose what kind
        of response that want to returned, by default
        set as JSON

        Returned formatted HTTP response
        """
        if not type(format):
            raise TypeError("Parameter format must be string object")

        if format.lower() not in ["multipart", "text", "json"]:
            raise NotImplementedError("There's no format that match with argument")

        try:
            if self.response.status_code == 200:
                if format.lower() == "json":
                    json_response = self.response.json()
                    response_body = {
                        "response_body": json_response,
                        "response_status_code": self.response.status_code,
                        "response_time": str(self.response.elapsed.total_seconds())
                        + " ms",
                        "response_headers": self.response.headers,
                        "is_json": True,
                    }
                elif format.lower() == "multipart":
                    part_response = self.response.content
                    response_body = part_response.decode()
                elif format.lower() == "text":
                    response_body = self.response.text, self.response.encoding
                else:
                    # need request body to debug when the
                    # error is occur during requested HTTP target
                    response_body = {
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
        except JSONDecodeError as e:
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
                response_body = "Either there's no URL redirect that can be counted or don't enable the parameter `allow_redirects` settings"
        except Exception as e:
            raise Exception(f"Another exception was occurs {e}")

        print(f"Count history : {response_count}", response_body)

    def http_response(self, *args, **kwargs):
        """
        Formatted HTTP response as raw format (text)
        """
        formatted_response = lambda x: "\n".join(
            f"{key} : {value}" for key, value in x.items()
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
                request_headers=formatted_response(self.response.request.headers),
                response_headers=formatted_response(self.response.headers),
            )
        )
