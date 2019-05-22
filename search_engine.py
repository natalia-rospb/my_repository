import indexer
import os
import shelve
from tokenizer_natashka_final import Tokenizator
import linecache
import re


class SearchEngine(object):
    """
    Class which contains methods for serching positions of tokens through
    a given database: "search_by_token" and "several_tokens_search". 
    """

    def __init__(self, databasename):
        """
        Opens database for the future search
        @param databasename: name of the database in the current
        folder to be opened.
        """
        self.database = shelve.open(databasename, writeback=True)

    def closeDatabase(self):
        """
        This method allows to close database.
        """
        self.database.close()
        for filename in os.listdir(os.getcwd()):
            if (filename.startswith('database.')):
                os.remove(filename)
            if (filename.startswith('text')):
                os.remove(filename)

    def search_by_token(self, tokenquery):
        """
        This method scans the database using a key - token, and returns
        all positions of this token in the database (position includes
        the position of the beginning of the word, that of its end =
        (position jf the beginning + len(word)), and the number of the
        line in which this token occurs).
        @param tokenquery: the token to be looked for in the database
        @return: dict with tokens as keys and information about their
        positions from the database as values
        """
        if not isinstance(tokenquery, str):
            raise TypeError
        return self.database.get(tokenquery,{})

    def several_tokens_search(self, tokenquerystring):
        """
        This method scans the database for each token from tokenized
        string and applies to them method search_by_token.
        @param tokenquerystring: the sentence of tokens to be tokenized and
        processed by SearchEngine
        @return resultedsearchdict: dict with files where ALL these tokens
        were found as keys and their positions in these files accordingly
        to the token's order in the query as values
        """
        t = Tokenizator()
        if not isinstance(tokenquerystring, str):
            raise TypeError
        if (tokenquerystring == ""):
            return {}
        tokenizerresult = list(t.generate_alpha_and_digits(tokenquerystring))
        searchresultarray = []
        for token in tokenizerresult:
            if token.word not in self.database:
                return {}
            else:
                searchresultarray.append(self.search_by_token(token.word))
        # we need at least one element to create set
        filesset = set(searchresultarray[0])
        for queryresult in searchresultarray:
            # filesset contains only filenames to exlude those files in
            # which not all tokens were found
            filesset.intersection_update(queryresult)
        resultedsearchdict = {}
        for file in filesset:
            for token in tokenizerresult:
                resultedsearchdict.setdefault(file,[]).extend(
                    self.database[token.word][file])
        return resultedsearchdict

    @staticmethod
    def get_context_windows(searchresult, leftcontext, rightcontext):
        """
        This method can give you all context windows suitable for your query
        @param searchresult: database with indexed search results
        @param leftcontext: number of words from the left side of the token
        to be added to the context window
        @param rightcontext: number of words from the right side of the token
        to be added to the context window
        @return mybigdict: dictionary where document names are keys and lists of
        context windows in each document are their values
        """
        mybigdict = {}
        #constructing a dictionary of separate CWs for each position
        for doc in searchresult:
            mybigdict[doc]=[]
            for tokenposition in searchresult[doc]:
                cw = ContextWindow.get_context_window_one_position_one_file(tokenposition,
                                                        doc, leftcontext, rightcontext)
                mybigdict[doc].append(cw)
        # windows intersection
        for doc in mybigdict:
            mybigdict[doc] = SearchEngine.check_and_unite_context_windows(mybigdict[doc])
        return mybigdict

    @staticmethod
    def check_and_unite_context_windows(mybiglist):
        """
        This method works with one list and intersect its CWs if it's possible
        @param mybiglist: list in question
        @return mybigdict: resulted list with already united CWs (if there could be some)
        """
        #mybiglist.sort()
        i = 0
        if (len(mybiglist)>1):
            while (i < len(mybiglist)-1):
                if(mybiglist[i].windowposition.doc==mybiglist[i+1].windowposition.doc):
                    if (mybiglist[i].windowposition.line==mybiglist[i+1].windowposition.line):
                        if ((mybiglist[i].windowposition.start < mybiglist[i+1].windowposition.end)
                            and (mybiglist[i].windowposition.end > mybiglist[i+1].windowposition.start)):
                            if str(mybiglist[i].wholestring) == str(mybiglist[i+1].wholestring):
                                wholestring = mybiglist[i].wholestring
                            else:
                                wholestring = str(mybiglist[i].wholestring[:mybiglist[i].tokenposition.wordend + 1] +
                                     mybiglist[i+1].wholestring[mybiglist[i].tokenposition.wordend:])
                            mynewcw = ContextWindow(wholestring,
                                [mybiglist[i].tokenposition,mybiglist[i+1].tokenposition],
                                WindowPosition(mybiglist[i].windowposition.start, mybiglist[i+1].windowposition.end,
                                mybiglist[i+1].windowposition.line, mybiglist[i+1].windowposition.doc))
                            mybiglist.pop(i+1)
                            mybiglist.insert(i+1, mynewcw)
                            mybiglist.pop(i)
                        else:
                            i = i+1
        return mybiglist

    def several_tokens_search_with_customizable_context(self, tokenquerystring, leftcontext, rightcontext):
        """
        This method gives CWs of customizable size
        @param tokenquerystring: the sentence of tokens to be tokenized and
        processed by SearchEngine
        @param leftcontext: number of words from the left side of the token
        to be added to the context window
        @param rightcontext: number of words from the right side of the token
        to be added to the context window
        @return contextwindowsresult: dict with docs as keys and CWs as values
        """
        searchresult = self.several_tokens_search(tokenquerystring)
        contextwindowsresult = self.get_context_windows(searchresult, leftcontext, rightcontext)
        return contextwindowsresult

    def several_tokens_search_with_sentence_context(self, tokenquerystring, leftcontext, rightcontext):
        """
        This method enlarges CWs until sentence boundaries on both sides or, if there are no boundary, until
        the position of the start or the end of the line.
        @param tokenquerystring: the sentence of tokens to be tokenized and
        processed by SearchEngine
        @param leftcontext: number of words from the left side of the token
        to be added to the context window
        @param rightcontext: number of words from the right side of the token
        to be added to the context window
        @return contextwindowsresult: dict with docs as keys and CWs as values
        """
        contextsearch = self.several_tokens_search_with_customizable_context(tokenquerystring, leftcontext, rightcontext)
        for doc in contextsearch.keys():
            for item in contextsearch[doc]:
                item.get_sentence_context_window()
            contextsearch[doc] = SearchEngine.check_and_unite_context_windows(contextsearch[doc])
        return contextsearch

    def highlighted_context_window_search(self, tokenquerystring, leftcontext, rightcontext):
        searchresult = self.several_tokens_search(tokenquerystring)
        mybigdict = {}
        mycitationdict = {}
        #constructing a dictionary of separate CWs for each position
        for doc in searchresult:
            mybigdict[doc]=[]
            for tokenposition in searchresult[doc]:
                cw = ContextWindow.get_context_window_one_position_one_file(tokenposition,
                                                        doc, leftcontext, rightcontext)
                cw.get_context_window_bold()
                mybigdict[doc].append(cw)
        # windows intersection
        for doc in mybigdict:
            mybigdict[doc] = SearchEngine.check_and_unite_context_windows(mybigdict[doc])
            #print(doc, mybigdict[doc])  
            mycitationlist = []
            for cw in mybigdict[doc]:
                mycitationlist.append(cw.wholestring[cw.windowposition.start:cw.windowposition.end])  
            mycitationdict[doc] = mycitationlist
        return mycitationdict
                

class WindowPosition(object):
    
    def __init__(self, start, end, line, doc):
        """
        Creates an instance of the class WindowPosition.
        @param start: position of the first symbol of the window in the whole line
        @param end: position of the the last symbol of the window + 1
        @param line: number of the line in the document
        @param doc: document where we take the context window from        
        """
        self.start = start
        self.end = end
        self.line = line
        self.doc = doc
        
    def __eq__(self, obj):
        """
        This method tells if two window positions are equal by their parameters
        @param self: Token positions which we are to compare
        @param obj: Token positions which we compare with our 'self' Token positions
        @return: True in case of equality, False in the opposite case
        """
        return (self.start == obj.start and self.end == obj.end
                and self.line == obj.line and self.doc == obj.doc)


class ContextWindow(object):
    
    def __init__(self, wholestring, tokenposition, windowposition):
        """
        Creates an instance of the class ContextWindow.
        @param wholestring: whole document line where we take context window from
        @param tokenposition: object of the class indexer.Position_with_lines,
        it has wordbeg, wordend and line as attributes
        @param windowposition: object of the class WindowPosition, it has start,
        end, line and doc as attributes
        """
        self.wholestring = wholestring
        self.tokenposition = tokenposition #wordbeg, wordend, line
        self.windowposition = windowposition #start, end and line

    def __repr__(self):
        """
        This method represents each context window as follows:
        
        'text of the context window'
        [(x,y,line:z)] #tokenposition
        windowposition: start=a end=b line=c doc=d  #windowposition
        """
        return ('\n\n' + str(self.wholestring[self.windowposition.start:
                 self.windowposition.end]) + '\n' + str(self.tokenposition)
                 + '\nwindowposition:' + ' start=' + str(self.windowposition.start)
                 + ' end=' + str(self.windowposition.end) + ' line=' +
                 str(self.windowposition.line) + ' doc=' +str(self.windowposition.doc))

    def __eq__(self, obj):
        """
        This method compares two window positions by their parameters
        @param self: Token positions which we are to compare
        @param obj: Token positions which we compare with our 'self' Token positions
        @return: True in case of equality, False in the opposite case
        """
        return (self.tokenposition == obj.tokenposition
                and self.windowposition == obj.windowposition)

    def __lt__(self, obj):
        """
        This method was necessary to arrange windows sorting 
        """
        return ((self.windowposition.start < obj.windowposition.start) and
                (self.windowposition.doc == obj.windowposition.doc))
    
    @classmethod
    def get_context_window_one_position_one_file(cls, tokenposition, doc, leftcontext, rightcontext):
        """
        This method can construct a context window of customizable size.
        @param tokenposition: position of the token
        @param doc: name of the document to work with
        @param leftcontext: number of words from the left side of the token
        to be added to the context window
        @param rightcontext: number of words from the right side of the token
        to be added to the context window
        @return mycontextwindow: object of the type ContextWindow,
        window for ONE position in ONE document
        """
        tokenizerresult = []
        t = Tokenizator()
        i = 0
        lineno = tokenposition.line
        currentfile = open(doc)
        for i, line in enumerate(currentfile):
            if i == lineno:
                contextline = line
                break
        currentfile.close()
        i = 0
        # left context
        mylist = []
        myleftline = contextline[:tokenposition.wordend]
        myreversedleftline = myleftline[::-1]
        tokenizerresult = list(t.generate_alpha_and_digits(myreversedleftline))
        for i, token in enumerate(tokenizerresult):
            if i==0:
                leftstart = tokenposition.wordbeg
                if i == leftcontext:
                    leftstart = tokenposition.wordbeg
                    break
                mylist.append(token.word)
            if i>0:
                mylist.append(token.word)
                # token.position is the position of the first token's symbol
                leftstart = token.position + len(token.word)
                if i == leftcontext or i == len(tokenizerresult)-1:
                    leftstart = tokenposition.wordend - leftstart
                    break
        mylist.reverse()
        for i,token in enumerate(mylist):
            mylist[i] = token[::-1]
        # right context
        myrightline = contextline[tokenposition.wordbeg:]
        tokenizerresult = list(t.generate_alpha_and_digits(myrightline))
        for i, token in enumerate(tokenizerresult):
            if i==0:
                rightend = tokenposition.wordend
                if i == rightcontext:
                    break
            if i>0:
                mylist.append(token.word)
                rightend = token.position + len(token.word)
                if i == rightcontext or i == len(tokenizerresult)-1:
                    rightend = tokenposition.wordbeg + rightend
                    break
        mycontextwindow = cls(contextline, indexer.Position_with_lines(
            tokenposition.wordbeg, tokenposition.wordend, tokenposition.line),
                            WindowPosition(leftstart,rightend,lineno,doc))
        return mycontextwindow

    def get_sentence_context_window(self):
        """
        This method changes ContextWindow.windowposition to include complete
        sentence which results from existing ContextWindow. If existing
        ContextWindow include parts of several sentences, all of them will
        be added to the ContextWindow in question.
        """
        start_boundary = re.compile(r'[A-ZА-Я]\s[.?!]')
        end_boundary = re.compile(r'[.?!]\s[A-ZА-Я]')
        before_cw = self.wholestring[:self.windowposition.start+1]
        after_cw = self.wholestring[self.windowposition.end:]
        start_result = re.search(start_boundary, before_cw[::-1])
        end_result = re.search(end_boundary, after_cw)
        # right sentence boundary
        if end_result == None:
            self.windowposition.end = len(self.wholestring)
        else:
            self.windowposition.end = self.windowposition.end + end_result.start() + 1
        # left sentence boundary    
        if start_result == None:
            self.windowposition.start = 0
        else:
            self.windowposition.start = len(before_cw) - start_result.start() - 1

    def get_context_window_bold(self):
        self.wholestring = self.wholestring[:self.tokenposition.wordend] + '</B>' + self.wholestring[self.tokenposition.wordend:]
        self.windowposition.end += 7
        self.wholestring = self.wholestring[:self.tokenposition.wordbeg] + '<B>' + self.wholestring[self.tokenposition.wordbeg:]
        self.tokenposition.wordend += 7
    
def main():
    indexing = indexer.Indexer("database")
    file = open('text.txt', 'w')
    file.write('На небе. Много. Фиолетовых облачков')
    file.close()
    indexing.index_with_lines('text.txt')
    file2 = open('text2.txt', 'w')
    file2.write('На розоватом. Небе небе Много облачков маленьких. J')
    file2.close()
    indexing.index_with_lines('text2.txt')
    file3 = open('text3.txt', 'w')
    file3.write('На голубом преголубом небе много облачков небе. \n птичек \n звезд')
    file3.close()
    indexing.index_with_lines('text3.txt')
    indexing.closeDatabase()
    search = SearchEngine("database")
    tokenquery = "небе"
    tokenquery2 = "Много"
##    searchresult = search.several_tokens_search_with_sentence_context(tokenquery, 2, 2) 
##    print(searchresult)
    contextsearch = search.highlighted_context_window_search(tokenquery, 2, 2)
    print(contextsearch)
    search.closeDatabase()
    

if __name__=='__main__':
    main()
