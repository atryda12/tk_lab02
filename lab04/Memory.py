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

    def get(self, name):
        """
        gets from memory stack current value of variable <name>
        if needed, it searches down the memory_stack
        """
        tmp = list()
        while not self.memoryStack[-1].has_key(name):
            tmp.append(self.memoryStack.pop())
            if self.memoryStack == []:
                return None

        value = self.memoryStack[-1].get(name)
        tmp.reverse()
        self.memoryStack.extend(tmp)

        return value

    def insert(self, name, value):
        """
        inserts into memory stack variable <name> with value <value>
        insert is always performed on current memory scope
        insert is called when initialisation is performed
        """
        self.memoryStack[-1].put(name, value)

    def set(self, name, value):
        """
        sets variable <name> to value <value>
        if variable is not defined in current scope
        it searches down the memory_stack
        set is called when assignment is performed
        """
        tmp = list()
        while not self.memoryStack[-1].has_key(name):
            tmp.append(self.memoryStack.pop())
            if self.memoryStack == []:
                return

        self.memoryStack[-1].put(name, value)
        tmp.reverse()
        self.memoryStack.extend(tmp)

    def push(self, memory):     # pushes memory <memory> onto the stack
        self.memoryStack.append(memory)

    def pop(self):              # pops the top memory from the stack
        return self.memoryStack.pop()

