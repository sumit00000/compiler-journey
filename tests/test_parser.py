import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mini_lang.lexer import Lexer
from mini_lang.parser import Parser

source = "LET x = 1 + 2 * 3;"

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)

tree = parser.parse()

print(tree)