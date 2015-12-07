import sys
import ply.yacc as yacc
from lab04.Cparser import Cparser
# required for printing to work
from lab04.TreePrinter import TreePrinter
from lab04.TypeChecker import TypeChecker
from lab04.Interpreter import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()

    ast = parser.parse(text, lexer=Cparser.scanner)
    #print(str(ast))
    typeChecker = TypeChecker()
    typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)

    ast.accept(Interpreter())
