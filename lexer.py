import re
from tokens import tokens_definitions

def lex(code):
    tokens_found = []
    position = 0
    while position < len(code):
        match = None
        for token_type, pattern in tokens_definitions.items():
            regex = re.compile(pattern)
            match = regex.match(code, position)
            if match:
                text = match.group(0)
                if token_type not in ['WHITESPACE', 'NEWLINE']: 
                    tokens_found.append((token_type, text))
                position = match.end(0)
                break
        if not match:
            raise SyntaxError(f'Erro Léxico: caractere inesperado "{code[position]}" na posição {position}')
    return tokens_found

def tokenize(code):
    return lex(code)

def test_rel_op():
    test_code = "menor_igual maior_igual igual diferente menor maior"
    try:
        tokens = tokenize(test_code)
        for token in tokens:
            print(token)
    except SyntaxError as e:
        print(e)

if __name__ == "__main__":
    test_rel_op()
