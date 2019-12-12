'''
Methods for working with the web server.
'''
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from search_engine import SearchEngine, ContextWindow
import time


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
                            <input type="number" name="limit" placeholder = "docs limit">
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
        print("new")
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                        environ={'REQUEST_METHOD': 'POST'})
        tokenquery = str(form.getvalue("query"))

        # limit - how many files to show on the page at once
        # offset - the number of a document from which to show citations
        limit = form.getvalue("limit")
        if not limit:
            limit = 5
        elif int(limit) < 0:
            limit = 0
        else:
            limit = int(limit)

        offset = form.getvalue("offset")
        if not offset:
            offset = 0
        elif int(offset) < 0:
            offset = 0
        else:
            offset = int(offset)
        
        # getting doclimit and docoffset for a particular document
        docslimoff = []
        for i in range(limit):
            doclimit = form.getvalue("doc%dlimit" % i)
            if not doclimit:
                doclimit = 3
            elif round(int(doclimit)) < 0:
                    doclimit = 0
            else: doclimit = int(doclimit)
            docoffset = form.getvalue("doc%doffset" % i)
            if not docoffset:
                docoffset = 0
            elif int(docoffset) < 0:
                docoffset = 0
            else: docoffset = int(docoffset)
            docslimoff.append([doclimit, docoffset])

        # necessary for checking the existence of results for the next page
        # if the results are confined to the current page, the button "Forward" will be disabled
        extlimit = limit + 1
        extdoclimoff = []
        for item in docslimoff:
            extdoclimoff.append(item)
        extdoclimoff.append([3,0])
        for i in range(extlimit):
            extdoclimoff[i][0] += 1
        
        # getting the action for documents in a whole 
        actiontype = str(form.getvalue("action"))
        if actiontype == "Beginning":
            offset = 0
        elif actiontype == "Forward":
            offset = offset + limit
        elif actiontype == "Back":
            offset = offset - limit

        # getting the action for each document
        for i in range(limit):
            docactiontype = str(form.getvalue("action%d" % i))
            if docactiontype == "Beginning":
                extdoclimoff[i][1] = 0
            elif docactiontype == "Forward":
                extdoclimoff[i][1] = extdoclimoff[i][1] + extdoclimoff[i][0] - 1
            elif docactiontype == "Back":
                extdoclimoff[i][1] = extdoclimoff[i][1] - extdoclimoff[i][0] + 1
            extdoclimoff[i] = [extdoclimoff[i][0], extdoclimoff[i][1]]

        start_time = time.time()
        # search itself
        extsearchresult = self.server.search_engine.lim_off_context_window_search_acc(tokenquery,
                                                    extlimit, offset, extdoclimoff)
        print('time:', time.time() - start_time)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        if not extsearchresult:
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
                                <input type="submit" name="action" value = "Beginning">
                            """ % (tokenquery, limit), encoding="utf-8"))
            sortedkeys = list(extsearchresult.keys())
            sortedkeys.sort()
            try:
                sortedkeys.pop(limit)
            except IndexError:
                pass
            # disabling of "Back" and "Forward" buttons for docs 
            if offset == 0:
                self.wfile.write(bytes("""<input type="submit" name="action" value = "Back" disabled>""", encoding="utf-8"))
            else:
                self.wfile.write(bytes("""<input type="submit" name="action" value = "Back"> """, encoding="utf-8"))
            if (len(extsearchresult.keys()) < extlimit) or (limit == 0):
                self.wfile.write(bytes("""<input type="submit" name="action" value = "Forward" disabled> 
                            <ol>
                            <hr />""", encoding="utf-8"))
            else:
                self.wfile.write(bytes("""<input type="submit" name="action" value = "Forward">
                            <ol>
                            <hr />""", encoding="utf-8"))
            
            for x, doc in enumerate(sortedkeys):
                # x = doc number; docslimoff[x][0] = doclimit; docslimoff[x][1] = docoffset
                self.wfile.write(bytes("<li><p>%s</p></li><ul>" % doc, encoding="UTF-8"))
                i = 0
                for cw in extsearchresult[doc]:
                    if (i < extdoclimoff[x][0]-1):
                        self.wfile.write(bytes("<li><p>%s</p></li>" % cw, encoding="UTF-8"))
                    i += 1
                self.wfile.write(bytes("</ul>", encoding="utf-8"))
                self.wfile.write(bytes("""
                    <input type="number" name="doc%dlimit" placeholder = "cit.limit in the doc" value = "%d">
                    <input type="hidden" name="doc%doffset" placeholder = "cit.offset in the doc" value = "%d">
                    <br>
                    <input type="submit" name="action%d" value = "Beginning">
                    """ % (x, extdoclimoff[x][0] - 1, x, extdoclimoff[x][1], x), encoding="utf-8"))
                # disabling of "Back" and "Forward" buttons for citations in every doc
                if extdoclimoff[x][1] < 1:
                    self.wfile.write(bytes("""<input type="submit" name="action%d" value = "Back" disabled>""" % x, encoding="utf-8"))
                else:
                    self.wfile.write(bytes("""<input type="submit" name="action%d" value = "Back"> """ % x, encoding="utf-8"))
                if ((len(extsearchresult[doc]) < extdoclimoff[x][0]) or (extdoclimoff[x][0] == 0)):
                    self.wfile.write(bytes("""<input type="submit" name="action%d" value = "Forward" disabled>""" % x, encoding="utf-8"))
                else:
                    self.wfile.write(bytes("""<input type="submit" name="action%d" value = "Forward">""" % x, encoding="utf-8"))
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
