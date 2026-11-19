"""Bounded local HTTP demonstration. Production ingress/TLS are not implemented."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socket
import sqlite3
import threading
from .contracts import Denied, canonical, parse_json


class BoundedServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 16

    def __init__(self, address, handler):
        if address[0] != "127.0.0.1":
            raise ValueError("The reference server only binds loopback")
        self.slots = threading.BoundedSemaphore(16)
        super().__init__(address, handler)

    def get_request(self):
        conn, address = super().get_request()
        conn.settimeout(3)
        return conn, address

    def process_request(self, request, address):
        if not self.slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, address)
        except BaseException:
            self.slots.release()
            raise

    def process_request_thread(self, request, address):
        try:
            super().process_request_thread(request, address)
        finally:
            self.slots.release()


def gateway_handler(engine):
    class Handler(BaseHTTPRequestHandler):
        server_version = "EnterpriseAIGateway/0.1"
        sys_version = ""

        def log_message(self, *args):
            pass

        def reply(self, status, payload):
            raw = canonical(payload)
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Connection", "close")
            self.end_headers()
            self.close_connection = True
            try:
                self.wfile.write(raw)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def do_GET(self):
            if self.path == "/healthz":
                self.reply(200, {"status": "local_reference_alive"})
            else:
                self.reply(404, {"error": "unknown_endpoint"})

        def do_POST(self):
            try:
                if (self.headers.get_all("Transfer-Encoding")
                        or len(self.headers.get_all("Content-Length") or []) != 1):
                    raise Denied("invalid_framing", 400)
                length = self.headers.get("Content-Length", "")
                if not length.isdigit() or not 1 <= int(length) <= 32768:
                    raise Denied("invalid_body_size", 413)
                if (len(self.headers.get_all("Content-Type") or []) != 1
                        or self.headers.get("Content-Type") != "application/json"):
                    raise Denied("unsupported_media_type", 415)
                auths = self.headers.get_all("Authorization") or []
                if len(auths) != 1 or not auths[0].startswith("Bearer "):
                    raise Denied("invalid_credential", 401)
                # Authenticate before spending effort on the JSON body.
                engine.identity.resolve(auths[0][7:])
                keys = self.headers.get_all("Idempotency-Key") or []
                if len(keys) > 1:
                    raise Denied("invalid_idempotency_header", 400)
                raw = self.rfile.read(int(length))
                if len(raw) != int(length):
                    raise Denied("incomplete_body", 400)
                value = parse_json(raw)
                response = engine.dispatch(auths[0][7:], self.path, value, keys[0] if keys else None)
                self.reply(200, response)
            except Denied as error:
                self.reply(error.status, {"error": error.code})
            except (socket.timeout, TimeoutError):
                self.reply(408, {"error": "body_timeout"})
            except (sqlite3.Error, OSError):
                self.reply(503, {"error": "local_state_unavailable"})
            except Exception:
                self.reply(500, {"error": "internal_reference_error"})
    return Handler
