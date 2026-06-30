"""
MiniLang Runtime
Provides a simple API to execute MiniLang code.
"""

from mini_lang.lexer import Lexer
from mini_lang.parser import Parser
from mini_lang.evaluator import Evaluator


def run(source, evaluator=None):
    """
    Compile and execute MiniLang source code.
    """

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    tree = parser.parse()

    if evaluator is None:
        evaluator = Evaluator()

    result = evaluator.visit(tree)

    return result, evaluator