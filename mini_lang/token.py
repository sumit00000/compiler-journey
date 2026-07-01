"""
Token definitions for MiniLang.
"""

from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    LET = auto()

    # Literals
    NUMBER = auto()
    IDENT = auto()

    # Arithmetic operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQUAL = auto()

    # Comparison operators
    EQ = auto()       # ==
    NE = auto()       # !=
    GT = auto()       # >
    LT = auto()       # <
    GTE = auto()      # >=
    LTE = auto()      # <=

    # Parentheses
    LPAREN = auto()
    RPAREN = auto()

    # Statement separator
    SEMICOLON = auto()

    # End of input
    EOF = auto()


class Token:
    def __init__(self, token_type: TokenType, value: str):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"