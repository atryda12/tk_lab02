#!/usr/bin/python


class Node(object):

    def accept(self, visitor):
        return visitor.visit(self)

    def __init__(self):
        self.children = ()



class BinExpr(Node):

    def __init__(self, op, left, right, token):
        self.token = token
        self.op = op
        self.left = left
        self.right = right

        # definition of children field required is in each class from AST
        # if you want to use somewhere generic_visit method instead of visit_XXX in visitor
        self.children = ( left, right )
        