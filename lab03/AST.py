class Node(object):
    def __str__(self):
        return self.printTree()


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
    def __init__(self, label, instruction):
        self.label = label
        self.instruction = instruction


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


class WhileInstruction(Node):
    def __init__(self, condition, instr):
        self.condition = condition
        self.instruction = instr


class RepeatInstruction(Node):
    def __init__(self, instructions, condition):
        self.condition = condition
        self.instructions = instructions


class ReturnInstruction(Node):
    def __init__(self, expression, lineno):
        self.expression = expression
        self.lineno = lineno


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
    def __init__(self, identifier):
        self.identifier = identifier


class FunctionDefinition(Node):
    def __init__(self, return_type, function_name, arguments, compound_instr, lineno):
        self.return_type = return_type
        self.function_name = function_name
        self.arguments = arguments
        self.compound_instr = compound_instr
        self.lineno = lineno


class FunctionArgument(Node):
    def __init__(self, argument_type, argument):
        self.argument_type = argument_type
        self.argument = argument


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


class CompoundInstruction(Node):
    def __init__(self, instructions, end_lineno):
        self.instructions = instructions
        self.children = instructions
        self.end_lineno = end_lineno

