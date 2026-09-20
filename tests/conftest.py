import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest


class DemoApiHandler(BaseHTTPRequestHandler):
    def _write_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self._write_json(200, {"status": "ok"})
            return
        if self.path == "/users":
            self._write_json(200, [{"id": 1, "name": "Sentinel Demo"}])
            return
        if self.path == "/server-error":
            self._write_json(500, {"error": "demo failure"})
            return
        self._write_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/login":
            self._write_json(404, {"error": "not found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(content_length) or b"{}")

        if payload == {"username": "demo", "password": "sentinel"}:
            self._write_json(200, {"token": "demo-token"})
            return

        self._write_json(401, {"error": "invalid credentials"})

    def log_message(self, format, *args):
        pass


@pytest.fixture
def demo_api_url():
    server = ThreadingHTTPServer(("127.0.0.1", 0), DemoApiHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    host, port = server.server_address
    yield f"http://{host}:{port}"

    server.shutdown()
    server.server_close()
    thread.join(timeout=2)
