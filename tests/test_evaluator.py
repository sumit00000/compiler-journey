import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mini_lang.lexer import Lexer
from mini_lang.parser import Parser
from mini_lang.evaluator import Evaluator


source = """
LET x = 10;
LET y = x * 2;
y + 5;
"""

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
tree = parser.parse()

evaluator = Evaluator()

result = evaluator.visit(tree)

print(result)