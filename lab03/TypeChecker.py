#!/usr/bin/python
from collections import defaultdict
import lab03.AST as AST
from lab03.SymbolTable import SymbolTable, FunctionSymbol, VariableSymbol

additional_operators = ['%']
arithmetic_operators = ['+', '-', '*', '/']
relation_operators = ['<', '<=', '>', '>=', '==', '!=']
binary_operators = ['||', '&&', '|', '^', '&', '<<', '>>']
ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for operator in additional_operators + arithmetic_operators + relation_operators + binary_operators:
    ttype[operator]['int']['int'] = 'int'

for operator in arithmetic_operators:
    ttype[operator]['float']['float'] = 'float'
    ttype[operator]['float']['int'] = 'float'
    ttype[operator]['int']['float'] = 'float'

for operator in relation_operators:
    ttype[operator]['string']['string'] = 'int'
    ttype[operator]['float']['float'] = 'int'
    ttype[operator]['float']['int'] = 'int'
    ttype[operator]['int']['float'] = 'int'

ttype['=']['string']['string'] = 'string'
ttype['=']['int']['int'] = 'int'
ttype['=']['float']['float'] = 'float'
ttype['=']['int']['float'] = 'int'
ttype['=']['float']['int'] = 'float'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):
    def log_error(self, message, lineno):
        print("Error: {}: line {}".format(message, lineno))

    def log_precision_loss_if_needed(self, type1, type2, lineno):
        if type1 == 'int' and type2 == 'float':
            print("Warning: possible percision loss: assigning float to int: line {}".format(lineno))

    def __init__(self):
        self.symbol_table = SymbolTable(None, "global-scope")
        self.current_type = None

    def visit_Declaration(self, node):
        self.current_type = node.type_name
        self.visit(node.initialisations)
        self.current_type = None

    def visit_Initialisation(self, node):
        initialisation_type = self.visit(node.expression)
        definition = self.symbol_table.searchInScopes(node.name)
        variable_name = node.name.identifier
        if definition is not None and isinstance(definition, FunctionSymbol):
            message = "Function identifier '{}' used as variable".format(variable_name)
            self.log_error(message, node.lineno)
        elif self.symbol_table.get(variable_name):
            message = "Redefinition of variable '{}'".format(variable_name)
            self.log_error(message, node.lineno)
        elif ttype['='][self.current_type][initialisation_type] is None:
            message = "Invalid definition of variable '{}': Expected: '{}', got: '{}'"\
                .format(variable_name, self.current_type, initialisation_type)
            self.log_error(message, node.lineno)
        else:
            self.log_precision_loss_if_needed(self.current_type, initialisation_type, node.lineno)
            self.symbol_table.put(variable_name, VariableSymbol(node.name, self.current_type))

    def visit_JustID(self, node):
        pass



    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op;
        # ... 
        #

    def visit_RelExpr(self, node):
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        # ... 
        #

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return "string"

