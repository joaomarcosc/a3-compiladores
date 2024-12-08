from lexer import tokenize
from parser import Parser

def compile_to_python(code):
    tokens = tokenize(code) 
    parser = Parser(tokens) 
    return parser.parse() 