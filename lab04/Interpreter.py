from lab04 import AST
import lab04.SymbolTable
from lab04.Memory import *
from lab04.Exceptions import  *
from lab04.visit import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):

    def __init__(self):
        self.globalMemory = MemoryStack(Memory("Global Memory"))
        self.functionMemory = MemoryStack(Memory("Function Memory"))

    @on('node')
    def visit(self, node):
        pass


    # TODO implement visit methods for all classes from AST


    @when(AST.Program)
    def visit(self, node):
        node.components.accept(self)



    @when(AST.BinOp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.RelOp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # ...

    @when(AST.Assignment)
    def visit(self, node):
    #
    #

    @when(AST.Const)
    def visit(self, node):
        return node.value

    # simplistic while loop interpretation
    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r


