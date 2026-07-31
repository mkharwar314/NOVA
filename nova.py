#!/usr/bin/env python3
import sys
import time

# =============================================================================
# 1. LEXER (TOKENIZER) - CASE INSENSITIVE
# =============================================================================

class TokenType:
    # Single-character tokens
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"

    # One or two character tokens
    ASSIGN = "ASSIGN"
    EQUAL = "EQUAL"
    BANG = "BANG"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"

    # Literals
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"

    # Keywords
    LET = "LET"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FN = "FN"
    RETURN = "RETURN"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NIL = "NIL"
    PRINT = "PRINT"
    EOF = "EOF"

KEYWORDS = {
    "let": TokenType.LET,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "fn": TokenType.FN,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "nil": TokenType.NIL,
    "print": TokenType.PRINT,
}

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def tokenize(self):
        while not self.is_at_end():
            self.start = self.current
            c = self.advance()
            if c in ' \r\t':
                continue
            elif c == '\n':
                self.line += 1
            elif c == '/':
                # Handle single-line comments //
                if self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            elif c == '+': self.add_token(TokenType.PLUS)
            elif c == '-': self.add_token(TokenType.MINUS)
            elif c == '*': self.add_token(TokenType.STAR)
            elif c == '(': self.add_token(TokenType.LPAREN)
            elif c == ')': self.add_token(TokenType.RPAREN)
            elif c == '{': self.add_token(TokenType.LBRACE)
            elif c == '}': self.add_token(TokenType.RBRACE)
            elif c == ',': self.add_token(TokenType.COMMA)
            elif c == ';': self.add_token(TokenType.SEMICOLON)
            elif c == '=':
                self.add_token(TokenType.EQUAL if self.match('=') else TokenType.ASSIGN)
            elif c == '!':
                self.add_token(TokenType.NOT_EQUAL if self.match('=') else TokenType.BANG)
            elif c == '<':
                self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            elif c == '>':
                self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            elif c in '"\'':
                self.string(c)
            elif c.isdigit():
                self.number()
            elif c.isalpha() or c == '_':
                self.identifier()
            else:
                raise SyntaxError(f"Unexpected character '{c}' on line {self.line}")

        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def peek(self):
        return '\0' if self.is_at_end() else self.source[self.current]

    def match(self, expected):
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def add_token(self, type_, value=None):
        text = self.source[self.start:self.current] if value is None else value
        self.tokens.append(Token(type_, text, self.line))

    def string(self, quote):
        while self.peek() != quote and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            raise SyntaxError(f"Unterminated string on line {self.line}")
        self.advance()  # Closing quote
        val = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, val)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.source[self.current + 1:self.current + 2].isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        val = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, val)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        
        # Case-Insensitive Lookup
        lower_text = text.lower()
        type_ = KEYWORDS.get(lower_text, TokenType.IDENTIFIER)
        stored_val = lower_text if type_ == TokenType.IDENTIFIER else text
        self.add_token(type_, stored_val)


# =============================================================================
# 2. PARSER & AST NODES
# =============================================================================

class ASTNode: pass

class Literal(ASTNode):
    def __init__(self, value): self.value = value

class Variable(ASTNode):
    def __init__(self, name): self.name = name

class Binary(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Unary(ASTNode):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class VarDecl(ASTNode):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Block(ASTNode):
    def __init__(self, statements): self.statements = statements

class IfStmt(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStmt(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FnDecl(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Call(ASTNode):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

class ReturnStmt(ASTNode):
    def __init__(self, value): self.value = value

class PrintStmt(ASTNode):
    def __init__(self, expression): self.expression = expression


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def declaration(self):
        if self.match(TokenType.LET): return self.var_declaration()
        if self.match(TokenType.FN): return self.function_declaration()
        return self.statement()

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return VarDecl(name.value, initializer)

    def function_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect function name.").value
        self.consume(TokenType.LPAREN, "Expect '(' after function name.")
        parameters = []
        if not self.check(TokenType.RPAREN):
            while True:
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name.").value)
                if not self.match(TokenType.COMMA): break
        self.consume(TokenType.RPAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LBRACE, "Expect '{' before function body.")
        body = self.block()
        return FnDecl(name, parameters, body)

    def statement(self):
        if self.match(TokenType.IF): return self.if_statement()
        if self.match(TokenType.WHILE): return self.while_statement()
        if self.match(TokenType.PRINT): return self.print_statement()
        if self.match(TokenType.RETURN): return self.return_statement()
        if self.match(TokenType.LBRACE): return self.block()
        return self.expression_statement()

    def if_statement(self):
        condition = self.expression()
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        return IfStmt(condition, then_branch, else_branch)

    def while_statement(self):
        condition = self.expression()
        body = self.statement()
        return WhileStmt(condition, body)

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return PrintStmt(value)

    def return_statement(self):
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return ReturnStmt(value)

    def block(self):
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RBRACE, "Expect '}' after block.")
        return Block(statements)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return expr

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.equality()
        if self.match(TokenType.ASSIGN):
            value = self.assignment()
            if isinstance(expr, Variable):
                return Assign(expr.name, value)
            raise SyntaxError("Invalid assignment target.")
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.previous()
            right = self.comparison()
            expr = Binary(expr, op, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            op = self.previous()
            right = self.term()
            expr = Binary(expr, op, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            right = self.factor()
            expr = Binary(expr, op, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.previous()
            right = self.unary()
            expr = Binary(expr, op, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.previous()
            right = self.unary()
            return Unary(op, right)
        return self.call()

    def call(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LPAREN):
                args = []
                if not self.check(TokenType.RPAREN):
                    while True:
                        args.append(self.expression())
                        if not self.match(TokenType.COMMA): break
                self.consume(TokenType.RPAREN, "Expect ')' after arguments.")
                expr = Call(expr, args)
            else:
                break
        return expr

    def primary(self):
        if self.match(TokenType.FALSE): return Literal(False)
        if self.match(TokenType.TRUE): return Literal(True)
        if self.match(TokenType.NIL): return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().value)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous().value)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
            return expr
        raise SyntaxError(f"Unexpected token {self.peek()} at line {self.peek().line}")

    def match(self, *types):
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def consume(self, type_, message):
        if self.check(type_): return self.advance()
        raise SyntaxError(f"{message} Found '{self.peek().value}' on line {self.peek().line}")

    def check(self, type_):
        return False if self.is_at_end() else self.peek().type == type_

    def advance(self):
        if not self.is_at_end(): self.current += 1
        return self.previous()

    def is_at_end(self): return self.peek().type == TokenType.EOF
    def peek(self): return self.tokens[self.current]
    def previous(self): return self.tokens[self.current - 1]


# =============================================================================
# 3. INTERPRETER & ENVIRONMENT - CASE INSENSITIVE
# =============================================================================

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        # Store in lower case for case-insensitivity
        self.values[name.lower()] = value

    def get(self, name):
        key = name.lower()
        if key in self.values:
            return self.values[key]
        if self.enclosing:
            return self.enclosing.get(key)
        raise NameError(f"Undefined variable '{name}'.")

    def assign(self, name, value):
        key = name.lower()
        if key in self.values:
            self.values[key] = value
            return
        if self.enclosing:
            self.enclosing.assign(key, value)
            return
        raise NameError(f"Undefined variable '{name}'.")

class NativeFunction:
    """Wrapper for built-in functions defined in Python."""
    def __init__(self, fn):
        self.fn = fn

    def call(self, interpreter, arguments):
        return self.fn(interpreter, arguments)

    def __repr__(self):
        return "<native fn>"

class NovaFunction:
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        env = Environment(self.closure)
        for param, arg in zip(self.declaration.params, arguments):
            env.define(param, arg)
        try:
            interpreter.execute_block(self.declaration.body.statements, env)
        except ReturnValue as ret:
            return ret.value
        return None

class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals

        # Register Native Built-in Functions
        def _native_input(interpreter, args):
            prompt = interpreter.stringify(args[0]) if len(args) > 0 else ""
            return input(prompt)

        def _native_clock(interpreter, args):
            return time.time()

        def _native_len(interpreter, args):
            if len(args) == 0:
                raise TypeError("len() expects 1 argument.")
            val = args[0]
            if isinstance(val, str):
                return float(len(val))
            raise TypeError("len() argument must be a string.")

        self.globals.define("input", NativeFunction(_native_input))
        self.globals.define("clock", NativeFunction(_native_clock))
        self.globals.define("len", NativeFunction(_native_len))

    def interpret(self, statements):
        try:
            for stmt in statements:
                self.execute(stmt)
        except Exception as e:
            print(f"Runtime Error: {e}", file=sys.stderr)

    def execute(self, stmt):
        method_name = f"visit_{type(stmt).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(stmt)

    def evaluate(self, expr):
        return self.execute(expr)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined.")

    def visit_Literal(self, node): return node.value
    def visit_Variable(self, node): return self.environment.get(node.name)

    def visit_Unary(self, node):
        right = self.evaluate(node.right)
        if node.operator.type == TokenType.MINUS: return -right
        if node.operator.type == TokenType.BANG: return not self.is_truthy(right)
        return None

    def visit_Binary(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        op = node.operator.type

        if op == TokenType.PLUS:
            if isinstance(left, str) or isinstance(right, str):
                return str(self.stringify(left)) + str(self.stringify(right))
            return left + right
        elif op == TokenType.MINUS: return left - right
        elif op == TokenType.STAR: return left * right
        elif op == TokenType.SLASH: return left / right
        elif op == TokenType.GREATER: return left > right
        elif op == TokenType.GREATER_EQUAL: return left >= right
        elif op == TokenType.LESS: return left < right
        elif op == TokenType.LESS_EQUAL: return left <= right
        elif op == TokenType.EQUAL: return left == right
        elif op == TokenType.NOT_EQUAL: return left != right
        return None

    def visit_VarDecl(self, node):
        value = None
        if node.initializer:
            value = self.evaluate(node.initializer)
        self.environment.define(node.name, value)

    def visit_Assign(self, node):
        value = self.evaluate(node.value)
        self.environment.assign(node.name, value)
        return value

    def visit_PrintStmt(self, node):
        value = self.evaluate(node.expression)
        print(self.stringify(value))

    def visit_Block(self, node):
        self.execute_block(node.statements, Environment(self.environment))

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous

    def visit_IfStmt(self, node):
        if self.is_truthy(self.evaluate(node.condition)):
            self.execute(node.then_branch)
        elif node.else_branch:
            self.execute(node.else_branch)

    def visit_WhileStmt(self, node):
        while self.is_truthy(self.evaluate(node.condition)):
            self.execute(node.body)

    def visit_FnDecl(self, node):
        func = NovaFunction(node, self.environment)
        self.environment.define(node.name, func)

    def visit_Call(self, node):
        callee = self.evaluate(node.callee)
        args = [self.evaluate(arg) for arg in node.arguments]
        if isinstance(callee, (NovaFunction, NativeFunction)):
            return callee.call(self, args)
        raise TypeError("Can only call functions.")

    def visit_ReturnStmt(self, node):
        val = self.evaluate(node.value) if node.value else None
        raise ReturnValue(val)

    def is_truthy(self, val):
        if val is None or val is False: return False
        return True

    def stringify(self, val):
        if val is None: return "nil"
        if isinstance(val, bool): return "true" if val else "false"
        if isinstance(val, float) and val.is_integer(): return str(int(val))
        return str(val)


# =============================================================================
# 4. CLI RUNNER & REPL MODE
# =============================================================================

def run_file(file_path):
    try:
        with open(file_path, "r") as f:
            source_code = f.read()

        tokens = Lexer(source_code).tokenize()
        ast = Parser(tokens).parse()
        Interpreter().interpret(ast)

    except FileNotFoundError:
        print(f"Error: Could not open file '{file_path}'")
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)

def run_repl():
    interpreter = Interpreter()
    print("Nova Script 2.1 Shell (Case-Insensitive)")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            line = input("nova > ")
            if line.strip().lower() == "exit":
                break
            if not line.strip():
                continue

            tokens = Lexer(line).tokenize()
            ast = Parser(tokens).parse()
            interpreter.interpret(ast)

        except SyntaxError as e:
            print(f"Syntax Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        run_repl()
