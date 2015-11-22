#!/usr/bin/python


class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        super(VariableSymbol, self).__init__(name, type)


class FunctionSymbol(Symbol):
    def __init__(self, name, type):
        super(FunctionSymbol, self).__init__(name, type)
        self.arguments = []

    def add_argument(self, arg):
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

    def has_label(self, name):
        if name in self.labels:
            return True
        if self.name.startswith("function") or self.parent is None:
            return False
        return self.parent.has_label(name)

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

    def get_scope_type(self, scope_type):
        if self.name == scope_type:
            return self
        else:
            if self.parent is not None:
                return self.parent.get_scope_type(scope_type)
            else:
                return None

    def get_function_scope(self):
        return self.get_scope_type("function-scope")

    def get_loop_scope(self):
        return self.get_scope_type("loop-scope")


