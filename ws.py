from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        '''
        Creates a HTML page with a button and a field. This method
        is used when a user opens the page.
        '''
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = '''
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query">
                            <input type="submit" value="Search">
                        </form>
                    </body>
                </html>
                '''
        self.wfile.write(bytes(html, encoding="UTF-8"))

def main():
    server = HTTPServer(('', 80), RequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
