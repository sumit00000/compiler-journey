import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mini_lang.lexer import Lexer
from mini_lang.parser import Parser

source = """
IF 10 > 5 THEN
LET x = 100;
ELSE
LET x = 0;
END;
"""

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)

tree = parser.parse()

print(tree)