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
        self.functionMemory = MemoryStack()
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
        memory = self.determine_memory_scope()
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
        memory = self.determine_memory_scope()
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
                    # memory.pop()
                    continue
                except BreakException:
                    memory.pop()
                    break
                except ReturnValueException as e:
                    memory.pop()
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

    @when(AST.FunctionCall)
    def visit(self, node):
        # TODO stack overflow when too many recursive calls

        function_name = node.function_name
        new_memory = Memory("function_" + function_name + "_memory_scope")

        function_definition = self.globalMemory.get(function_name)

        for i in range(0, len(node.arguments)):
            accepted_def_arg = function_definition.arguments[i].accept(self)
            accepted_call_arg = node.arguments[i].accept(self)
            type = accepted_def_arg['arg_type']
            name = accepted_def_arg['arg_name']
            new_memory.put(name, self.cast(type, accepted_call_arg))

        self.inFunctionScope = True
        self.functionMemory.push(new_memory)

        try:
            return_val = function_definition.compound_instr.accept(self)
        except ReturnValueException as e:
            self.functionMemory.pop()
            if len(self.functionMemory.memoryStack) == 0:
                self.inFunctionScope = False
            return self.cast(function_definition.return_type, e.value)

        self.functionMemory.pop()
        if len(self.functionMemory.memoryStack) == 0:
            self.inFunctionScope = False
        return return_val

    @when(AST.JustID)
    def visit(self, node):
        if self.inFunctionScope:
            return self.functionMemory.get(node.identifier)
        else:
            return self.globalMemory.get(node.identifier)

    @when(AST.FunctionDefinition)
    def visit(self, node):
        self.globalMemory.insert(node.function_name, node)

    @when(AST.FunctionArgument)
    def visit(self, node):
        return {'arg_name': node.argument, 'arg_type': node.argument_type}

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
            try:
                instruction.accept(self)
            except BreakException as e:
                memory.pop()
                raise e
            except ContinueException as e:
                memory.pop()
                raise e
            except ReturnValueException as e:
                memory.pop()
                raise e

        memory.pop()

    def determine_memory_scope(self):
        return self.functionMemory if self.inFunctionScope else self.globalMemory

    def cast(self, type_str, val):
        if type_str == "int":
            return int(val)
        elif type_str == "float":
            return float(val)
        else:
            return str(val)