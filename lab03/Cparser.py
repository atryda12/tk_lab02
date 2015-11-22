#!/usr/bin/python

from lab03.scanner import Scanner
import lab03.AST as AST


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '|'),
        ("left", '^'),
        ("left", '&'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", 'SHL', 'SHR'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')"
                  .format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : components"""
        p[0] = AST.Program(p[1])

    def p_components(self, p):
        """components : components component
                      | """
        p[0] = [] if len(p) == 1 else p[1] + [p[2]]

    def p_component(self, p):
        """component    : fundef
                        | instruction_component """
        p[0] = p[1]

    def p_instruction_component(self, p):
        """instruction_component    : declaration
                        | instruction """
        p[0] = p[1]

    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        p[0] = p[1] if len(p) == 3 else AST.Declaration(p[1], p[2])

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = AST.Initialisation(p[1], p[3], p.lineno(1))

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction"""
        p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        p[0] = p[1]

    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """
        p[0] = AST.PrintInstruction(p[2])

    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = AST.LabeledInstruction(p[1], p[3], p.lineno(1))

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AST.Assignment(p[1], p[3], p.lineno(1))

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        p[0] = AST.ChoiceInstruction(*p[3::2])

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.WhileInstruction(p[3], p[5])

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = AST.RepeatInstruction(p[2], p[4])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.ReturnInstruction(p[2], p.lineno(1))

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstruction(p.lineno(1))

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstruction(p.lineno(1))

    def p_compound_instr(self, p):
        """compound_instr : '{' instruction_components '}' """
        p[0] = AST.CompoundInstruction(p[2], p.lineno(3))

    def p_intruction_components(self, p):
        """instruction_components : instruction_components instruction_component
                                   | instruction_component"""
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]

    def p_const(self, p):
        """const : float
                 | integer
                 | string"""
        p[0] = p[1]

    def p_integer(self, p):
        """integer : INTEGER"""
        p[0] = AST.Integer(p[1])


    def p_float(self, p):
        """float : FLOAT"""
        p[0] = AST.Float(p[1])


    def p_string(self, p):
        """string : STRING"""
        p[0] = AST.String(p[1])

    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        if len(p) == 5:
            p[0] = AST.FunctionCall(p[1], p[3], p.lineno(1))
        elif len(p) == 4 and p[1] == '(':
            p[0] = p[2]
        elif len(p) == 4:
            p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(2))
        else:
            p[0] = AST.JustID(p[1], p.lineno(1)) if type(p[1]) is str else p[1]

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        p[0] = [] if len(p) == 1 else p[1]

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = AST.FunctionDefinition(p[1], p[2], p[4], p[6], p.lineno(1))

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        p[0] = [] if len(p) == 1 else p[1]

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = AST.FunctionArgument(p[1], p[2], p.lineno(1))
