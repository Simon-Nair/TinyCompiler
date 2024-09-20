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
        pass

    # Skip whitespace except newlines, which we will use to indicate end of statement
    def skipWhitespace(self):
        pass

    # Skip comments in the code
    def skipComment(self):
        pass

    # Return the next token
    def getToken(self):
        pass
    