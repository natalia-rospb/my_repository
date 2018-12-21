import indexer
import os
import shelve


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

   # def several_tokens_search(self, tokenquerystring):
        

def main():
    indexing = indexer.Indexer("database")
    file = open('text.txt', 'w')
    file.write('На розовом небе много фиолетовых облачков небе небе.')
    #file.write('There are only kittens!')
    file.close()
    indexing.index_with_lines('text.txt')
    os.remove('text.txt')
    indexing.closeDatabase()
    search = SearchEngine("database")
    #tokenquery = "only"
    tokenquery = "небе"
    #print(search.search_by_token(tokenquery))
    print(tokenquery, dict(search.search_by_token(tokenquery)))

if __name__=='__main__':
    main()
