"""
This module can be used for tokenization of string.
"""
from unicodedata import category


class Token (object):
    """
    Class of tokens. Instances of the class have attributes
    'position' and 'word'.
    """
    
    def __init__ (self, position, word):
        """
        This method creates an instance of the class Token with 2 attributes:
        @param position: position of the first symbol of the token in the string
        @param word: token itself
        """
        self.position = position
        self.word = word

        
class TypeToken (Token):
    """It is a Token with defined Type. Type can be alphabetic (a), digit (d),
    space (s), punctuation (p), other (o)
    """
    def __init__ (self, position, word, typ):
        self.position = position
        self.word = word
        self.typ = typ

        
class Tokenizator (object):
    """Class which has a fuction for dividing our text on tokens"""

    def generate (self, string):
        """
        Generator
        This method takes the argument of 'string' type. There is a cycle
        on all the symbols of the string. We record in the list of tokens
        only tokens that consist of alphabetic symbols, we cut these tokens
        from the string. 
        @param a: position of the first symbol of a token
        @return: list of tokens
        """
        if string == "":
            return "Empty string"
        # array for the final tokens
        a = 0
        for i, c, in enumerate (string):
            if not c.isalpha():
                # if the character previous to the current is non-alphabetical,
                # it was the end of the word and we can add this token in our list
                if string[i-1].isalpha() and i != 0:
                    yield Token(a, string[a:i])
            if c.isalpha():
                # if the first symbol of the string, we record its position in a
                # as the position of the beginning of a new token
                if i == 0:
                    a = 0
                # if our current character is alphabetical and the previous one
                # is not, we record in param a the position of the current symbol
                # as the beginning of a new one
                elif not string[i-1].isalpha() and i != 0:
                    a = i
        # if the last symbol of the string is alphabetical,
        # we need to add another token after our cycle
        # param a at this moment denotes the first symbol of the last token
        if string[-1].isalpha():
            yield Token(a, string[a:len(string)])

    def tokenize(self, string):
        """
        Previous tokenizer, now without a collection of tokens, but it can still
        return the tokens as a list with the method generate
        """
        return list(self.generate(string))
    
    def _getType (self, c):
        """
        The method identify the type of the character
        @param c: character in question
        @return: type of the character: alphabetical (a), digit (d),
        space (s), punctuation (p), other (o)
        """
        mycategory = category (c)
        if mycategory [0] == "L":
           return "a" #alphabetical
        elif mycategory [0] == "N":
           return "d" #digit
        elif mycategory [0] == "Z":
           return "s" #space or separator
        elif mycategory [0] == "P":
           return "p" #punctuation
        else: return "o" #other
        
    def generate_with_types (self, string):
        """
        This method is pretty similar to the method 'generate' (above),
        but it records also the type to each token.
        @param string: text to be divided into tokens
        @yield: TypeTokens with params: position, word and typ
        """
        if string == "":
            return "Empty string"
        lastTokenType = ""
        a = 0
        lastTokenType = self._getType(string[0])
        for i, c, in enumerate (string):
            currentTokenType = self._getType(c)
            """
            We extract token in this method only when the type of the
            previous character before the beginning of the token and
            that of the next character after the token have different
            type from the type of the characters inside the token.
            Therefore, space, digits (like 1 or 939872), punctuation
            and so on are tokens as well.
            """
            if currentTokenType != lastTokenType and i>0:
                yield TypeToken(a, string[a:i], lastTokenType)
                a = i
                lastTokenType = currentTokenType
        #This string is necessary for processing of the last token
        yield TypeToken(a, string[a:i+1], currentTokenType)
                
    def tokenize_with_types(self, string):
        """
        This method uses generator with types and records
        all TypeTokens into one list.
        @param string: string to be processed by generate_with_types method
        @return: list of TypeTokens
        """
        return list(self.generate_with_types(string))
    
    def generate_alpha_and_digits(self, string):
        for token in self.generate_with_types(string):
            if ((token.typ=="a") or (token.typ=="d")):
                yield token
        
        
text = "  // 194  This  14 program 225 can 655 cause 320//, tears  "
text2 = "12This program can cause tears"
text3 = "You can cope with everything!"
# creating an instance of class Tokenizator
t = Tokenizator()
#tokenslist = list(t.tokenize_with_types(text2))
tokenscollection = list(t.generate_alpha_and_digits(text3))
#tokenscollection = list(t.generate(""))

for token in tokenscollection:
    print(token.word, token.position, token.typ)
