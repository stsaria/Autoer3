from http.server import HTTPServer, CGIHTTPRequestHandler, BaseHTTPRequestHandler, ThreadingHTTPServer

class Handler(CGIHTTPRequestHandler):
    cgi_directories = ["/cgi-bin"]
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = "Hello, world!"
        self.wfile.write(bytes(message, "utf8"))
        return
PORT = 8080
httpd = ThreadingHTTPServer(("", PORT), Handler)
httpd.serve_forever()