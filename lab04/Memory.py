class Memory:

    def __init__(self, name):  # variables name
        self.name = name
        self.variables = dict()

    def has_key(self, name):  # variable name
        return name in self.variables

    def get(self, name):         # gets from variables current value of variable <name>
        return self.variables[name]

    def put(self, name, value):  # puts into variables current value of variable <name>
        self.variables[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.memoryStack = list()
        if memory is not None:
            self.push(memory)

    def get(self, name):         # gets from memory stack current value of variable <name>
        return self.memoryStack[-1].get(name)

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.memoryStack[-1].put(name, value)

    def set(self, name, value):     # sets variable <name> to value <value>
        if self.memoryStack[-1].has_key(name):
            self.memoryStack[-1].put(name, value)

    def push(self, memory):     # pushes memory <memory> onto the stack
        self.memoryStack.append(memory)

    def pop(self):              # pops the top memory from the stack
        return self.memoryStack.pop()

