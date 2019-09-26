from tokenizer_natashka_final import Tokenizator
import shelve
import os
from functools import total_ordering


@total_ordering 
class Position(object):
    """
    This class keeps position of the beginning of the token and that
    of its end. We regard only tokens of alphabetical and digit types.
    """
    
    def __init__(self, wordbeg, wordend):
        """
        Creates an example of class Position
        """
        self.wordbeg = wordbeg
        self.wordend = wordend

    def __eq__(self, obj):
        """
        This method compares two tokens  by their initial and final
        symbol positions.
        @param self: Token positions which we are to compare
        @param obj: Token positions which we compare with our 'self' Token positions
        @return: True in case of equality, False in the opposite case
        """
        return (self.wordbeg == obj.wordbeg and self.wordend == obj.wordend)

    def __lt__(self, obj):
        "Comparison"
        return self.wordbeg < obj.wordbeg
        
    def __repr__(self):
        """
        This method represents an example of class Position in an appropriate
        way. Example of how does it look like: (8; 12)
        """
        return ('(' + str(self.wordbeg) + ';' + ' ' + str(self.wordend) + ')')

    
@total_ordering 
class Position_with_lines(object):
    """
    This class keeps position of the beginning of the token, that
    of its end and the number of the line. We regard only tokens of alphabetical and digit types.
    attribute wordbeg: position of the beginning of the Token
    attribute wordend: position of the end of the Token
    attribute line: number of the line where the Token occurs
    """

    def __init__(self, wordbeg, wordend, line):
        """
        Creates an example of the class Position.
        """
        self.wordbeg = wordbeg
        self.wordend = wordend
        self.line = line
        
    def __eq__(self, obj):
        """
        This method compares two tokens  by their initial and final
        symbol positions.
        @param self: Token positions which we are to compare
        @param obj: Token positions which we compare with our 'self' Token positions
        @return: True in case of equality, False in the opposite case
        """
        return (self.wordbeg == obj.wordbeg and self.wordend == obj.wordend
                and self.line == obj.line)
    
    def __lt__(self, obj):
        "Comparison"
        if self.line == obj.line:
            return self.wordbeg < obj.wordbeg
        else:
            return self.line < obj.line

    def __repr__(self):
        """
        This method represents an example of class Position in a following
        way: (8, 12; line:7)
        """
        return ('(' + str(self.wordbeg) + ',' + ' ' + str(self.wordend) + ';' + 
                ' line:' + str(self.line) + ')')
    
    
class Indexer(object):
    """
    Class which contains 2 methods for indexing text(creating a database
    with positions of all tokens in the text): the one that regards
    lines and the one that does not. 
    """

    def __init__(self, databasename):
        """
        Creates an example of class Indexer
        @param database: name of the database where data after indexing will
        be stored.
        """
        self.database = shelve.open(databasename, writeback=True)

    def index(self, filename):
        """
        This method indexes text and adds all alphabetical and digital
        tokens that it meet into a database with the text positions of
        their beginning and end. 
        @param filename: name of the text file to be indexed
        """
        t = Tokenizator()
        # checking the existance of the file during its opening
        try:
            file = open(filename)       
        except IOError:
            raise FileNotFoundError("File is not found")
        # cycle on the text as on one string
        for token in t.generate_alpha_and_digits(file.read()):
            self.database.setdefault(token.word,{}).setdefault(
                filename,[]).append(Position(token.position,
                    (token.position+len(token.word))))
        file.close()
        # save and close database
        self.database.sync()
    
    def index_with_lines(self, filename):
        """
        This method indexes text and adds all alphabetical and digital
        tokens that it meet into a database with the text positions of
        their beginning and end, and a number of the line in which
        the token occurs. 
        @param filename: name of the text file to be indexed
        """
        t = Tokenizator()
        # checking the existance of the file during its opening
        try:
            file = open(filename)       
        except IOError:
            raise FileNotFoundError("File is not found")
        # cycle on each string of the text one after one
        for linenumber, line in enumerate(file):
            for token in t.generate_with_types(line):
                if ((token.typ=="a") or (token.typ=="d")):
                    self.database.setdefault(token.word,{}).setdefault(
                        filename,[]).append(Position_with_lines(
                            token.position, (token.position+len(token.word)),linenumber))
        file.close()
        # save and close database
        self.database.sync()

    def closeDatabase(self):
        """
        This method allows to close database.
        """
        self.database.close()
        
def main():
    indexer = Indexer('database')
    file = open('text.txt', 'w')
    file.write('это мое предложение')
    file.close()
    indexer.index('text.txt')
    os.remove('text.txt')
    file2 = open('text2.txt', 'w')
    file2.write('this is a sentence \r\nto be be indexed')
    file2.close()
    indexer.index_with_lines('Плутон.txt')
    os.remove('text2.txt')

    #indexer2.index_with_lines('tolstoy1.txt')
    #indexer2.index_with_lines('tolstoy2.txt')
    #indexer2.index_with_lines('tolstoy3.txt')
    #indexer2.index_with_lines('tolstoy4.txt')
    indexer.closeDatabase()
    #print(dict(indexer.database.get("небо", {})))
    #indexer.closeDatabase()
    
if __name__=='__main__':
    main()
