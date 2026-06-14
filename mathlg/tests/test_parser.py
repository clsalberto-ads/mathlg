"""Testes do parser do MathLg.

Categorias:
    1. Expressões aritméticas simples
    2. Expressões com funções matemáticas
    3. Atribuição de variáveis
    4. Precedência de operadores
    5. Parênteses
    6. Erros de sintaxe
    7. Control flow (if, while, for)
    8. Funções
"""

from __future__ import annotations

import pytest

from mathlg.lang.ast_nodes import (
    Assignment,
    BinaryOp, BinOp,
    BoolLiteral,
    ForLoop,
    FunctionCall,
    FunctionDef,
    IfStatement,
    MathFunction, MathFunctionCall,
    NumberLiteral,
    Program,
    StringLiteral,
    UnaryOp, UnaryOpEnum,
    WhileLoop,
)
from mathlg.lang.parser import parse
from mathlg.lang.tokenizer import tokenize
from mathlg.semantic.errors import ParserError


# --- Helpers ---

def _parse(text: str, lang: str = "pt-BR") -> Program:
    """Tokeniza e parseia uma string."""
    tokens = tokenize(text, lang)
    return parse(tokens)


# --- Testes ---

class TestParserSimpleExpressions:
    """Testes de expressões aritméticas simples."""

    def test_number_literal(self) -> None:
        ast = _parse("42")
        assert len(ast.statements) == 1
        stmt = ast.statements[0]
        assert isinstance(stmt, NumberLiteral)
        assert stmt.value == 42

    def test_float_literal(self) -> None:
        ast = _parse("3.14")
        stmt = ast.statements[0]
        assert isinstance(stmt, NumberLiteral)
        assert stmt.value == 3.14

    def test_simple_addition(self) -> None:
        ast = _parse("2 mais 3", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOp)
        assert stmt.op == BinOp.PLUS
        assert isinstance(stmt.left, NumberLiteral)
        assert stmt.left.value == 2
        assert isinstance(stmt.right, NumberLiteral)
        assert stmt.right.value == 3

    def test_simple_subtraction(self) -> None:
        ast = _parse("10 minus 3", "en")
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOp)
        assert stmt.op == BinOp.MINUS

    def test_multiplication(self) -> None:
        ast = _parse("4 vezes 5", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOp)
        assert stmt.op == BinOp.TIMES

    def test_division(self) -> None:
        ast = _parse("20 divided by 4", "en")
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOp)
        assert stmt.op == BinOp.DIVIDE


class TestParserMathFunctions:
    """Testes de funções matemáticas."""

    def test_sqrt(self) -> None:
        ast = _parse("raiz quadrada de 144", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, MathFunctionCall)
        assert stmt.func == MathFunction.SQRT
        assert len(stmt.arguments) == 1
        assert isinstance(stmt.arguments[0], NumberLiteral)
        assert stmt.arguments[0].value == 144

    def test_sin(self) -> None:
        ast = _parse("seno de 0", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, MathFunctionCall)
        assert stmt.func == MathFunction.SIN

    def test_cos(self) -> None:
        ast = _parse("cosine of 0", "en")
        stmt = ast.statements[0]
        assert isinstance(stmt, MathFunctionCall)
        assert stmt.func == MathFunction.COS


class TestParserPrecedence:
    """Testes de precedência de operadores."""

    def test_multiplication_before_addition(self) -> None:
        """2 + 3 * 4 = 2 + (3 * 4), não (2 + 3) * 4"""
        ast = _parse("2 mais 3 vezes 4", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOp)
        assert stmt.op == BinOp.PLUS  # raiz é PLUS
        assert isinstance(stmt.right, BinaryOp)
        assert stmt.right.op == BinOp.TIMES

    def test_parentheses_override(self) -> None:
        """Teste conceitual: (2 + 3) * 4"""
        # Esta sintaxe pode variar — o teste verifica que parênteses funcionam
        ast = _parse("(2 mais 3) vezes 4", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOp)
        assert stmt.op == BinOp.TIMES
        assert isinstance(stmt.left, BinaryOp)  # (2 + 3) é binário
        assert stmt.left.op == BinOp.PLUS


class TestParserAssignment:
    """Testes de atribuição de variáveis."""

    def test_simple_assignment(self) -> None:
        ast = _parse("x = 10", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, Assignment)
        assert stmt.target.name == "x"
        assert isinstance(stmt.value, NumberLiteral)
        assert stmt.value.value == 10

    def test_assignment_with_expression(self) -> None:
        ast = _parse("resultado = 2 mais 3", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, Assignment)
        assert stmt.target.name == "resultado"
        assert isinstance(stmt.value, BinaryOp)


class TestParserControlFlow:
    """Testes de control flow."""

    def test_if_statement(self) -> None:
        ast = _parse("se x maior que 0: mostre x", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, IfStatement)

    def test_while_loop(self) -> None:
        ast = _parse("enquanto x menor que 10: x = x mais 1", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, WhileLoop)

    def test_for_loop(self) -> None:
        ast = _parse("para i = 1 ate 10: mostre i", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, ForLoop)

    def test_if_else(self) -> None:
        ast = _parse("se x maior que 0: mostre x senao: mostre 0", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, IfStatement)
        assert stmt.else_body is not None


class TestParserFunctions:
    """Testes de definição e chamada de funções."""

    def test_function_definition(self) -> None:
        ast = _parse("funcao dobro(x): retorna x vezes 2", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionDef)
        assert stmt.name == "dobro"
        assert stmt.params == ["x"]

    def test_function_call(self) -> None:
        ast = _parse("dobro(5)", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionCall)
        assert stmt.name == "dobro"
        assert len(stmt.arguments) == 1


class TestParserErrors:
    """Testes de erros de sintaxe."""

    def test_unexpected_token(self) -> None:
        with pytest.raises(ParserError):
            _parse("=", "pt-BR")

    def test_unclosed_parenthesis(self) -> None:
        with pytest.raises(ParserError):
            _parse("(2 mais 3", "pt-BR")


class TestParserBooleans:
    """Testes de booleanos."""

    def test_boolean_literal(self) -> None:
        ast = _parse("verdadeiro", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, BoolLiteral)
        assert stmt.value is True

    def test_boolean_expression(self) -> None:
        ast = _parse("10 maior que 5 and 3 menor que 8", "pt-BR")
        stmt = ast.statements[0]
        assert isinstance(stmt, BinaryOp)
        assert stmt.op == BinOp.AND
