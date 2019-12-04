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
                            <input type="hidden" name="offset" value = "0">
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
        try:
            limit = int(limit)
            if limit < 0:
                limit = 0
        except ValueError:
            self.wfile.write(bytes("Wrong query", encoding="UTF-8"))
            
        offset = form.getvalue("offset")
        if not offset:
            offset = 0
        elif int(offset) < 0:
            offset = 0
        else:
            offset = int(offset)
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
                                <input type="number" name="limit" value = "%d">
                                <br>
                                <br>
                                <input type="submit" name="action" value = "Beginning">
                            """ % (tokenquery, limit), encoding="utf-8"))
            # limit - how many files to show on the page at once
            # offset - the number of a document from which to show citations
            docnumber = 0
            sortedkeys = list(searchresult.keys())
            sortedkeys.sort()

            actiontype = str(form.getvalue("action"))
            if actiontype == "Beginning":
                offset = 0
            elif actiontype == "Forward":
                offset = offset + limit
            elif actiontype == "Back":
                offset = offset - limit

            if offset == 0:
                self.wfile.write(bytes("""<input type="submit" name="action" value = "Back" disabled>""", encoding="utf-8"))
            else:
                self.wfile.write(bytes("""<input type="submit" name="action" value = "Back"> """, encoding="utf-8"))
            nextpagesearchresult = self.server.search_engine.lim_off_context_window_search(tokenquery,
                                                    limit, offset+limit, docslimoff)
            if (len(nextpagesearchresult.keys()) > 0):
                self.wfile.write(bytes("""<input type="submit" name="action" value = "Forward"> 
                            <ol>
                            <hr />""", encoding="utf-8"))
            else:
                self.wfile.write(bytes("""<input type="submit" name="action" value = "Forward" disabled>
                            <ol>
                            <hr />""", encoding="utf-8"))
                               
            for doc in sortedkeys:
                # getting doclimit and docoffset for a particular document
                doclimit = form.getvalue("doc%dlimit" % docnumber)
                if not doclimit:
                    doclimit = 3
                elif round(int(doclimit)) < 0:
                    doclimit = 0
                else: doclimit = round(int(doclimit))
                docoffset = form.getvalue("doc%doffset" % docnumber)
                if not docoffset:
                    docoffset = 0
                elif int(docoffset) < 0:
                    docoffset = 0
                else: docoffset = int(docoffset)

                docactiontype = str(form.getvalue("action%d" % docnumber))
                if docactiontype == "Beginning":
                    docoffset = 0
                elif docactiontype == "Forward":
                    docoffset = docoffset + doclimit
                elif docactiontype == "Back":
                    docoffset = docoffset - doclimit
                
                docslimoff[docnumber] = [doclimit, docoffset]
                docnumber += 1
            
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
                    <input type="number" name="doc%dlimit" placeholder = "cit.limit in the doc" value = "%d">
                    <input type="hidden" name="doc%doffset" placeholder = "cit.offset in the doc" value = "%d">
                    <br>
                    <input type="submit" name="action" value = "Beginning">
                    """ % (x, docslimoff[x][0], x, docslimoff[x][1]), encoding="utf-8"))
                if docslimoff[x][1] == 0:
                    self.wfile.write(bytes("""<input type="submit" name="action%d" value = "Back" disabled>""" % x, encoding="utf-8"))
                else:
                    self.wfile.write(bytes("""<input type="submit" name="action%d" value = "Back"> """ % x, encoding="utf-8"))
                intermeddoclimoff = docslimoff
                intermeddoclimoff[x][1] = intermeddoclimoff[x][1] + intermeddoclimoff[x][0]
                nextpagesearchresult = self.server.search_engine.lim_off_context_window_search(tokenquery,
                                                        limit, offset, intermeddoclimoff)
                if (len(nextpagesearchresult.keys()) > 0 and intermeddoclimoff[x][0] != 0):
                    self.wfile.write(bytes("""<input type="submit" name="action%d" value = "Forward">""" % x, encoding="utf-8"))
                else:
                    self.wfile.write(bytes("""<input type="submit" name="action%d" value = "Forward" disabled>""" % x, encoding="utf-8"))
                
            self.wfile.write(bytes("""<input type="hidden" name="offset" value = "%d">
                                </form>
                            </ol>
                        </body>
                    </html>
                    """ % offset, encoding="utf-8"))

        
def main():
    server = HTTPServer(('', 8000), RequestHandler)
    server.search_engine = SearchEngine("vim")
    server.serve_forever()

if __name__ == "__main__":
    main()
