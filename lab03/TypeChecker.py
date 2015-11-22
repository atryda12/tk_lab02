#!/usr/bin/python
from collections import defaultdict
from itertools import chain
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

    def enter_scope(self, new_scope_name):
        self.symbol_table = SymbolTable(self.symbol_table, new_scope_name)

    def leave_scope(self):
        self.symbol_table = self.symbol_table.getParentScope()

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
        if definition is not None and isinstance(definition, FunctionSymbol):
            message = "Function identifier '{}' used as variable".format(node.name)
            self.log_error(message, node.lineno)
        elif self.symbol_table.get(node.name):
            message = "Variable '{}' already declared".format(node.name)
            self.log_error(message, node.lineno)
        elif ttype['='][self.current_type][initialisation_type] is None:
            message = "Assignment of {} to {}".format(initialisation_type, self.current_type)
            self.log_error(message, node.lineno)
        else:
            self.log_precision_loss_if_needed(self.current_type, initialisation_type, node.lineno)
            self.symbol_table.put(node.name, VariableSymbol(node.name, self.current_type))

    def visit_JustID(self, node):
        id_type = self.symbol_table.searchInScopes(node.identifier)
        if id_type is None:
            message = "Usage of undeclared variable '{}'".format(node.identifier)
            self.log_error(message, node.lineno)
            return None
        return id_type.type

    def visit_LabeledInstruction(self, node):
        if self.symbol_table.has_label(node.label):
            message = "Label '{}' already in use in this scope ".format(node.label)
            self.log_error(message, node.lineno)
        else:
            self.symbol_table.putLabel(node.label)
        self.visit(node.instruction)

    def visit_Assignment(self, node):
        expression_type = self.visit(node.expression)
        variable_definition = self.symbol_table.searchInScopes(node.name)
        if expression_type is not None:
            if variable_definition is None:
                message = "Variable '{}' undefined in current scope".format(node.name)
                self.log_error(message, node.lineno)
            elif ttype['='][variable_definition.type][expression_type] is None:
                message = "Assignment of {} to {}".format(expression_type, variable_definition.type)
                self.log_error(message, node.lineno)
            else:
                self.log_precision_loss_if_needed(variable_definition.type, expression_type, node.lineno)

    def visit_ChoiceInstruction(self, node):
        self.visit(node.condition)
        self.visit(node.if_instruction)
        if node.else_instruction is not None:
            self.visit(node.else_instruction)

    def visit_RepeatInstruction(self, node):
        self.enter_scope("loop-scope")
        self.visit(node.instructions)
        self.leave_scope()
        self.visit(node.condition)

    def visit_WhileInstruction(self, node):
        self.visit(node.condition)
        self.enter_scope("loop-scope")
        self.visit(node.instruction)
        self.leave_scope()

    def visit_ReturnInstruction(self, node):
        function_scope = self.symbol_table.get_function_scope()
        if function_scope is None:
            self.log_error("return instruction outside a function", node.lineno)
        else:
            function_type = function_scope.function_symbol.type
            return_type = self.visit(node.expression)
            if return_type is not None:
                if ttype['='][function_type][return_type] is None:
                    message = "Improper returned type, expected {}, got {}".format(function_type, return_type)
                    self.log_error(message, node.lineno)
                else:
                    self.log_precision_loss_if_needed(function_type, return_type, node.lineno)

    def visit_loop_instruction(self, instruction, lineno):
        if self.symbol_table.get_loop_scope() is None:
            message = "{} instruction outside a loop".format(instruction)
            self.log_error(message, lineno)

    def visit_ContinueInstruction(self, node):
        self.visit_loop_instruction("continue", node.lineno)

    def visit_BreakInstruction(self, node):
        self.visit_loop_instruction("break", node.lineno)

    def visit_BinExpr(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        return_type = ttype[node.op][left_type][right_type]
        if return_type is None:
            message = "Illegal operation, {} {} {}".format(left_type, node.op, right_type)
            self.log_error(message, node.lineno)
        return return_type


    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return "string"

    def visit_FunctionDefinition(self, node):
        symbol = self.symbol_table.searchInScopes(node.function_name)
        if isinstance(symbol, FunctionSymbol):
            message = "Redefinition  of function '{}'".format(node.function_name)
            self.log_error(message, node.lineno)
        elif isinstance(symbol, VariableSymbol):
            message = "Variable identifier '{}' used as function name".format(node.function_name)
            self.log_error(message, node.lineno)
        else:
            return_instructions = node.compound_instr.flatten()
            if not return_instructions:
                self.log_error("Missing return statement", node.compound_instr.end_lineno)
            function_symbol = FunctionSymbol(node.function_name, node.return_type)
            self.symbol_table.put(node.function_name, function_symbol)
            self.enter_scope("function-scope")
            self.symbol_table.function_symbol = function_symbol

            self.visit(node.arguments)
            self.visit(node.compound_instr)

            self.leave_scope()

    def visit_FunctionArgument(self, node):
        if self.symbol_table.searchInCurrentScope(node.argument) is not None:
            self.log_error("Redefinition of an argument {0}.".format(node.argument), node.lineno)
        else:
            self.symbol_table.put(node.argument, VariableSymbol(node.argument, node.argument_type))
            self.symbol_table.function_symbol.add_argument(node.argument_type)

    def visit_FunctionCall(self, node):
        pass


