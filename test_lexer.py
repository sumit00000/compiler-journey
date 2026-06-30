from mini_lang.lexer import Lexer

source = "LET x = 10 + 20;"

lexer = Lexer(source)

tokens = lexer.tokenize()

for token in tokens:
    print(token)