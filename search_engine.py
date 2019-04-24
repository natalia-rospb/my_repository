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
        
    def __eq__(self, obj):
        """
        This method compares two window positions by their parameters
        @param self: Token positions which we are to compare
        @param obj: Token positions which we compare with our 'self' Token positions
        @return: True in case of equality, False in the opposite case
        """
        return (self.start == obj.start and self.end == obj.end
                and self.line == obj.line and self.doc == obj.doc)


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
        return ((self.windowposition.start < obj.windowposition.start) and
                (self.windowposition.doc == obj.windowposition.doc))
    
    def get_context_window_one_position_one_file(tokenposition, doc, leftcontext, rightcontext):
        """
        This method performs several_tokens_search in text, saves necessary
        strings as its attributes and finally is able to represent context
        window of customizable size.
        @param searchresult: database we get after search engine run
        @param leftcontext: number of words from the left side of the token
        to be added to the context window
        @param rightcontext: number of words from the right side of the token
        to be added to the context window
        @return mylist: list with context windows. With the method __repr__
        it can(will) be presented as a citation from the text.
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
        mycontextwindow = ContextWindow(contextline, indexer.Position_with_lines(
            tokenposition.wordbeg, tokenposition.wordend, tokenposition.line),
                            WindowPosition(leftstart,rightend,lineno,doc))
        return mycontextwindow

    def get_context_window(searchresult, leftcontext, rightcontext):
        mylistfordoc = []
        mybigdict = {}
        for doc in searchresult:
            mybigdict[doc]=[]
            for tokenposition in searchresult[doc]:
                cw = ContextWindow.get_context_window_one_position_one_file(tokenposition,
                                                        doc, leftcontext, rightcontext)
                mybigdict[doc].append(cw)
        for doc in mybigdict:
            mybigdict[doc] = ContextWindow.check_and_unite_context_windows(mybigdict[doc])
        return mybigdict

    def check_and_unite_context_windows(mybiglist):
        mybiglist.sort()
        i = 0
        if (len(mybiglist)>1):
            while (i < len(mybiglist)-1):
                if(mybiglist[i].windowposition.doc==mybiglist[i+1].windowposition.doc):
                    if (mybiglist[i].windowposition.line==mybiglist[i+1].windowposition.line):
                        if ((mybiglist[i].windowposition.start < mybiglist[i+1].windowposition.end)
                            and (mybiglist[i].windowposition.end > mybiglist[i+1].windowposition.start)):
                            mynewcw = ContextWindow(mybiglist[i+1].wholestring,
                                [mybiglist[i].tokenposition,mybiglist[i+1].tokenposition],
                                WindowPosition(mybiglist[i].windowposition.start, mybiglist[i+1].windowposition.end,
                                mybiglist[i+1].windowposition.line, mybiglist[i+1].windowposition.doc))
                            mybiglist.pop(i+1)
                            mybiglist.insert(i+1, mynewcw)
                            mybiglist.pop(i)
                        else:
                            i = i+1
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
    tokenquery2 = "небе много"
    
    searchresult = dict(search.several_tokens_search(tokenquery2))  
    print(searchresult)
    print(ContextWindow.get_context_window(searchresult,2,2))
##    print(ContextWindow.get_context_window_one_position_one_file
##          (indexer.Position_with_lines(8,13,0),"text.txt",0,1))

if __name__=='__main__':
    main()
