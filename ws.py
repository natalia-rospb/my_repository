'''
Methods for working with the web server.
'''
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from search_engine import SearchEngine, ContextWindow


class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        '''
        Creates a HTML page with a button and a field. This method
        is used when a user opens the page.
        '''
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query">
                            <input type="submit" value="Search">
                        </form>
                    </body>
                </html>
                """
        self.wfile.write(bytes(html, encoding="utf-8"))

    def do_POST(self):
        '''
        Enables to search in database and see the results as an ordered list of contexts.
        '''
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                        environ={'REQUEST_METHOD': 'POST'})
        tokenquery = str(form.getvalue("query"))
        search = SearchEngine("vim")
        searchresult = search.highlighted_context_window_search(tokenquery, 1, 1)
        print(searchresult)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        if not searchresult:
            self.wfile.write(bytes("Nothing found", encoding="UTF-8"))
        else:
            self.wfile.write(bytes("""
                    <html>
                        <body>
                            <form method="post">
                                <input type="text" name="query">
                                <input type="submit" value="Search">
                            </form>
                            <ol>
                            """, encoding="utf-8"))
            for doc in searchresult.keys():
                self.wfile.write(bytes("<li><p>%s</p></li>" % doc, encoding="UTF-8"))
                for cw in searchresult[doc]:
                    self.wfile.write(bytes("<ul><p>%s</p></ul>" % cw, encoding="UTF-8"))
            self.wfile.write(bytes("""
                            </ol>
                        </body>
                    </html>
                    """, encoding="utf-8"))

        
def main():
    server = HTTPServer(('', 80), RequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
