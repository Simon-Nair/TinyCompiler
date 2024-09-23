import enum
import sys

class Lexer:
    def __init__(self, source):
        self.source = source + '\n' # source code to lex as a string. append newline to simplify lexing/parsing the last token/statement
        self.curChar = '' # current character in the string
        self.curPos = -1 # current posititon in the string
        self.nextChar()

    # Process the next character
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0' # end of file
        else: 
            self.curChar = self.source[self.curPos]

    # Return the lookahead character
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.curPos + 1]


    # Invalid token found, print error message and exit
    def abort(self, message):
        sys.exit("Lexing error. " + message)

    # Skip whitespace except newlines, which we will use to indicate end of statement
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    # Skip comments in the code
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # Return the next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None
        # Check the first character of this token to see if we can decide what it is
        # If it is a multiple character operator (!=), number, identifier, or keyword then process the rest
        # operators
        if self.curChar == '+':  # plus token
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':  # minus token
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':  # asterisk token
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':  # slash token 
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '=':  # check if = or ==
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '<':  # check if < or <=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '>':  # check if > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '!':  # != or error
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        # special chars
        elif self.curChar == '\n':  # newline token 
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':  # EOF token
            token = Token('', TokenType.EOF)
        # stings
        elif self.curChar == '\"':
            # get chars between quotes
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # wont allow special chars in the string no escape, newlines, tabs, or %
                # for ease when use C's printf on the string
                if self.curChar == '\r' or self.curChar == "\n" or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()
            
            tokText = self.source[startPos : self.curPos] # get the substring
            token = Token(tokText, TokenType.STRING)
        # numbers
        elif self.curChar.isdigit():
            # leading char is a digit, so this must be a number
            # get all consecutive digits and decimal if one exists
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.': # if decimal
                self.nextChar()

                # must have at least one digit after decimal
                if not self.peek().isdigit():
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()
            
            tokText = self.source[startPos : self.curPos + 1] # get substring
            token = Token(tokText, TokenType.NUMBER)
        # identifiers and keywords
        elif self.curChar.isalpha():
            # leading char is a letter so must be identifier or keyword
            # get all consecutive alpha numeric chars
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            
            # check if token is in the list of keywords
            tokText = self.source[startPos : self.curPos + 1] # get substring
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None: # identifier
                token = Token(tokText, TokenType.IDENT)
            else: # keyword
                token = Token(tokText, keyword)
        # Unknown token
        else:
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token


# Token contains the original text and the type of token
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText # the token's actual text, used for identifiers, numbers, and strings
        self.kind = tokenKind # The type of token this toke is classified as

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # relies on all keyword enum values being 1XX
            if kind.name == tokenText and kind.value >= 100 and kind.value <200:
                return kind
        return None


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2  # identifier
    STRING = 3
    # keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    #operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206 
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211