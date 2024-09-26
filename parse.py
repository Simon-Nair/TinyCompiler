import sys
from lex import *

# Parser objects keep track of current token and check if the code matches the grammer.
class Parser:
    def __init__(self, lexer):
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()  # call twice to init current and peek

    # Return true if the current token matches
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # Return true if the next token matches
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # Try to match current token. If not, error. Advances the current token
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    # Advances the current token
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # lexer handles passing EOF

    def abort(self, message):
        sys.exit("Error. " + message)

    # Production Rules

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # Parse all statements in the program
        while not self.checkToken(TokenType.EOF):
            self.statement()

    def statement(self):
        # Check first token to see what kind of statement this is

        # "PRINT" (expression | string)
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

        
 
