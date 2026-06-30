print("=== Lexer ===")


source = "LET x = 1 + 2"

for token in source.split():
    if token == "LET":
        print("KEYWORD:", token)
    elif token.isdigit():
        print("NUMBER:", token)
    elif token in ["+", "-", "*", "/", "="]:
        print("OPERATOR:", token)
    elif token.isidentifier():
        print("IDENTIFIER:", token)
    else:
        print("UNKNOWN:", token)


print("\n=== Tiny Parser ===")

expression = "1 + 2 * 3"
tokens = expression.split()
print("expression:", expression)
print("tokens:", tokens)

# parse: numer opeator
left_num = int(tokens[0])
first_op = tokens[1]
middle_num = int(tokens[2])
second_op = tokens[3]
right_num = int(tokens[4])

# Handle operator precedence
if second_op in ["*"]:
    result = left_num + (middle_num * right_num)
elif first_op in ["/"]:
    result = left_num + (middle_num / right_num)
else:
    result = 0

print("result:", result)