import indexer
import os
import shelve
from tokenizer_natashka_final import Tokenizator


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
        the position of the beginning of the word, that of its end, and
        the number of the line in which this token occurs).
        @param tokenquery: the token to be looked for in the database
        """
        if not isinstance(tokenquery, str):
            raise TypeError
        return self.database.get(tokenquery,{})

    def several_tokens_search(self, tokenquerystring):
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
        #print(searchresultarray)
        filesset = set(searchresultarray[0])
        for queryresult in searchresultarray:
            filesset.intersection_update(queryresult)
        #print(filesset)
        resultedsearchdict = {}
        for file in filesset:
            for token in tokenizerresult:
                #print(tokenizerresult)
                resultedsearchdict.setdefault(file,[]).extend(
                    self.database[token.word][file])
        return resultedsearchdict

def main():
    indexing = indexer.Indexer("database")
    file = open('text.txt', 'w')
    file.write('На розовом небе много фиолетовых облачков небе небе.')
    #file.write('There are only kittens!')
    file.close()
    indexing.index_with_lines('text.txt')
    os.remove('text.txt')
    file2 = open('text2.txt', 'w')
    file2.write('На розовом небе много облачков небе небе.')
    file2.close()
    indexing.index_with_lines('text2.txt')
    os.remove('text2.txt')
    file3 = open('text3.txt', 'w')
    file3.write('На небе много облачков небе небе.')
    file3.close()
    indexing.index_with_lines('text3.txt')
    os.remove('text3.txt')
    indexing.closeDatabase()
    search = SearchEngine("database")
    #tokenquery = "only"
    tokenquery = "облачков розовом небе"
    #print(search.search_by_token(tokenquery))
    #print(tokenquery, dict(search.search_by_token(tokenquery)))
    print(search.several_tokens_search(tokenquery))

if __name__=='__main__':
    main()
