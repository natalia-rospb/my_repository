from tokenizer_natashka_final import Tokenizator
import shelve
import os


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
        
    def __repr__(self):
        """
        This method represents an example of class Position in an appropriate
        way. Example of how does it look like: (8; 12)
        """
        return ('(' + self.wordbeg + ';' + ' ' + self.wordend + ')')
    

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

    def __repr__(self):
        """
        This method represents an example of class Position in an appropriate
        way. Example of how does it look like: (8; 12)
        """
        return ('(' + self.wordbeg + ';' + ' ' + self.wordend +
                ' line:' + self.line + ')')
    
    
class Indexer(object):

    def __init__(self, database):
        self.database = shelve.open(database, writeback=True)

    def index (self, filename):
        t = Tokenizator()
        try:
            file = open(filename)       
        except IOError:
            raise FileNotFoundError("File is not found")
        for token in t.generate_with_types(file.read()):
            if ((token.typ=="a") or (token.typ=="d")):
                self.database.setdefault(token.word,{}).setdefault(
                    filename,[]).append(Position(token.position,
                                                 token.position+len(token))
    
    def index_with_lines(self, filename):
        try:
            file = open(filename)       
        except IOError:
            raise FileNotFoundError("File is not found")
        for line, string in enumerate(file.read()):
            for token in t.generate_with_types(string):
                if ((token.typ=="a") or (token.typ=="d")):
                    self.database.setdefault(token.word,{}).setdefault(
                        filename,[]).append(Position_with_lines(
                            token.position, token.position+len(token),line)

    def closeDatabase(self):
        self.database = shelve.sync()
        
def main():
    indexer = Indexer('database')
    file = open('text.txt', 'w')
    file.write('this is a sentence to be be indexed')
    file.close()
    indexer.index('text.txt')
    indexer.closeDatabase()
    os.remove('text.txt')
    file2 = open('text2.txt', 'w')
    file2.write('this is a sentence \r\nto be be indexed')
    file2.close()
    indexer.index('text2.txt')
    indexer.closeDatabase()
    os.remove('text2.txt')
    print(dict(indexer.database))
    
if __name__=='__main__':
    main()
