import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mini_lang.lexer import Lexer

source = """
IF 10 > 5 THEN
LET x = 100;
ELSE
LET x = 0;
END;
"""

lexer = Lexer(source)

for token in lexer.tokenize():
    print(token)