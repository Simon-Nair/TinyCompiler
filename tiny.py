from lex import * 
from parse import *
import sys

def main():
    print("Tiny Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()
    
    # Init lexer and parser
    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program() # start the parser
    print("Parsing Complete")

main()