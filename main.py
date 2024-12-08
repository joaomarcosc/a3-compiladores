import sys
from helpers.read_code import read_code
from helpers.compile_to_python import compile_to_python

def save_and_run(generated_code, output_file='output_generated.py'):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(generated_code)
    
    print("Executando o código...")
    with open(output_file, 'r', encoding='utf-8') as file:
        exec(file.read())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_de_entrada>")
        sys.exit(1)

    input_file = sys.argv[1] 
    code = read_code(input_file)
    generated_code = compile_to_python(code)
    save_and_run(generated_code)
