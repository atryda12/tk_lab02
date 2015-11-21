#!/usr/bin/python


class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        super(VariableSymbol, self).__init__(name, type)

    def accept(self, visitor):
        return visitor.visit(self)


class FunctionSymbol(Symbol):
    def __init__(self, name, type):
        super(FunctionSymbol, self).__init__(name, type)
        self.arguments = []

    def addArgument(self, arg):
        self.arguments.append(arg)


class SymbolTable(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.entry = dict()
        self.labels = list()
        self.function_symbol = None

    def put(self, name, symbol):
        self.entry[name] = symbol

    def get(self, name):
        return self.entry.get(name)

    def putLabel(self, name):
        self.labels.append(name)

    def getLabel(self, name):
        return name in self.labels

    def getParentScope(self):
        return self.parent

    def searchInCurrentScope(self, name):
        return self.entry.get(name)

    def searchInScopes(self, name):
        if self.entry.get(name) is not None:
            return self.entry.get(name)
        else:
            if self.parent is not None:
                return self.parent.searchInScopes(name)
            else:
                return None

    def searchFunctionScope(self):
        if self.name.startswith("function"):
            return self
        else:
            if self.parent is not None:
                return self.parent.searchFunctionScope()
            else:
                return None

    def searchLoopScope(self):
        if self.name.startswith("while") or self.name.startswith("repeat"):
            return self
        else:
            if self.parent is not None:
                return self.parent.searchFunctionScope()
            else:
                return None


