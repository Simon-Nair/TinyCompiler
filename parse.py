import sys
from lex import *

# Parser objects keep track of current token and check if the code matches the grammer.
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

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

        # skip newlines at start of file
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # Parse all statements in the program
        while not self.checkToken(TokenType.EOF):
            self.statement()

    def statement(self):
        # Check first token to see what kind of statement this is

        # "PRINT" (expression | string)
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                # simple string
                self.nextToken()
            else:
                # expression
                self.expression()

        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            # Zero or more statements in the body
            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            
            self.match(TokenType.ENDIF)

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            # Zero or more statemnts in the loop body
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
            
            self.match(TokenType.ENDWHILE)

        # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()
            self.match(TokenType.IDENT)
        
        # "GOTO" IDENT
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.match(TokenType.IDENT)
        
        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            print("STATEMENT-LET")
            self.nextToken()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()
            self.match(TokenType.IDENT)

        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        # Newline
        self.nl()

    # nl ::= '\n'+
    def nl(self):
        print("NEWLINE")

        # require at least one newline
        self.match(TokenType.NEWLINE)
        # also allow extra newlines
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
        
    # Comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)
    def comparison(self):
        print("COMPARISON")

        self.expression()
        # Must be at least one comparison operator and another expression
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparissonn operator at: " + self.curToken.text)

        # Can have 0 or more comparison operators and expressions
        while self.isComparisonOperator():
            self.nextToken()
            self.expression()
    
    # return true if current token is a comparison operator
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)
    
    # Expression ::= ter {( "-" | "+" ) term}
    def expression(self):
        print("EXPRESSION")

        self.term()
        # can have 0 or more +/- and expressions
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    # term ::= unary {( "/" | "*") unary}
    def term(self):
        print("TERM")

        self.unary()
        # can have 0 or more //* and terms
        while self.checkToken(TokenType.SLASH) or self.checkToken(TokenType.ASTERISK):
            self.nextToken()
            self.unary()

    # unary ::= ["+" | "-"] primary
    def unary(self):    
        print("UNARY")

        # optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    # primary ::= number | ident
    def primary(self):
        print("PRIMARY (" + self.curToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            self.nextToken()
        else:
            # Error
            self.abort("Unexpected token at " + self.checkToken.text)
 
