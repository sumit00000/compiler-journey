# simple token class
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


# lexer
# reads input one char at a time
class Lexer:
    def __init__(self, text):
        self.text = text
        self.i = 0

    def current_char(self):
        if self.i >= len(self.text):
            return None
        return self.text[self.i]

    def advance(self):
        self.i += 1

    def skip_spaces(self):
        while self.current_char() is not None and self.current_char().isspace():
            self.advance()

    def read_number(self):
        start = self.i
        while self.current_char() is not None and self.current_char().isdigit():
            self.advance()
        return self.text[start:self.i]

    def read_word(self):
        start = self.i
        while self.current_char() is not None and (
            self.current_char().isalnum() or self.current_char() == "_"
        ):
            self.advance()
        return self.text[start:self.i]

    def tokenize(self):
        tokens = []

        while self.current_char() is not None:
            ch = self.current_char()

            if ch.isspace():
                self.skip_spaces()
                continue

            if ch.isdigit():
                num = self.read_number()
                tokens.append(Token("NUMBER", num))
                continue

            if ch.isalpha() or ch == "_":
                word = self.read_word()
                if word.upper() == "LET":
                    tokens.append(Token("LET", word))
                else:
                    tokens.append(Token("IDENT", word))
                continue

            if ch == "+":
                tokens.append(Token("PLUS", ch))
                self.advance()
                continue

            if ch == "-":
                tokens.append(Token("MINUS", ch))
                self.advance()
                continue

            if ch == "*":
                tokens.append(Token("STAR", ch))
                self.advance()
                continue

            if ch == "/":
                tokens.append(Token("SLASH", ch))
                self.advance()
                continue

            if ch == "=":
                tokens.append(Token("EQUAL", ch))
                self.advance()
                continue

            if ch == "(":
                tokens.append(Token("LPAREN", ch))
                self.advance()
                continue

            if ch == ")":
                tokens.append(Token("RPAREN", ch))
                self.advance()
                continue

            raise Exception("Bad character: " + ch)

        tokens.append(Token("EOF", ""))
        return tokens


# AST nodes
class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode({self.value})"


class VarNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"VarNode({self.name})"


class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op}, {self.right})"


class LetNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"LetNode({self.name}, {self.value})"


# parser
# grammar idea:
# statement   -> LET IDENT = expr | expr
# expr        -> term ((+|-) term)*
# term        -> factor ((*|/) factor)*
# factor      -> NUMBER | IDENT | (expr)
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def current_token(self):
        return self.tokens[self.i]

    def advance(self):
        self.i += 1

    def eat(self, token_type):
        tok = self.current_token()
        if tok.type != token_type:
            raise Exception(f"Expected {token_type}, got {tok.type}")
        self.advance()
        return tok

    def parse(self):
        node = self.statement()
        self.eat("EOF")
        return node

    def statement(self):
        if self.current_token().type == "LET":
            self.advance()
            name = self.eat("IDENT").value
            self.eat("EQUAL")
            value = self.expr()
            return LetNode(name, value)

        return self.expr()

    def expr(self):
        # handles + and -
        # this fixes the bug with things like 1+2+3+4
        node = self.term()

        while self.current_token().type in ("PLUS", "MINUS"):
            op = self.current_token().value
            self.advance()
            right = self.term()
            node = BinOpNode(node, op, right)

        return node

    def term(self):
        # handles * and /
        node = self.factor()

        while self.current_token().type in ("STAR", "SLASH"):
            op = self.current_token().value
            self.advance()
            right = self.factor()
            node = BinOpNode(node, op, right)

        return node

    def factor(self):
        tok = self.current_token()

        if tok.type == "NUMBER":
            self.advance()
            return NumberNode(int(tok.value))

        if tok.type == "IDENT":
            self.advance()
            return VarNode(tok.value)

        if tok.type == "LPAREN":
            self.advance()
            node = self.expr()
            self.eat("RPAREN")
            return node

        raise Exception("Unexpected token: " + str(tok))


# evaluator
class Evaluator:
    def __init__(self):
        self.vars = {}

    def visit(self, node):
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, VarNode):
            if node.name not in self.vars:
                raise Exception("Undefined variable: " + node.name)
            return self.vars[node.name]

        if isinstance(node, BinOpNode):
            left = self.visit(node.left)
            right = self.visit(node.right)

            if node.op == "+":
                return left + right
            if node.op == "-":
                return left - right
            if node.op == "*":
                return left * right
            if node.op == "/":
                return left / right

            raise Exception("Unknown operator: " + node.op)

        if isinstance(node, LetNode):
            value = self.visit(node.value)
            self.vars[node.name] = value
            return value

        raise Exception("Unknown node")


def run(text, env=None, show_tokens=False, show_ast=False):
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    if show_tokens:
        print("TOKENS:", tokens)

    parser = Parser(tokens)
    tree = parser.parse()

    if show_ast:
        print("AST:", tree)

    if env is None:
        env = Evaluator()

    result = env.visit(tree)
    return result, env


# test
if __name__ == "__main__":
    env = Evaluator()

    tests = [
        "1 + 2 + 3 + 4",
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "LET x=1+2",
        "x + 5",
        "LET y=x*10",
        "y + 1"
    ]

    for t in tests:
        print("input:", t)
        result, env = run(t, env, show_tokens=True, show_ast=True)
        print("result:", result)
        print("-" * 40)
