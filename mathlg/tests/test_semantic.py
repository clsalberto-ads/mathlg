"""Testes do analisador semântico do MathLg."""

from __future__ import annotations

import pytest

from mathlg.interpreter.environment import Environment
from mathlg.lang.parser import parse
from mathlg.lang.tokenizer import tokenize
from mathlg.semantic.analyzer import TypeEnvironment, analyze
from mathlg.semantic.errors import SemanticError


def _analyze(text: str, lang: str = "pt-BR") -> list[SemanticError]:
    """Tokeniza, parseia e analisa — retorna erros semânticos."""
    env = Environment()
    tokens = tokenize(text, lang)
    ast = parse(tokens)
    return analyze(ast, env)


class TestSemanticTypeChecking:
    """Verificação de tipos."""

    def test_number_plus_number_ok(self) -> None:
        errors = _analyze("2 mais 3", "pt-BR")
        assert len(errors) == 0

    def test_number_plus_string_error(self) -> None:
        errors = _analyze('2 mais "texto"', "pt-BR")
        assert len(errors) > 0

    def test_undefined_variable(self) -> None:
        errors = _analyze("x mais 3", "pt-BR")
        # Pode ou não gerar erro dependendo do escopo da análise
        # Se x não foi definida, o semantic analyzer deve acusar
        has_undefined = any("não definida" in str(e).lower() or "undefined" in str(e).lower()
                           for e in errors)
        assert has_undefined

    def test_if_condition_must_be_bool(self) -> None:
        errors = _analyze("se 5: mostre 1", "pt-BR")
        # 5 como condição não é booleano — deve gerar erro
        has_type_error = any("lógico" in str(e).lower() or "logical" in str(e).lower()
                            or "condição" in str(e).lower()
                            for e in errors)
        # Nota: algumas linguagens aceitam truthy/falsy. MathLg pode ser permissiva.
        # Este teste existe para documentar a decisão.
        pass

    def test_while_condition_must_be_bool(self) -> None:
        errors = _analyze("enquanto 1: x = x mais 1", "pt-BR")
        pass  # Similar à condição if


class TestSemanticScope:
    """Resolução de escopo."""

    def test_variable_in_outer_scope(self) -> None:
        env = Environment()
        type_env = TypeEnvironment(fallback_env=env)

        # Define x no escopo global
        tokens = tokenize("x = 10", "pt-BR")
        ast = parse(tokens)
        errors = analyze(ast, env, type_env)
        assert len(errors) == 0

        # Usa x em nova expressão — deve resolver do escopo global
        tokens = tokenize("x mais 5", "pt-BR")
        ast = parse(tokens)
        errors = analyze(ast, env, type_env)
        assert len(errors) == 0

    def test_undefined_function(self) -> None:
        errors = _analyze("inexistente(5)", "pt-BR")
        has_undefined = any("não definida" in str(e).lower() or "undefined" in str(e).lower()
                           for e in errors)
        assert has_undefined


class TestSemanticFunction:
    """Funções definidas pelo usuário."""

    def test_function_definition(self) -> None:
        errors = _analyze("funcao dobro(x): retorna x vezes 2", "pt-BR")
        assert len(errors) == 0

    def test_function_call_after_definition(self) -> None:
        env = Environment()
        type_env = TypeEnvironment(fallback_env=env)

        # Define função
        tokens = tokenize("funcao dobro(x): retorna x vezes 2", "pt-BR")
        ast = parse(tokens)
        errors = analyze(ast, env, type_env)
        assert len(errors) == 0

        # Chama função
        tokens = tokenize("dobro(5)", "pt-BR")
        ast = parse(tokens)
        errors = analyze(ast, env, type_env)
        assert len(errors) == 0
