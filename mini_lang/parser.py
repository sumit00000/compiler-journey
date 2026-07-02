"""
MiniLang Parser
Builds an Abstract Syntax Tree (AST) from a stream of tokens.
"""

from mini_lang.token import TokenType
from mini_lang.ast_nodes import (
    ProgramNode,
    NumberNode,
    VarNode,
    UnaryOpNode,
    BinOpNode,
    LetNode,
    IfNode,
)
from mini_lang.errors import ParserError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def eat(self, token_type):
        token = self.current()

        if token.type != token_type:
            raise ParserError(
                f"Expected {token_type.name}, got {token.type.name}"
            )

        self.advance()
        return token

    def parse(self):
        """
        program -> statement (';' statement)* EOF
        """
        statements = []

        while self.current().type != TokenType.EOF:

            statements.append(self.statement())

            if self.current().type == TokenType.SEMICOLON:
                self.advance()

        return ProgramNode(statements)

    def statement(self):
        """
        statement ->
            LET IDENT = comparison
            | IF comparison THEN statement (ELSE statement)? END
            | comparison
        """

        # LET statement
        if self.current().type == TokenType.LET:

            self.advance()

            name = self.eat(TokenType.IDENT).value

            self.eat(TokenType.EQUAL)

            value = self.comparison()

            return LetNode(name, value)

        # IF statement
        if self.current().type == TokenType.IF:
            return self.if_statement()

        return self.comparison()
    
    def if_statement(self):
        self.eat(TokenType.IF)

        condition = self.comparison()

        self.eat(TokenType.THEN)

        then_branch = self.statement()

        if self.current().type == TokenType.SEMICOLON:
            self.advance()

        else_branch = None

        if self.current().type == TokenType.ELSE:
            self.advance()

            else_branch = self.statement()

            if self.current().type == TokenType.SEMICOLON:
                self.advance()

        self.eat(TokenType.END)

        return IfNode(condition, then_branch, else_branch)

    def comparison(self):
        """
        comparison -> expression
                   ((== | != | > | < | >= | <=) expression)*
        """

        node = self.expression()

        while self.current().type in (
            TokenType.EQ,
            TokenType.NE,
            TokenType.GT,
            TokenType.LT,
            TokenType.GTE,
            TokenType.LTE,
        ):

            op = self.current().value

            self.advance()

            right = self.expression()

            node = BinOpNode(node, op, right)

        return node

    def expression(self):
        """
        expression -> term ((+|-) term)*
        """

        node = self.term()

        while self.current().type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):

            op = self.current().value

            self.advance()

            right = self.term()

            node = BinOpNode(node, op, right)

        return node

    def term(self):
        """
        term -> factor ((*|/) factor)*
        """

        node = self.factor()

        while self.current().type in (
            TokenType.STAR,
            TokenType.SLASH,
        ):

            op = self.current().value

            self.advance()

            right = self.factor()

            node = BinOpNode(node, op, right)

        return node

    def factor(self):
        """
        factor -> NUMBER
               | IDENT
               | -factor
               | (comparison)
        """

        token = self.current()

        # Unary minus
        if token.type == TokenType.MINUS:
            self.advance()
            return UnaryOpNode("-", self.factor())

        # Number
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(int(token.value))

        # Variable
        if token.type == TokenType.IDENT:
            self.advance()
            return VarNode(token.value)

        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()

            node = self.comparison()

            self.eat(TokenType.RPAREN)

            return node

        raise ParserError(
            f"Unexpected token: {token}"
        )