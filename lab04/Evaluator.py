class Evaluator:
    
    def __init__(self):
        self.expressions = dict()
        self.expressions['+'] = lambda x, y: x + y
        self.expressions['-'] = lambda x, y: x - y
        self.expressions['*'] = lambda x, y: x * y
        self.expressions['/'] = lambda x, y: x / y
        self.expressions['%'] = lambda x, y: x % y
        self.expressions['<'] = lambda x, y: x < y
        self.expressions['<='] = lambda x, y: x <= y
        self.expressions['>'] = lambda x, y: x > y
        self.expressions['>='] = lambda x, y: x >= y
        self.expressions['=='] = lambda x, y: x == y
        self.expressions['!='] = lambda x, y: x != y
        self.expressions['||'] = lambda x, y: x or y
        self.expressions['&&'] = lambda x, y: x and y
        self.expressions['|'] = lambda x, y: x | y
        self.expressions['^'] = lambda x, y: x ^ y
        self.expressions['&'] = lambda x, y: x & y
        self.expressions['<<'] = lambda x, y: x << y
        self.expressions['>>'] = lambda x, y: x >> y
    
    def __call__(self, op, arg1, arg2):
        return self.expressions[op](arg1, arg2)
