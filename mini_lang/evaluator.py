"""
MiniLang Evaluator
Walks the AST and executes the program.
"""

from mini_lang.ast_nodes import (
    ProgramNode,
    NumberNode,
    VarNode,
    UnaryOpNode,
    BinOpNode,
    LetNode,
    IfNode,
)
from mini_lang.errors import RuntimeError


class Evaluator:
    def __init__(self):
        self.env = {}

    def visit(self, node):

        # Program
        if isinstance(node, ProgramNode):
            result = None

            for statement in node.statements:
                result = self.visit(statement)

            return result

        # Number
        if isinstance(node, NumberNode):
            return node.value

        # Variable
        if isinstance(node, VarNode):

            if node.name not in self.env:
                raise RuntimeError(
                    f"Undefined variable '{node.name}'"
                )

            return self.env[node.name]

        # Unary operator
        if isinstance(node, UnaryOpNode):

            value = self.visit(node.expr)

            if node.op == "-":
                return -value

            raise RuntimeError(
                f"Unknown unary operator '{node.op}'"
            )

        # Binary operator
        if isinstance(node, BinOpNode):

            left = self.visit(node.left)
            right = self.visit(node.right)

            # Arithmetic
            if node.op == "+":
                return left + right

            if node.op == "-":
                return left - right

            if node.op == "*":
                return left * right

            if node.op == "/":

                if right == 0:
                    raise RuntimeError("Division by zero")

                return left / right

            # Comparison
            if node.op == "==":
                return left == right

            if node.op == "!=":
                return left != right

            if node.op == ">":
                return left > right

            if node.op == "<":
                return left < right

            if node.op == ">=":
                return left >= right

            if node.op == "<=":
                return left <= right

            raise RuntimeError(
                f"Unknown operator '{node.op}'"
            )
        
        # IF statement
        if isinstance(node, IfNode):

            condition = self.visit(node.condition)

            if condition:
                return self.visit(node.then_branch)

            if node.else_branch is not None:
                return self.visit(node.else_branch)

            return None

        # LET statement
        if isinstance(node, LetNode):

            value = self.visit(node.value)

            self.env[node.name] = value

            return value

        raise RuntimeError(
            f"Unknown AST node: {type(node).__name__}"
        )