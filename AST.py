class Node(object):
    def __str__(self):
        return self.printTree()


class Declaration(Node):
    def __init__(self, type_name, initialisations):
        self.type_name = type_name
        self.initialisations = initialisations


class Initialisation(Node):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression


class PrintInstruction(Node):
    def __init__(self, expressions):
        self.expressions = expressions


class LabeledInstruction(Node):
    def __init__(self, label, instruction):
        self.label = label
        self.instruction = instruction


class Assignment(Node):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression


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
    def __init__(self, expression):
        self.expression = expression







class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Const(Node):
    pass
    #...

class Integer(Const):
    pass
    #...


class Float(Const):
    pass
    #...


class String(Const):
    pass
    #...


class Variable(Node):
    pass
    #...




# ...


