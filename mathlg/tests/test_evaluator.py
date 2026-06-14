"""Testes do avaliador (evaluator) do MathLg.

Testa o pipeline completo: tokenize → parse → evaluate.
"""

from __future__ import annotations

import math
import pytest

from mathlg.interpreter.environment import Environment
from mathlg.interpreter.evaluator import evaluate
from mathlg.lang.parser import parse
from mathlg.lang.tokenizer import tokenize
from mathlg.semantic.analyzer import analyze
from mathlg.semantic.errors import MathLgError, RuntimeError_


# --- Helpers ---

def _eval(text: str, lang: str = "pt-BR") -> object:
    """Tokeniza → parseia → analisa → avalia uma expressão completa."""
    env = Environment()
    tokens = tokenize(text, lang)
    ast = parse(tokens)
    errors = analyze(ast, env)
    if errors:
        raise errors[0]
    return evaluate(ast, env)


# --- Testes de operações básicas ---

class TestBasicOperations:
    """Operações aritméticas fundamentais."""

    def test_addition(self) -> None:
        assert _eval("2 mais 3", "pt-BR") == 5

    def test_subtraction(self) -> None:
        assert _eval("10 menos 4", "pt-BR") == 6

    def test_multiplication(self) -> None:
        assert _eval("7 vezes 6", "pt-BR") == 42

    def test_division(self) -> None:
        assert _eval("20 dividido por 4", "pt-BR") == 5.0

    def test_multiple_operations(self) -> None:
        assert _eval("2 mais 3 vezes 4", "pt-BR") == 14  # precedência: 2 + (3*4)

    def test_division_by_zero(self) -> None:
        with pytest.raises(RuntimeError_):
            _eval("10 dividido por 0", "pt-BR")


class TestMathFunctions:
    """Funções matemáticas (sqrt, sin, cos, log, etc.)."""

    def test_sqrt(self) -> None:
        result = _eval("raiz quadrada de 144", "pt-BR")
        assert result == pytest.approx(12.0)

    def test_sqrt_negative(self) -> None:
        with pytest.raises(RuntimeError_):
            _eval("raiz quadrada de -1", "pt-BR")

    def test_sin(self) -> None:
        result = _eval("seno de 0", "pt-BR")
        assert result == pytest.approx(0.0)

    def test_cos(self) -> None:
        result = _eval("cosseno de 0", "pt-BR")
        assert result == pytest.approx(1.0)

    def test_log(self) -> None:
        result = _eval("logaritmo de 1", "pt-BR")
        assert result == pytest.approx(0.0)

    def test_log_negative(self) -> None:
        with pytest.raises(RuntimeError_):
            _eval("logaritmo de -10", "pt-BR")

    def test_power(self) -> None:
        result = _eval("potencia de 2 elevado a 3", "pt-BR")
        assert result == 8


class TestVariables:
    """Atribuição e uso de variáveis."""

    def test_assignment_and_usage(self) -> None:
        env = Environment()
        tokens = tokenize("x = 10", "pt-BR")
        ast = parse(tokens)
        errors = analyze(ast, env)
        assert not errors
        evaluate(ast, env)

        tokens = tokenize("x mais 5", "pt-BR")
        ast = parse(tokens)
        errors = analyze(ast, env)
        assert not errors
        result = evaluate(ast, env)
        assert result == 15

    def test_variable_reuse(self) -> None:
        env = Environment()
        for expr in ["x = 2", "x = x mais 3"]:
            tokens = tokenize(expr, "pt-BR")
            ast = parse(tokens)
            errors = analyze(ast, env)
            assert not errors, f"Erro em '{expr}': {errors}"
            evaluate(ast, env)
        assert env.get("x") == 5


class TestEnglishSupport:
    """Operações em inglês."""

    def test_addition_en(self) -> None:
        assert _eval("2 plus 3", "en") == 5

    def test_sqrt_en(self) -> None:
        result = _eval("square root of 144", "en")
        assert result == pytest.approx(12.0)

    def test_mixed_expression_en(self) -> None:
        result = _eval("10 times 3 plus 2", "en")
        assert result == 32  # (10*3) + 2


class TestEdgeCases:
    """Casos extremos e comportamento de borda."""

    def test_float_result(self) -> None:
        result = _eval("10 dividido por 3", "pt-BR")
        assert isinstance(result, float)
        assert result == pytest.approx(3.333, rel=0.01)

    def test_integer_result(self) -> None:
        result = _eval("2 mais 3", "pt-BR")
        assert isinstance(result, int)

    def test_large_numbers(self) -> None:
        result = _eval("1000000 vezes 1000000", "pt-BR")
        assert result == 1_000_000_000_000

    def test_zero(self) -> None:
        assert _eval("0", "pt-BR") == 0


class TestComparisonAndBooleans:
    """Comparações e operadores lógicos."""

    def test_greater_than(self) -> None:
        assert _eval("10 maior que 5", "pt-BR") is True
        assert _eval("5 maior que 10", "pt-BR") is False

    def test_less_than(self) -> None:
        assert _eval("3 less than 10", "en") is True
        assert _eval("10 less than 3", "en") is False

    def test_equality(self) -> None:
        assert _eval("5 igual a 5", "pt-BR") is True
        assert _eval("5 igual a 6", "pt-BR") is False

    def test_not(self) -> None:
        assert _eval("nao verdadeiro", "pt-BR") is False
        assert _eval("not false", "en") is True

    def test_and(self) -> None:
        assert _eval("verdadeiro and verdadeiro", "pt-BR") is True
        assert _eval("verdadeiro and falso", "pt-BR") is False

    def test_or(self) -> None:
        assert _eval("verdadeiro ou falso", "pt-BR") is True
        assert _eval("falso ou falso", "pt-BR") is False
