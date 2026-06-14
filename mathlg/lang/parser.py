"""Parser do MathLg: token stream → AST (Abstract Syntax Tree).

Implementa um parser descendente recursivo manual (recursive descent).
A gramática é LL(1) para a maior parte dos casos, com backtracking
limitado para expressões ambíguas.

Precedência de operadores (mais alta para mais baixa):
  1. Parênteses
  2. Funções matemáticas (sqrt, sin, cos, log, abs)
  3. Potência
  4. Unário (menos, não)
  5. Multiplicação / Divisão
  6. Adição / Subtração
  7. Comparação
  8. AND
  9. OR (mais baixa)
"""

from __future__ import annotations

from mathlg.lang.ast_nodes import (
    Assignment,
    BinaryOp, BinOp,
    BoolLiteral,
    CompareOp,
    Comparison,
    ExportStatement,
    Expression,
    ForLoop,
    FunctionCall,
    FunctionDef,
    Identifier,
    IfStatement,
    MathFunction, MathFunctionCall,
    NumberLiteral,
    PrintStatement,
    Program,
    ReturnStatement,
    Statement,
    StringLiteral,
    UnaryOp, UnaryOpEnum,
    WhileLoop,
)
from mathlg.lang.tokens import Token, TokenType
from mathlg.semantic.errors import ParserError


class Parser:
    """Parser descendente recursivo para MathLg.

    Consome tokens um a um (lookahead de 1 token) e constrói a AST.
    """

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        """Retorna o token atual sem consumi-lo."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(type=TokenType.EOF)

    def advance(self) -> Token:
        """Consome e retorna o token atual."""
        token = self.tokens[self.pos] if self.pos < len(self.tokens) else Token(type=TokenType.EOF)
        self.pos += 1
        return token

    def expect(self, *types: TokenType) -> Token:
        """Consome o token atual e verifica se é um dos tipos esperados.

        Raises:
            ParserError: Se o token atual não for do tipo esperado.
        """
        token = self.peek()
        if token.type not in types:
            expected = ", ".join(t.name for t in types)
            got = token.type.name
            raise ParserError(
                f"Esperado {expected}, encontrado {got} ('{token.value}')"
                if token.value
                else f"Esperado {expected}, encontrado {got}"
            )
        return self.advance()

    def parse(self) -> Program:
        """Parseia o programa completo."""
        statements: list[Statement] = []

        while self.peek().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)

        return Program(statements=statements)

    def parse_statement(self) -> Statement | None:
        """Parseia um único statement.

        Determina o tipo baseado no token atual.
        """
        token = self.peek()

        match token.type:
            case TokenType.FN:
                return self.parse_function_def()
            case TokenType.IF:
                return self.parse_if_statement()
            case TokenType.WHILE:
                return self.parse_while_loop()
            case TokenType.FOR:
                return self.parse_for_loop()
            case TokenType.EXPORT:
                return self.parse_export()
            case TokenType.RETURN:
                return self.parse_return()
            case TokenType.CALC:
                # "mostre" / "calcule" — consome o token e parseia expressão
                self.advance()
                expr = self.parse_expression()
                return PrintStatement(expression=expr)
            case TokenType.EOF:
                return None
            case _:
                # Pode ser assignment ou expression
                return self.parse_assignment_or_expression()

    def parse_assignment_or_expression(self) -> Statement:
        """Parseia assignment (x = ...) ou expressão.

        Precisa de lookahead: se após o IDENTIFIER vier ASSIGN, é assignment.
        """
        # Tentativa: ver se é um assignment
        # Precisa de posição de save para backtracking
        save_pos = self.pos

        try:
            if self.peek().type == TokenType.IDENTIFIER:
                id_token = self.peek()
                self.advance()
                if self.peek().type == TokenType.ASSIGN:
                    # É assignment!
                    self.advance()  # consome o =
                    target = Identifier(name=str(id_token.value))
                    value = self.parse_expression()
                    return Assignment(target=target, value=value)

            # Não é assignment, volta e parseia como expressão
            self.pos = save_pos
            return self.parse_expression()

        except ParserError:
            self.pos = save_pos
            return self.parse_expression()

    def parse_expression(self) -> Expression:
        """Parseia uma expressão (precedência mais baixa: OR)."""
        return self.parse_logical_or()

    def parse_logical_or(self) -> Expression:
        """OR lógico: <and> (ou <and>)*"""
        left = self.parse_logical_and()

        while self.peek().type == TokenType.OR:
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(op=BinOp.OR, left=left, right=right)

        return left

    def parse_logical_and(self) -> Expression:
        """AND lógico: <comparison> (e <comparison>)*"""
        left = self.parse_comparison()

        while self.peek().type == TokenType.AND:
            self.advance()
            right = self.parse_comparison()
            left = BinaryOp(op=BinOp.AND, left=left, right=right)

        return left

    def parse_comparison(self) -> Expression:
        """Comparação: <addition> (<comp_op> <addition>)*"""
        left = self.parse_addition()

        op_map = {
            TokenType.GT: CompareOp.GT,
            TokenType.LT: CompareOp.LT,
            TokenType.EQ: CompareOp.EQ,
            TokenType.GTE: CompareOp.GTE,
            TokenType.LTE: CompareOp.LTE,
            TokenType.NEQ: CompareOp.NEQ,
        }

        while self.peek().type in op_map:
            op_type = self.advance().type
            op = op_map[op_type]
            right = self.parse_addition()
            left = Comparison(op=op, left=left, right=right)

        return left

    def parse_addition(self) -> Expression:
        """Adição/Subtração: <term> ((mais|menos) <term>)*"""
        left = self.parse_term()

        while self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            op = BinOp.PLUS if op_token.type == TokenType.PLUS else BinOp.MINUS
            right = self.parse_term()
            left = BinaryOp(op=op, left=left, right=right)

        return left

    def parse_term(self) -> Expression:
        """Multiplicação/Divisão: <factor> ((vezes|dividido) <factor>)*"""
        left = self.parse_unary()

        while self.peek().type in (TokenType.TIMES, TokenType.DIVIDE):
            op_token = self.advance()
            op = BinOp.TIMES if op_token.type == TokenType.TIMES else BinOp.DIVIDE
            right = self.parse_unary()
            left = BinaryOp(op=op, left=left, right=right)

        return left

    def parse_unary(self) -> Expression:
        """Operador unário: NOT? <power>"""
        if self.peek().type == TokenType.NOT:
            self.advance()
            operand = self.parse_power()
            return UnaryOp(op=UnaryOpEnum.NOT, operand=operand)

        if self.peek().type == TokenType.MINUS:
            self.advance()
            operand = self.parse_power()
            return UnaryOp(op=UnaryOpEnum.MINUS, operand=operand)

        return self.parse_power()

    def parse_power(self) -> Expression:
        """Potência: <call> (elevado a <call>)*

        A potencia é associativa à direita: a^b^c = a^(b^c)
        """
        left = self.parse_call_or_primary()

        if self.peek().type == TokenType.POWER:
            self.advance()
            # Trata POWER como função binária: power(base, expoente)
            right = self.parse_call_or_primary()
            return MathFunctionCall(
                func=MathFunction.POWER,
                arguments=[left, right],
            )

        return left

    def parse_call_or_primary(self) -> Expression:
        """Chamada de função ou primary.

        A ordem é importante:
        1. Funções matemáticas (SQRT, SIN, COS, etc.) são tokens próprios
        2. IDENTIFIER pode ser variável, chamada de função, ou math function
        3. Demais casos vão para parse_primary (números, parênteses, etc.)
        """
        # 1. Funções matemáticas como token próprio (SQRT, SIN, COS, etc.)
        if self._is_math_function():
            return self.parse_math_function()

        # 2. Identificador ou chamada de função
        if self.peek().type == TokenType.IDENTIFIER:
            id_token = self.peek()
            self.advance()

            if self.peek().type == TokenType.LPAREN:
                # Chamada de função do usuário
                return self.parse_function_call_after_id(str(id_token.value))

            # É identificador simples (variável)
            return Identifier(name=str(id_token.value))

        # 3. Primary (números, parênteses, strings, etc.)
        return self.parse_primary()

    def _is_math_function(self) -> bool:
        """Verifica se o token atual é início de uma função matemática."""
        return self.peek().type in (
            TokenType.SQRT, TokenType.SIN, TokenType.COS,
            TokenType.LOG, TokenType.ABS, TokenType.ROUND,
            TokenType.POWER,
        )

    def parse_math_function(self) -> Expression:
        """Parseia chamada de função matemática embutida.

        sqrt, sin, cos, log, abs, round, power
        """
        func_map = {
            TokenType.SQRT: MathFunction.SQRT,
            TokenType.SIN: MathFunction.SIN,
            TokenType.COS: MathFunction.COS,
            TokenType.LOG: MathFunction.LOG,
            TokenType.ABS: MathFunction.ABS,
            TokenType.ROUND: MathFunction.ROUND,
        }

        token = self.advance()

        if token.type == TokenType.POWER:
            # Potência: power(left, right)
            left = self.parse_call_or_primary()
            # Precisa do "to the power of" / "elevado a" token
            # que já pode ter sido consumido pelo tokenizer
            # Se ainda está no stream, consome
            if self.peek().type in (TokenType.POWER,):
                self.advance()
            right = self.parse_call_or_primary()
            return MathFunctionCall(
                func=MathFunction.POWER,
                arguments=[left, right],
            )

        func = func_map.get(token.type)
        if func is None:
            raise ParserError(f"Função matemática desconhecida: {token.type.name}")

        # Funções unárias: sqrt, sin, cos, log, abs, round
        arg = self.parse_call_or_primary()
        return MathFunctionCall(func=func, arguments=[arg])

    def parse_function_call_after_id(self, name: str) -> FunctionCall:
        """Parseia chamada de função do usuário depois do nome já consumido."""
        self.expect(TokenType.LPAREN)
        args: list[Expression] = []

        if self.peek().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            while self.peek().type == TokenType.COMMA:
                self.advance()
                args.append(self.parse_expression())

        self.expect(TokenType.RPAREN)
        return FunctionCall(name=name, arguments=args)

    def parse_primary(self) -> Expression:
        """Parseia um elemento primário: número, string, bool, parênteses."""
        token = self.advance()

        match token.type:
            case TokenType.NUMBER:
                value = token.value
                assert isinstance(value, (int, float))
                return NumberLiteral(value=value)

            case TokenType.STRING:
                value = token.value
                assert isinstance(value, str)
                return StringLiteral(value=value)

            case TokenType.TRUE:
                return BoolLiteral(value=True)

            case TokenType.FALSE:
                return BoolLiteral(value=False)

            case TokenType.IDENTIFIER:
                name = str(token.value)
                if self.peek().type == TokenType.LPAREN:
                    return self.parse_function_call_after_id(name)
                return Identifier(name=name)

            case TokenType.LPAREN:
                expr = self.parse_expression()
                self.expect(TokenType.RPAREN)
                return expr

            case TokenType.MINUS:
                operand = self.parse_primary()
                return UnaryOp(op=UnaryOpEnum.MINUS, operand=operand)

            case _:
                raise ParserError(
                    f"Token inesperado: {token.type.name} ('{token.value}')"
                    if token.value
                    else f"Token inesperado: {token.type.name}"
                )

    # --- Statements estruturados ---

    def parse_if_statement(self) -> IfStatement:
        """se <condicao> <bloco> [senao <bloco>]"""
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        then_body = self.parse_block()

        else_body: list[Statement] | None = None
        if self.peek().type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.COLON)
            else_body = self.parse_block()

        return IfStatement(condition=condition, then_body=then_body, else_body=else_body)

    def parse_while_loop(self) -> WhileLoop:
        """enquanto <condicao> <bloco>"""
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        body = self.parse_block()
        return WhileLoop(condition=condition, body=body)

    def parse_for_loop(self) -> ForLoop:
        """para <var> = <start> ate <end> <bloco>"""
        self.expect(TokenType.FOR)
        id_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGN)
        start = self.parse_expression()
        self.expect(TokenType.FOR)  # "ate"/"to" pode ser tokenizado como FOR
        end = self.parse_expression()
        self.expect(TokenType.COLON)
        body = self.parse_block()

        return ForLoop(
            variable=Identifier(name=str(id_token.value)),
            start=start,
            end=end,
            body=body,
        )

    def parse_function_def(self) -> FunctionDef:
        """funcao <nome>(<params>) <bloco>"""
        self.expect(TokenType.FN)
        id_token = self.expect(TokenType.IDENTIFIER)
        name = str(id_token.value)

        self.expect(TokenType.LPAREN)
        params: list[str] = []
        if self.peek().type == TokenType.IDENTIFIER:
            param_token = self.advance()
            params.append(str(param_token.value))
            while self.peek().type == TokenType.COMMA:
                self.advance()
                param_token = self.expect(TokenType.IDENTIFIER)
                params.append(str(param_token.value))
        self.expect(TokenType.RPAREN)

        self.expect(TokenType.COLON)
        body = self.parse_block()

        return FunctionDef(name=name, params=params, body=body)

    def parse_return(self) -> ReturnStatement:
        """retorna <expressão>"""
        self.expect(TokenType.RETURN)
        value = self.parse_expression() if self.peek().type != TokenType.EOF else None
        return ReturnStatement(value=value)

    def parse_export(self) -> ExportStatement:
        """exportar csv|json"""
        self.expect(TokenType.EXPORT)
        fmt_token = self.expect(TokenType.IDENTIFIER)
        fmt = str(fmt_token.value).lower()
        if fmt not in ("csv", "json"):
            raise ParserError(f"Formato de exportação inválido: {fmt}")
        return ExportStatement(format=fmt)

    def parse_block(self) -> list[Statement]:
        """Parseia um bloco de statements.

        No MVP, blocos são delimitados por : na mesma linha.
        Exemplo: se x > 0: mostre x
        Suporte a blocos multilinha com indentação pode ser adicionado depois.
        """
        statements: list[Statement] = []

        # Bloco inline (após o :)
        # O bloco termina em EOF, NEWLINE, ELSE (para if-else inline),
        # ou COLON (para else: que já foi consumido)
        while self.peek().type not in (TokenType.EOF, TokenType.NEWLINE, TokenType.ELSE):
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)

        return statements


def parse(tokens: list[Token]) -> Program:
    """Função de conveniência: token stream → AST.

    Args:
        tokens: Lista de tokens do tokenizador.

    Returns:
        AST do programa.

    Raises:
        ParserError: Se a sintaxe estiver incorreta.
    """
    parser = Parser(tokens)
    return parser.parse()
