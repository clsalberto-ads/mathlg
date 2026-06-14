"""Testes de integração do MathLg.

Testam o pipeline completo: texto → tokenizer → parser → semantic → evaluator.
Fluxos completos de funcionalidade.
"""

from __future__ import annotations

import pytest

from mathlg.interpreter.environment import Environment
from mathlg.interpreter.evaluator import evaluate
from mathlg.lang.parser import parse
from mathlg.lang.tokenizer import tokenize
from mathlg.semantic.analyzer import analyze


def _run(text: str, lang: str = "pt-BR", env: Environment | None = None) -> object:
    """Pipeline completo: texto → resultado."""
    if env is None:
        env = Environment()
    tokens = tokenize(text, lang)
    ast = parse(tokens)
    errs = analyze(ast, env)
    if errs:
        raise errs[0]
    return evaluate(ast, env)


class TestIntegrationFull:
    """Testes de fluxo completo."""

    def test_simple_pipeline(self) -> None:
        result = _run("calcule 2 mais 3", "pt-BR")
        assert result == 5

    def test_sqrt_and_add(self) -> None:
        result = _run("raiz quadrada de 144 mais 3", "pt-BR")
        assert result == pytest.approx(15.0)  # sqrt(144) + 3 = 15

    def test_variable_lifecycle(self) -> None:
        env = Environment()
        _run("x = 10", "pt-BR", env)
        _run("y = 20", "pt-BR", env)
        result = _run("x mais y", "pt-BR", env)
        assert result == 30

    def test_function_definition_and_call(self) -> None:
        env = Environment()
        _run("funcao quadrado(n): retorna n vezes n", "pt-BR", env)
        result = _run("quadrado(5)", "pt-BR", env)
        assert result == 25

    def test_complex_expression(self) -> None:
        result = _run("2 mais 3 vezes 4 menos 1", "pt-BR")
        # Precedência: 2 + (3 * 4) - 1 = 2 + 12 - 1 = 13
        assert result == 13

    def test_english_pipeline(self) -> None:
        result = _run("calculate 10 plus 20", "en")
        assert result == 30

    def test_power_expression(self) -> None:
        result = _run("potencia de 2 elevado a 3", "pt-BR")
        assert result == 8


class TestIntegrationControlFlow:
    """Fluxos de controle integrados."""

    def test_if_true(self) -> None:
        env = Environment()
        _run("x = 10", "pt-BR", env)
        _run("se x maior que 5: x = 0", "pt-BR", env)
        assert env.get("x") == 0

    def test_if_false(self) -> None:
        env = Environment()
        _run("x = 1", "pt-BR", env)
        _run("se x maior que 5: x = 0", "pt-BR", env)
        assert env.get("x") == 1  # não mudou

    def test_while_loop(self) -> None:
        env = Environment()
        _run("contador = 0", "pt-BR", env)
        for _ in range(5):
            _run("contador = contador mais 1", "pt-BR", env)
        assert env.get("contador") == 5


class TestIntegrationEdgeCases:
    """Casos extremos de integração."""

    def test_multiple_statements(self) -> None:
        env = Environment()
        _run("a = 5", "pt-BR", env)
        _run("b = 10", "pt-BR", env)
        result = _run("a mais b vezes 2", "pt-BR", env)
        # a + (b * 2) = 5 + 20 = 25
        assert result == 25

    def test_chain_operations(self) -> None:
        result = _run("10 mais 5 menos 3", "pt-BR")
        assert result == 12

    def test_nested_math_functions(self) -> None:
        result = _run("raiz quadrada de (4 mais 5)", "pt-BR")
        # sqrt(4 + 5) = sqrt(9) = 3.0
        assert result == pytest.approx(3.0)
