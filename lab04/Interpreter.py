from lab04 import AST
import lab04.SymbolTable
from lab04.Memory import *
from lab04.Exceptions import *
from lab04.visit import *
from lab04.Evaluator import *
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.globalMemory = MemoryStack(Memory("global_memory_scope"))
        self.functionMemory = MemoryStack(Memory("function_memory_scope"))
        self.inFunctionScope = False
        self.declaredType = None
        self.evaluator = Evaluator()

    @on("node")
    def visit(self, node):
        pass

    # TODO implement visit methods for all classes from AST

    @when(AST.Program)
    def visit(self, node):
        for component in node.components:
            component.accept(self)

    @when(AST.Declaration)
    def visit(self, node):
        self.declaredType = node.type_name
        for initialisation in node.initialisations:
            initialisation.accept(self)

    @when(AST.Initialisation)
    def visit(self, node):
        variable_name = node.name
        expression_value = node.expression.accept(self)
        memory = self.functionMemory if self.inFunctionScope else self.globalMemory
        if self.declaredType == "int":
            expression_value = int(expression_value)
        elif self.declaredType == "float":
            # TODO jesli zainicjalizujemy float a = 1;
            # TODO to tworzony jest obiekt AST.Integer, a nie AST.Float
            expression_value = float(expression_value)

        memory.insert(variable_name, expression_value)
        return expression_value

    @when(AST.PrintInstruction)
    def visit(self, node):
        for expression in node.expressions:
            print(expression.accept(self))

    @when(AST.LabeledInstruction)
    def visit(self, node):
        node.instruction.accept(self)

    @when(AST.Assignment)
    def visit(self, node):
        variable_name = node.name
        expression_value = node.expression.accept(self)
        memory = self.functionMemory if self.inFunctionScope else self.globalMemory
        # casting is performed to ensure that new value matches the declared type
        expression_value = type(memory.get(variable_name))(expression_value)
        memory.set(variable_name, expression_value)

        return expression_value

    @when(AST.ChoiceInstruction)
    def visit(self, node):

        if node.condition.accept(self):
            node.if_instruction.accept(self)
        elif node.else_instruction is not None:
            node.else_instruction.accept(self)

    @when(AST.WhileInstruction)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
            except ReturnValueException as e:
                return e.value

    @when(AST.RepeatInstruction)
    def visit(self, node):

        memory = self.determine_memory_scope()
        memory.push(Memory("repeat_loop_memory_scope"))
        cond = True
        
        while cond:
            for instruction in node.instructions:
                try:
                    instruction.accept(self)
                except ContinueException:
                    continue
                except BreakException:
                    break
                except ReturnValueException as e:
                    return e.value

                if node.condition.accept(self):
                    cond = False
        memory.pop()

    @when(AST.ReturnInstruction)
    def visit(self, node):
        raise ReturnValueException(node.expression.accept(self))

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(AST.BinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        return self.evaluator(node.op, left, right)

    # TODO functioncall,

    @when(AST.JustID)
    def visit(self, node):
        if self.inFunctionScope:
            return self.functionMemory.get(node.identifier)
        else:
            return self.globalMemory.get(node.identifier)

    # TODO function definition
    # TODO function argument

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value).strip('"')

    @when(AST.CompoundInstruction)
    def visit(self, node):
        memory = self.determine_memory_scope()
        memory.push(Memory("compound_instr_memory_scope"))
        for instruction in node.instructions:
            instruction.accept(self)
        memory.pop()

    def determine_memory_scope(self):
        return self.functionMemory if self.inFunctionScope else self.globalMemory
