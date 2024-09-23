from lex import * 

def main():
    source = """
    WHILE true
    12 + 12
    n != 1
    \"sup\" 
    = 1123
    """
    lexer = Lexer(source)


    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()

main()