from lexer import tokenize

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.indent_level = 0

    def add_line(self, line):
        indent = '    ' * self.indent_level
        self.code.append(f"{indent}{line}")

    def increase_indent(self):
        self.indent_level += 1

    def decrease_indent(self):
        if self.indent_level > 0:
            self.indent_level -= 1

    def get_code(self):
        return "\n".join(self.code)

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def declare_variable(self, name, var_type):
        if name in self.symbol_table:
            raise ValueError(f"Erro Semântico: Variável '{name}' já foi declarada.")
        self.symbol_table[name] = var_type

    def check_variable(self, name):
        if name not in self.symbol_table:
            raise ValueError(f"Erro Semântico: Variável '{name}' não foi declarada.")
        return self.symbol_table[name]

    def check_type_compatibility(self, var_name, expression_type):
        var_type = self.check_variable(var_name)
        if var_type != expression_type:
            raise ValueError(f"Erro Semântico: Tipo incompatível para '{var_name}', esperado '{var_type}' mas obteve '{expression_type}'.")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.generator = CodeGenerator()
        self.semantic_analyzer = SemanticAnalyzer()

    def parse_operador_relacional(self, operador):
        operadores_map = {
        'menor': '<',
        'maior': '>',
        'igual': '==',
        'diferente': '!=',
        'menor_igual': '<=',
        'maior_igual': '>=',
        'e': 'and',
        'ou': 'or',
        'modulo': '%',
    }
        if operador not in operadores_map:
            raise ValueError(f"Erro Semântico: Operador relacional '{operador}' inválido.")
        return operadores_map[operador]



    def match(self, expected_type):
        if self.position < len(self.tokens) and self.tokens[self.position][0] == expected_type:
           self.position += 1 
           return True
        return False

    def cmd_if(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'eleQueQueremos'")

        left_expr, left_type = self.expr()

        if not self.match('REL_OP'):
            self.error("Operador relacional esperado em 'eleQueQueremos'")
        operador = self.tokens[self.position - 1][1]
        operador_python = self.parse_operador_relacional(operador)


        right_expr, right_type = self.expr()

        if not self.match('RPAREN'):
            self.error("Esperado ')' após expressão em 'eleQueQueremos'")

        # Gera o código para a condicional
        self.generator.add_line(f"if {left_expr} {operador_python} {right_expr}:")
        self.generator.increase_indent()

        if not self.match('LBRACE'):
            self.error("Esperado '{' após condição 'eleQueQueremos'")
        self.bloco()
        self.generator.decrease_indent()

        if not self.match('RBRACE'):
            self.error("Esperado '}' após bloco 'eleQueQueremos'")

        if self.match('ELSE'):
            self.generator.add_line("else:")
            self.generator.increase_indent()
            if not self.match('LBRACE'):
                self.error("Esperado '{' após 'naoVaiDarNao'")
            self.bloco()
            self.generator.decrease_indent()
            if not self.match('RBRACE'):
                self.error("Esperado '}' após bloco 'naoVaiDarNao'")



    def error(self, message="Erro de Sintaxe"):
        current_token = self.tokens[self.position] if self.position < len(self.tokens) else "EOF"
        raise SyntaxError(f"{message} no token {current_token} na posição {self.position}")

    def parse(self):
        self.program()
        return self.generator.get_code()

    def program(self):
        if not self.match('PROGRAM'):
            self.error("Esperado 'inicioDoPrograma'")
        self.declara()
        self.bloco()
        if not self.match('END_PROGRAM'):
            self.error("Esperado 'fimDoPrograma'")

    def declara(self):
        while self.tokens[self.position][0] in ['INT', 'DECIMAL', 'TEXT', 'BOOLEAN']:
            tipo = self.tipo()
            ids = self.id_list()
            for var in ids:
                self.semantic_analyzer.declare_variable(var, tipo)
                if tipo == "monstro":
                    self.generator.add_line(f"{var} = 0  # int")
                elif tipo == "trapezio":
                    self.generator.add_line(f"{var} = 0.0  # float")
                elif tipo == "frango":
                    self.generator.add_line(f"{var} = ''  # str")
                elif tipo == "barril":
                    self.generator.add_line(f"{var} = False  # bool")


    def tipo(self):
        if self.match('INT'):
            return "monstro"
        elif self.match('DECIMAL'):
            return "trapezio"
        elif self.match('TEXT'):
            return "frango"
        elif self.match('BOOLEAN'):
            return "barril"
        else:
            self.error("Tipo de variável esperado")


    def id_list(self):
        ids = []
        if not self.match('ID'):
            self.error("Esperado identificador")
        ids.append(self.tokens[self.position - 1][1])
        while self.match('COMMA'):
            if not self.match('ID'):
                self.error("Esperado identificador após ','")
            ids.append(self.tokens[self.position - 1][1])
        return ids

    def bloco(self):
        while self.tokens[self.position][0] in ['READ', 'WRITE', 'ID', 'IF', 'WHILE', 'FOR']:
            self.cmd()

    def cmd(self):
        if self.match('READ'):
            self.cmd_leitura()
        elif self.match('WRITE'):
            self.cmd_escrita()
        elif self.match('IF'):
            self.cmd_if()
        elif self.match('WHILE'):
            self.cmd_while() 
        elif self.match('FOR'):
            self.cmd_for() 
        elif self.tokens[self.position][0] == 'ID' and self.tokens[self.position + 1][0] == 'ASSIGN':
            self.cmd_expr()
        else:
            self.error("Comando inválido")


    def cmd_while(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'queroMais'")

        left_expr, left_type = self.expr()

        if not self.match('REL_OP'):
            self.error("Operador relacional esperado em 'queroMais'")
        operador = self.tokens[self.position - 1][1]
        operador_python = self.parse_operador_relacional(operador)

        right_expr, right_type = self.expr()

        if not self.match('RPAREN'):
            self.error("Esperado ')' após expressão em 'queroMais'")

        self.generator.add_line(f"while {left_expr} {operador_python} {right_expr}:")
        self.generator.increase_indent()

        if not self.match('LBRACE'):
            self.error("Esperado '{' após condição 'queroMais'")
        self.bloco()
        self.generator.decrease_indent()

        if not self.match('RBRACE'):
            self.error("Esperado '}' após bloco 'queroMais'")


    def cmd_leitura(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'leia'")
        if not self.match('ID'):
            self.error("Esperado identificador em 'leia'")
        var_name = self.tokens[self.position - 1][1]
        var_type = self.semantic_analyzer.check_variable(var_name) 
        if not self.match('RPAREN'):
            self.error("Esperado ')' após identificador em 'leia'")
        if var_type == "monstro":
            self.generator.add_line(f"{var_name} = int(input())")
        elif var_type == "trapezio":
            self.generator.add_line(f"{var_name} = float(input())")
        elif var_type == "frango":
            self.generator.add_line(f"{var_name} = input()")

    def cmd_escrita(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'escreva'")
        if self.match('STRING'):
            text = self.tokens[self.position - 1][1]
            self.generator.add_line(f"print({text})")
        elif self.match('ID'):
            var_name = self.tokens[self.position - 1][1]
            self.semantic_analyzer.check_variable(var_name)
            self.generator.add_line(f"print({var_name})")
        else:
            self.error("Esperado string ou identificador em 'escreva'")
        if not self.match('RPAREN'):
            self.error("Esperado ')' após 'escreva'")

    def cmd_expr(self):
        if not self.match('ID'):
            self.error("Esperado identificador")
        var_name = self.tokens[self.position - 1][1]
        if not self.match('ASSIGN'):
            self.error("Esperado '=' para atribuição")
        expression_code, expression_type = self.expr()  
        var_type = self.semantic_analyzer.check_variable(var_name)  
        self.semantic_analyzer.check_type_compatibility(var_name, expression_type)  
        self.generator.add_line(f"{var_name} = {expression_code}") 



    def expr(self):
        left_code, left_type = self.termo()
        while self.match('ADD_OP'):
            op = self.tokens[self.position - 1][1]
            op_python = {'mais': '+', 'menos': '-'}.get(op, op)
            right_code, right_type = self.termo()
            left_code = f"({left_code} {op_python} {right_code})"
            left_type = "trapezio" if left_type == "trapezio" or right_type == "trapezio" else "monstro"
        return left_code, left_type



    def termo(self):
        left_code, left_type = self.fator()
        while self.match('MUL_OP') or self.match('MOD_OP'):
            op = self.tokens[self.position - 1][1]
            op_python = {'vezes': '*', 'dividido': '/', 'modulo': '%'}.get(op, op)
            right_code, right_type = self.fator()
            left_code = f"({left_code} {op_python} {right_code})"
            left_type = "trapezio" if left_type == "trapezio" or right_type == "trapezio" else "monstro"
        return left_code, left_type


    def fator(self):
        if self.match('NUMBER'):
            code = self.tokens[self.position - 1][1]
            return code, "monstro" if '.' not in code else "trapezio"
        elif self.match('ID'):
           var_name = self.tokens[self.position - 1][1]
           var_type = self.semantic_analyzer.check_variable(var_name)
           return var_name, var_type
        elif self.match('STRING'): 
           string_value = self.tokens[self.position - 1][1]
           return string_value, "frango"
        elif self.match('TRUE'): 
            return "True", "barril"
        elif self.match('FALSE'): 
            return "False", "barril"
        elif self.match('LPAREN'):
           code, expr_type = self.expr()
           if not self.match('RPAREN'):
               self.error("Esperado ')' após expressão")
           return f"({code})", expr_type
        else:
           self.error("Fator esperado")
           
    def cmd_for(self):
        if not self.match('LPAREN'):
            self.error("Esperado '(' após 'mandaMais'")

        if not self.match('ID') or not self.match('ASSIGN'):
            self.error("Esperado inicialização no 'mandaMais'")
        var_name = self.tokens[self.position - 2][1] 
        init_value, init_type = self.expr()
        self.generator.add_line(f"{var_name} = {init_value}")

        if not self.match('SEMI'):
            self.error(f"Esperado ';' após inicialização no 'mandaMais', mas encontrado {self.tokens[self.position]}")

        left_expr, left_type = self.expr()

        if not self.match('REL_OP'):
            self.error("Esperado operador relacional no 'mandaMais'")
        operador = self.tokens[self.position - 1][1]
        operador_python = self.parse_operador_relacional(operador)

        right_expr, right_type = self.expr()

        condition_full = f"{left_expr} {operador_python} {right_expr}"

        if not self.match('SEMI'):
            self.error(f"Esperado ';' após condição no 'mandaMais', mas encontrado {self.tokens[self.position]}")

        if not self.match('ID'):
            self.error("Esperado identificador no incremento do 'mandaMais'")
        increment_var = self.tokens[self.position - 1][1]
        if not self.match('ASSIGN'):
            self.error("Esperado '=' no incremento do 'mandaMais'")
        increment_expr, increment_type = self.expr()
        increment_code = f"{increment_var} = {increment_expr}"

        if not self.match('RPAREN'):
            self.error(f"Esperado ')' após incremento no 'mandaMais', mas encontrado {self.tokens[self.position]}")

        if not self.match('LBRACE'):
            self.error("Esperado '{' após condição do 'mandaMais'")

        self.generator.add_line(f"while {condition_full}:")
        self.generator.increase_indent()
        self.bloco() 
        self.generator.add_line(f"{increment_code}") 
        self.generator.decrease_indent()

        if not self.match('RBRACE'):
            self.error("Esperado '}' após bloco do 'mandaMais'")








