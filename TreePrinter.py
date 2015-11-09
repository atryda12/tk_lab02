import AST


def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Declaration)
    def printTree(self):
        pass

    @addToClass(AST.Initialisation)
    def printTree(self):
        pass

    @addToClass(AST.LabeledInstruction)
    def printTree(self):
        pass

    @addToClass(AST.ChoiceInstruction)
    def printTree(self):
        pass

    @addToClass(AST.WhileInstruction)
    def printTree(self):
        pass

    @addToClass(AST.RepeatInstruction)
    def printTree(self):
        pass

    @addToClass(AST.BinExpr)
    def printTree(self):
        pass

    @addToClass(AST.FunctionCall)
    def printTree(self):
        pass

    @addToClass(AST.FunctionDefinition)
    def printTree(self):
        pass

    @addToClass(AST.FunctionArgument)
    def printTree(self):
        pass
