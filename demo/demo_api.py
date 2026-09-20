"""Small local API used to demonstrate Sentinel without external dependencies."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8765


class DemoApiHandler(BaseHTTPRequestHandler):
    def _write_json(self, status_code: int, payload) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/":
            self._write_json(200, {"status": "ok", "service": "sentinel-demo"})
            return

        if self.path == "/users":
            self._write_json(200, [{"id": 1, "name": "Sentinel Demo"}])
            return

        self._write_json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/login":
            self._write_json(404, {"error": "not found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(content_length) or b"{}")

        if payload == {"username": "demo", "password": "sentinel"}:
            self._write_json(200, {"token": "demo-token"})
            return

        self._write_json(401, {"error": "invalid credentials"})

    def log_message(self, format, *args) -> None:
        pass


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), DemoApiHandler)
    print(f"Sentinel demo API running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
