from http.server import HTTPServer, BaseHTTPRequestHandler

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header("Location", f"http://127.0.0.1:8501{self.path}")
        self.end_headers()

    def do_HEAD(self):
        self.send_response(302)
        self.send_header("Location", f"http://127.0.0.1:8501{self.path}")
        self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8502), RedirectHandler)
    server.serve_forever()
