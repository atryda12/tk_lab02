import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def shift(expression):
# TODO zjebalem wprost od Grochala, mozemy chociaz zmienic nazwe :P
    output_string = ""
    for line in expression.split('\n'):
        output_string += "" if len(line) == 0 else "| " + line + '\n'
    return output_string


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Declaration)
    def printTree(self):
        return "DECL\n" + self.initialisations

    @addToClass(AST.Initialisation)
    def printTree(self):
        output_string = "| =\n| | " + self.name + '\n'
        for line in self.expression.split('\n'):
            output_string += "" if len(line) == 0 else "| | " + line + '\n'
        return output_string

    @addToClass(AST.PrintInstruction)
    def printTree(self):
        output_string = "PRINT\n"
        output_string += shift(self.expressions)
        return output_string

    @addToClass(AST.LabeledInstruction)
    def printTree(self):
        output_string = "LABEL\n| " + self.label + "\n"
        output_string += shift(self.instruction)
        return output_string

    @addToClass(AST.Assignment)
    def printTree(self):
        output_string = "=\n| " + self.variable_name + '\n'
        output_string += shift(self.expression)
        return output_string
    
    @addToClass(AST.ChoiceInstruction)
    def printTree(self):
        # TODO ...
        pass

    @addToClass(AST.WhileInstruction)
    def printTree(self):
        output_string = "WHILE\n"
        output_string += shift(self.condition)
        output_string += shift(self.instruction)
        return output_string

    @addToClass(AST.RepeatInstruction)
    def printTree(self):
        # TODO ...
        pass
    
    @addToClass(AST.ReturnInstruction)
    def printTree(self):
        output_string = "RETURN\n"
        output_string += shift(self.expression)
        return output_string


    @addToClass(AST.BinExpr)
    def printTree(self):
        output_string = self.op + '\n'
        output_string += shift(self.left)
        output_string += shift(self.right)
        return output_string
    
    @addToClass(AST.FunctionCall)
    def printTree(self):
            output_string = "FUNCALL\n| " + self.function_name + "\n"
            output_string += shift(self.arguments)
            return output_string

    @addToClass(AST.FunctionDefinition)
    def printTree(self):
        output_string ="FUNDEF\n| " + self.function_name + "\n| RET " \
                       + self.return_type + "\n" + self.arguments
        output_string += shift(self.compound_instr)
        return output_string

    @addToClass(AST.FunctionArgument)
    def printTree(self):
        return "| ARG " + self.argument_type + " " + self.argument + "\n"
