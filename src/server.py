from concurrent.futures.process import ProcessPoolExecutor
from http.server import BaseHTTPRequestHandler, HTTPServer

from src.environmentvariables import EnvironmentVariables
from src.scraper import Scraper


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Simple HTTP request handler only for POST requests.
    """
    def do_POST(self):
        """
        If path is '/scrape', then it responds with 200 and starts scraping in the background. Otherwise, responds 404.

        Any kind of parameters are ignored.
        """
        if self.path == '/scrape':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('Going to scrape!'.encode('utf8'))
            self.server.pool.submit(Scraper.scrape)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write('The requested path was not found.'.encode('utf8'))


if __name__ == '__main__':
    httpd = HTTPServer(('', int(EnvironmentVariables.PORT)), SimpleHTTPRequestHandler)
    httpd.pool = ProcessPoolExecutor(max_workers=1)
    httpd.serve_forever()
