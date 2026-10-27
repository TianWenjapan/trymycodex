"""Serve the admin page and proxy its log requests to the local backend."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen
from urllib.error import URLError


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="administrator", **kwargs)

    def do_GET(self):
        if self.path.split("?", 1)[0] != "/api/logs":
            return super().do_GET()
        query = "?" + self.path.split("?", 1)[1] if "?" in self.path else ""
        try:
            with urlopen("http://127.0.0.1:8001/logs" + query, timeout=10) as response:
                body = response.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
        except (URLError, TimeoutError):
            self.send_error(502, "Backend unavailable")


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
