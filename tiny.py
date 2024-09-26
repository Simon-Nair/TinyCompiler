from lex import * 

def main():
    source = """
    WHILE varName
    12 + 12
    n != 1
    \"sup\" 
    = 1123
    \"Simon Nair\"
    1.2
    234
    """
    lexer = Lexer(source)


    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()

main()