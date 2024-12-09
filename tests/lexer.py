from lexer import tokenize

def test_rel_op():
    test_code = "<= >= == != < >"
    try:
        tokens = tokenize(test_code)
        for token in tokens:
            print(token)
    except SyntaxError as e:
        print(e)

if __name__ == "__main__":
    test_rel_op()
