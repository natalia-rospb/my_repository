import indexer
import os
import shelve
from tokenizer_natashka_final import Tokenizator
import linecache


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


class WindowPosition(object):
    
    def __init__(self, start, end, line, doc):
        """
        Creates an example of the class WindowPosition.
        """
        self.start = start
        self.end = end
        self.line = line
        self.doc = doc

class ContextWindow(object):
    
    def __init__(self, wholestring, tokenposition, windowposition):
        self.wholestring = wholestring
        self.tokenposition = tokenposition #wordbeg, wordend, line
        self.windowposition = windowposition #start, end and line

    def __repr__(self):
        """
        This method represents array with tokens' positions in the text as
        a citation. 
        """
        return ('\n\n' + str(self.wholestring[self.windowposition.start:
                 self.windowposition.end]) + '\n' + str(self.tokenposition)
                 + '\nwindowposition:' + ' start=' + str(self.windowposition.start)
                 + ' end=' + str(self.windowposition.end) + ' line=' +
                 str(self.windowposition.line) + ' doc=' +str(self.windowposition.doc))
    
    def get_context_window_for_one_word(searchresult, leftcontext, rightcontext):
        """
        This method performs several_tokens_search in text, saves necessary
        strings as its attributes and finally is able to represent context
        window of customizable size.
        @param searchresult: database we get after search engine run
        @param leftcontext: number of words from the left side of the token
        to be added to the context window
        @param rightcontext: number of words from the right side of the token
        to be added to the context window
        @return mylist: list with words close to the query in question in
        the text. With the method __repr__ it can(will) be presented as a
        citation from the text.
        """
        tokenizerresult = []
        t = Tokenizator()
        i = 0
        mybiglist = []
        for doc in searchresult:
            for tokenposition in searchresult[doc]:
                lineno = tokenposition.line
                currentfile = open(doc)
                for i, line in enumerate(currentfile):
                    if i == lineno:
                        contextline = line
                        break
                currentfile.close()
                i = 0
                #left context
                mylist = []
                myleftline = contextline[:tokenposition.wordend]
                myreversedleftline = myleftline[::-1]
                tokenizerresult = list(t.generate_alpha_and_digits(myreversedleftline))
                for i, token in enumerate(tokenizerresult):
                    if i==0:
                        mylist.append(token.word)
                        leftstart = tokenposition.wordbeg
                    if i>0:
                        mylist.append(token.word)
                        #token.position is the position of the first token's symbol
                        leftstart = token.position + len(token.word)
                        if i == leftcontext or i == len(tokenizerresult)-1:
                            leftstart = tokenposition.wordend - leftstart
                            break
                mylist.reverse()
                for i,token in enumerate(mylist):
                    mylist[i] = token[::-1]
                #right context
                myrightline = contextline[tokenposition.wordbeg:]
                tokenizerresult = list(t.generate_alpha_and_digits(myrightline))
                for i, token in enumerate(tokenizerresult):
                    if i==0:
                        rightend = tokenposition.wordend
                    if i>0:
                        mylist.append(token.word)
                        rightend = token.position + len(token.word)
                        if i == rightcontext:
                            rightend = tokenposition.wordbeg + rightend
                            break
                mycontextwindow = ContextWindow(contextline, indexer.Position_with_lines(
                    tokenposition.wordbeg, tokenposition.wordend, tokenposition.line),
                                    WindowPosition(leftstart,rightend,lineno,doc))
                mybiglist.append(mycontextwindow)
                result = check_and_unite_context_windows(mybiglist)
        return result

    def check_and_unite_context_windows(mybiglist):
        for i in enumerate(mybiglist):
            if (mybiglist[i].windowposition.doc==mybiglist[i+1].windowposition.doc):
                if (mybiglist[i].windowposition.line==mybiglist[i+1].windowposition.line):
                    if (mybiglist[i].windowposition.start < mybiglist[i+1].windowposition.end) and (mybiglist[i].windowposition.end > mybiglist[i+1].windowposition.start):
                            mynewcw = ContextWindow(mybiglist[i+1].wholestring,
                                [mybiglist[i].tokenposition,mybiglist[i+1].tokenposition],
                                    WindowPosition(mybiglist[i+1].windowposition.start,mybiglist[i].windowposition.end,
                                     mybiglist[i+1].windowposition.line,mybiglist[i+1].windowposition.doc))
                        mybiglist.append(mynewcw)
                        mybiglist.remove(mybiglist[i],mybiglist[i+1])
        return mybiglist
                        

def main():
    indexing = indexer.Indexer("database")
    file = open('text.txt', 'w')
    file.write('На небе много фиолетовых облачков')
    file.close()
    indexing.index_with_lines('text.txt')
    #os.remove('text.txt')
    file2 = open('text2.txt', 'w')
    file2.write('На розоватом небе небе много облачков маленьких')
    file2.close()
    indexing.index_with_lines('text2.txt')
    #os.remove('text2.txt')
    file3 = open('text3.txt', 'w')
    file3.write('На голубом преголубом небе много облачков небе \n птичек \n звезд')
    file3.close()
    indexing.index_with_lines('text3.txt')
    #os.remove('text3.txt')
    indexing.closeDatabase()
    search = SearchEngine("database")
    tokenquery = "облачков розовом небе"
    tokenquery2 = "небе"
    searchresult = dict(search.search_by_token(tokenquery2))
    print(searchresult)
    print(ContextWindow.get_context_window_for_one_word(searchresult,2,2))
    #print(tokenquery2, dict(search.search_by_token(tokenquery2)))
    #print(tokenquery, search.several_tokens_search(tokenquery))

if __name__=='__main__':
    main()
