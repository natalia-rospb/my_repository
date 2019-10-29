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
                            <input type="text" name="query" placeholder = "query">
                            <input type="submit" value="Search">
                            <br>
                            <br>
                            <input type="limit" name="limit" placeholder = "docs limit">
                            <input type="offset" name="offset" placeholder = "docs offset">
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
        limit = form.getvalue("limit")
        if not limit:
            limit = 5
        else: limit = int(limit)
        offset = form.getvalue("offset")
        if not offset:
            offset = 0
        else: offset = int(offset)

        docslimoff = [0] * limit
        for i in range(limit):
                docslimoff[i] = [3,0]
        searchresult = self.server.search_engine.lim_off_context_window_search(tokenquery,
                                                    limit, 0, docslimoff)
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
                                <input type="text" name="query" value="%s">
                                <input type="submit" value="Search">
                                <br>
                                <br>
                                <input type="limit" name="limit" value = "%d">
                                <input type="offset" name="offset" value = "%d">
                                <hr />
                            <ol>
                            """ % (tokenquery, limit, offset), encoding="utf-8"))
            # limit - how many files to show on the page at once
            # offset - the number of an element from which to show citations
            docnumber = 0
            sortedkeys = list(searchresult.keys())
            sortedkeys.sort()
            for doc in sortedkeys:
                
                # getting doclimit and docoffset for a particular document
                doclimit = form.getvalue("doc%dlimit" % docnumber)
                if not doclimit:
                    doclimit = 3
                else: doclimit = int(doclimit)
                docoffset = form.getvalue("doc%doffset" % docnumber)
                if not docoffset:
                    docoffset = 0
                else: docoffset = int(docoffset)
                docslimoff[docnumber] = [doclimit, docoffset]
                docnumber += 1
            ##docslimoff = docslimoff[offset:]
            searchresultlimoff = self.server.search_engine.lim_off_context_window_search(tokenquery,
                                                limit, offset, docslimoff)
            sortedkeyslimoff = list(searchresultlimoff.keys())
            sortedkeyslimoff.sort()
            for x, doc in enumerate(sortedkeyslimoff):
                # x = docnumber; docslimoff[x][0] = doclimit; docslimoff[x][1] = docoffset
                self.wfile.write(bytes("<li><p>%s</p></li><ul>" % doc, encoding="UTF-8"))
                for cw in searchresultlimoff[doc]:
                    self.wfile.write(bytes("<li><p>%s</p></li>" % cw, encoding="UTF-8"))
                self.wfile.write(bytes("</ul>", encoding="utf-8"))
                self.wfile.write(bytes("""
                    <input type="doc%dlimit" name="doc%dlimit" placeholder = "cit.limit in the doc" value = "%d">
                    <input type="doc%doffset" name="doc%doffset" placeholder = "cit.offset in the doc" value = "%d">
                        """ % (x, x, docslimoff[x][0], x, x, docslimoff[x][1]), encoding="utf-8"))
                
            self.wfile.write(bytes("""</form>
                            </ol>
                        </body>
                    </html>
                    """, encoding="utf-8"))

        
def main():
    server = HTTPServer(('', 8000), RequestHandler)
    server.search_engine = SearchEngine("vim")
    server.serve_forever()

if __name__ == "__main__":
    main()
