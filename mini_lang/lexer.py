"""
MiniLang Lexer
Converts source code into a stream of tokens.
"""

from mini_lang.token import Token, TokenType
from mini_lang.errors import LexerError


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def current_char(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def advance(self):
        self.pos += 1

    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char().isspace():
            self.advance()

    def read_number(self):
        start = self.pos

        while (
            self.current_char() is not None
            and self.current_char().isdigit()
        ):
            self.advance()

        return self.text[start:self.pos]

    def read_identifier(self):
        start = self.pos

        while (
            self.current_char() is not None
            and (
                self.current_char().isalnum()
                or self.current_char() == "_"
            )
        ):
            self.advance()

        return self.text[start:self.pos]

    def tokenize(self):
        tokens = []

        while self.current_char() is not None:

            ch = self.current_char()

            if ch.isspace():
                self.skip_whitespace()
                continue

            if ch.isdigit():
                tokens.append(
                    Token(
                        TokenType.NUMBER,
                        self.read_number(),
                    )
                )
                continue

            if ch.isalpha() or ch == "_":

                ident = self.read_identifier()

                if ident.upper() == "LET":
                    tokens.append(Token(TokenType.LET, ident))
                else:
                    tokens.append(Token(TokenType.IDENT, ident))

                continue

            if ch == "+":
                tokens.append(Token(TokenType.PLUS, ch))
                self.advance()
                continue

            if ch == "-":
                tokens.append(Token(TokenType.MINUS, ch))
                self.advance()
                continue

            if ch == "*":
                tokens.append(Token(TokenType.STAR, ch))
                self.advance()
                continue

            if ch == "/":
                tokens.append(Token(TokenType.SLASH, ch))
                self.advance()
                continue

            if ch == "=":
                tokens.append(Token(TokenType.EQUAL, ch))
                self.advance()
                continue

            if ch == "(":
                tokens.append(Token(TokenType.LPAREN, ch))
                self.advance()
                continue

            if ch == ")":
                tokens.append(Token(TokenType.RPAREN, ch))
                self.advance()
                continue

            if ch == ";":
                tokens.append(Token(TokenType.SEMICOLON, ch))
                self.advance()
                continue

            raise LexerError(f"Unexpected character: {ch}")

        tokens.append(Token(TokenType.EOF, ""))

        return tokens