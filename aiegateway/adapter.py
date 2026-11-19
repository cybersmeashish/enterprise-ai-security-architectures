"""A loopback-only HTTP adapter for deterministic provider fixtures."""
import http.client
import socket
from urllib.parse import urlsplit
from .contracts import Denied, canonical, fields, parse_json


class LoopbackAdapter:
    def __init__(self, url, upstream_token, timeout=0.5):
        parsed = urlsplit(url)
        try:
            port = parsed.port
        except ValueError:
            raise Denied("invalid_provider_endpoint") from None
        if (parsed.scheme != "http" or parsed.hostname != "127.0.0.1"
                or not port or parsed.username or parsed.password or parsed.path != "/infer"
                or parsed.query or parsed.fragment or not 0.01 <= timeout <= 2):
            raise Denied("invalid_provider_endpoint")
        self.port, self.upstream_token, self.timeout = port, upstream_token, timeout

    def generate(self, prompt, max_output_bytes, model):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=self.timeout)
        try:
            connection.request("POST", "/infer",
                               canonical({"prompt": prompt, "max_output_bytes": max_output_bytes,
                                          "model": model}),
                               {"Content-Type": "application/json",
                                "Authorization": "Bearer " + self.upstream_token})
            response = connection.getresponse()
            if response.status != 200:
                raise Denied("provider_unavailable", 503)
            if response.getheader("Content-Type", "").split(";")[0] != "application/json":
                raise Denied("provider_invalid_response", 502)
            raw = response.read(16385)
            if len(raw) > 16384:
                raise Denied("provider_response_too_large", 502)
            value = parse_json(raw)
            fields(value, ("text",))
            if (not isinstance(value["text"], str)
                    or len(value["text"].encode()) > max_output_bytes):
                raise Denied("provider_invalid_response", 502)
            return value["text"]
        except Denied as error:
            if error.status == 400:
                raise Denied("provider_invalid_response", 502) from None
            raise
        except (OSError, socket.timeout, http.client.HTTPException, UnicodeError):
            raise Denied("provider_unavailable", 503) from None
        finally:
            connection.close()
