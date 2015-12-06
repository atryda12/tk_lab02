class Node(object):
    # def __str__(self):
    #     return self.printTree()

    def flatten(self):
        return []

    def accept(self, visitor):
        return visitor.visit(self)


class Program(Node):
    def __init__(self, components):
        self.components = components
        self.children = components


class Declaration(Node):
    def __init__(self, type_name, initialisations):
        self.type_name = type_name
        self.initialisations = initialisations


class Initialisation(Node):
    def __init__(self, name, expression, lineno):
        self.name = name
        self.expression = expression
        self.lineno = lineno


class PrintInstruction(Node):
    def __init__(self, expressions):
        self.expressions = expressions
        self.children = [expressions]


class LabeledInstruction(Node):
    def __init__(self, label, instruction, lineno):
        self.label = label
        self.instruction = instruction
        self.lineno = lineno

    def flatten(self):
        return self.instruction.flatten()


class Assignment(Node):
    def __init__(self, name, expression, lineno):
        self.name = name
        self.expression = expression
        self.lineno = lineno


class ChoiceInstruction(Node):
    def __init__(self, condition, if_instr, else_instr=None):
        self.condition = condition
        self.if_instruction = if_instr
        self.else_instruction = else_instr

    def flatten(self):
        if_flattened = self.if_instruction.flatten()
        else_flattened = self.else_instruction.flatten() if self.else_instruction else None
        if isinstance(if_flattened, list) and isinstance(else_flattened, list):
            return if_flattened + else_flattened
        if isinstance(if_flattened, list):
            if_flattened.append(else_flattened)
            return if_flattened
        return [if_flattened, else_flattened]


class WhileInstruction(Node):
    def __init__(self, condition, instr):
        self.condition = condition
        self.instruction = instr
        self.children = instr

    def flatten(self):
        return self.instruction.flatten()


class RepeatInstruction(Node):
    def __init__(self, instructions, condition):
        self.condition = condition
        self.instructions = instructions

    def flatten(self):
        return [i.flatten for i in self.instructions]


class ReturnInstruction(Node):
    def __init__(self, expression, lineno):
        self.expression = expression
        self.lineno = lineno

    def flatten(self):
        return [self]


class ContinueInstruction(Node):
    def __init__(self, lineno):
        self.lineno = lineno


class BreakInstruction(Node):
    def __init__(self, lineno):
        self.lineno = lineno


class BinExpr(Node):
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno


class FunctionCall(Node):
    def __init__(self, function_name, arguments, lineno):
        self.function_name = function_name
        self.arguments = arguments
        self.lineno = lineno


class JustID(Node):
    def __init__(self, identifier, lineno):
        self.identifier = identifier
        self.lineno = lineno


class FunctionDefinition(Node):
    def __init__(self, return_type, function_name, arguments, compound_instr, lineno):
        self.return_type = return_type
        self.function_name = function_name
        self.arguments = arguments
        self.compound_instr = compound_instr
        self.lineno = lineno


class FunctionArgument(Node):
    def __init__(self, argument_type, argument, lineno):
        self.argument_type = argument_type
        self.argument = argument
        self.lineno = lineno


class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    def __init__(self, value):
        super(Integer, self).__init__(value)


class Float(Const):
    def __init__(self, value):
        super(Float, self).__init__(value)


class String(Const):
    def __init__(self, value):
        super(String, self).__init__(value)


def flatten(item):
    if not isinstance(item, list):
        return [item]
    flattened = []
    for x in item:
        if x:
            for y in flatten(x):
                flattened.append(y)
    return flattened


class CompoundInstruction(Node):
    def __init__(self, instructions, end_lineno):
        self.instructions = instructions
        self.children = instructions
        self.end_lineno = end_lineno

    def flatten(self):
        nested = [i.flatten() for i in self.instructions]
        flattened = flatten(nested)
        return list(filter(lambda x: isinstance(x, ReturnInstruction), flattened))
