class Lexer:
    def __init__(self, source):
        pass

    # Process the next character
    def nextChar(self):
        pass

    # Return the lookahead character
    def peek(self):
        pass

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
    