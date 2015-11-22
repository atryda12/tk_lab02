from lab03 import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def indent(expression):
    output_string = ""
    for line in str(expression).split('\n'):
        output_string += "" if len(line) == 0 else "| " + line + '\n'
    return output_string


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self):
        output_str = ""
        for component in self.components:
            output_str += str(component)
        return output_str

    @addToClass(AST.Declaration)
    def printTree(self):
        output_str = "DECL\n"
        for init in self.initialisations:
            output_str += str(init)
        return output_str

    @addToClass(AST.Initialisation)
    def printTree(self):
        output_string = "| =\n| | " + self.name + '\n' + "| | " + str(self.expression) + '\n'
        return output_string

    @addToClass(AST.PrintInstruction)
    def printTree(self):
        output_string = "PRINT\n"
        for expression in self.expressions:
            output_string += indent(expression)
        return output_string

    @addToClass(AST.LabeledInstruction)
    def printTree(self):
        output_string = "LABEL\n| " + self.label + "\n"
        output_string += indent(self.instruction)
        return output_string

    @addToClass(AST.Assignment)
    def printTree(self):
        output_string = "=\n| " + self.name + '\n'
        output_string += indent(self.expression)
        return output_string
    
    @addToClass(AST.ChoiceInstruction)
    def printTree(self):
        output_string = "IF\n"
        output_string += indent(self.condition)
        output_string += indent(self.if_instruction)
        if self.else_instruction:
            output_string += "ELSE\n"
            output_string += indent(self.else_instruction)
        return output_string

    @addToClass(AST.WhileInstruction)
    def printTree(self):
        output_string = "WHILE\n"
        output_string += indent(self.condition)
        output_string += indent(self.instruction)
        return output_string

    @addToClass(AST.RepeatInstruction)
    def printTree(self):
        output_string = "REPEAT\n"
        for instruction in self.instructions:
            output_string += indent(instruction)
        output_string += "UNTIL\n"
        output_string += indent(self.condition)
        return output_string
    
    @addToClass(AST.ReturnInstruction)
    def printTree(self):
        output_string = "RETURN\n"
        output_string += indent(self.expression)
        return output_string

    @addToClass(AST.ContinueInstruction)
    def printTree(self):
        output_string = "CONTINUE\n"
        return output_string

    @addToClass(AST.BreakInstruction)
    def printTree(self):
        output_string = "BREAK\n"
        return output_string

    @addToClass(AST.BinExpr)
    def printTree(self):
        output_string = self.op + '\n'
        output_string += indent(self.left)
        output_string += indent(self.right)
        return output_string
    
    @addToClass(AST.FunctionCall)
    def printTree(self):
        output_string = "FUNCALL\n| " + self.function_name + "\n"
        for argument in self.arguments:
            output_string += indent(argument)
        return output_string

    @addToClass(AST.JustID)
    def printTree(self):
        return self.identifier

    @addToClass(AST.FunctionDefinition)
    def printTree(self):
        output_string ="FUNDEF\n| " + self.function_name + "\n| RET " \
                       + self.return_type + "\n"
        for arg in self.arguments:
            output_string += str(arg)
        output_string += indent(self.compound_instr)
        return output_string

    @addToClass(AST.FunctionArgument)
    def printTree(self):
        return "| ARG " + self.argument + "\n"

    @addToClass(AST.Const)
    def printTree(self):
        return str(self.value)

    @addToClass(AST.CompoundInstruction)
    def printTree(self):
        output_str = ""
        for instr in self.instructions:
            output_str += str(instr) + "\n"
        return output_str
