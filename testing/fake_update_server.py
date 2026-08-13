#!/usr/bin/env python3
"""Serve a harmless fake Porn Fetch 4.0 update for QML UI testing."""

import argparse
import json

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class FakeUpdateHandler(BaseHTTPRequestHandler):
    server_version = "PornFetchFakeUpdate/1.0"

    def do_GET(self) -> None:
        if self.path == "/update":
            host, port = self.server.server_address
            base_url = f"http://{host}:{port}"
            self._send_json(
                {
                    "version": "latest - 4.0",
                    "url": f"{base_url}/downloads/authenticated",
                    "anonymous_download": f"{base_url}/downloads/anonymous",
                    "important_info": (
                        "<p><strong>Development test update.</strong> This is fake data "
                        "served from your computer. No application files will be installed.</p>"
                    ),
                    "changelog": (
                        "<h3>Porn Fetch 4.0 — Test Changelog</h3>"
                        "<ul>"
                        "<li>Added the new QML update notification.</li>"
                        "<li>Added rich-text release notes and external download links.</li>"
                        "<li>Added automatic-update progress reporting.</li>"
                        "<li>Fixed several imaginary bugs for this test release.</li>"
                        "</ul>"
                        "<p><strong>Reminder:</strong> This changelog is not a real release.</p>"
                    ),
                }
            )
            return

        if self.path in {"/downloads/authenticated", "/downloads/anonymous"}:
            body = b"This is a fake update download used only to test the popup.\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(404, "Not Found")

    def _send_json(self, payload: dict) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, message: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {message % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), FakeUpdateHandler)
    print(f"Fake update endpoint: http://{args.host}:{args.port}/update")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping fake update server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
