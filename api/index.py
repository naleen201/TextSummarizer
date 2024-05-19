# api/index.py

from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
from io import BytesIO
from app import app

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def handle_request(self, method):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        query_string = parse_qs(self.path.split('?', 1)[-1])
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': self.path.split('?', 1)[0],
            'QUERY_STRING': self.path.split('?', 1)[-1],
            'CONTENT_TYPE': self.headers.get('Content-Type', ''),
            'CONTENT_LENGTH': str(content_length),
            'wsgi.input': BytesIO(body),
            'wsgi.url_scheme': 'http',
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'HTTP_COOKIE': self.headers.get('Cookie', ''),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'HTTP_HOST': self.headers.get('Host', ''),
        }
        for key, value in query_string.items():
            environ[f'QUERY_STRING_{key}'] = value[0]
        headers = []
        def start_response(status, response_headers, exc_info=None):
            headers[:] = [status, response_headers]
        result = app(environ, start_response)
        self.send_response(int(headers[0].split(' ')[0]))
        for key, value in headers[1]:
            self.send_header(key, value)
        self.end_headers()
        if isinstance(result, bytes):
            self.wfile.write(result)
        else:
            for data in result:
                self.wfile.write(data)