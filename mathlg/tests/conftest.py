"""Fixtures compartilhadas para os testes do MathLg."""

from __future__ import annotations

import pytest

from mathlg.interpreter.environment import Environment
from mathlg.i18n.manager import LangManager
from mathlg.lang.tokens import Token, TokenType


@pytest.fixture
def env() -> Environment:
    """Ambiente limpo para cada teste."""
    return Environment()


@pytest.fixture
def lang_pt() -> LangManager:
    """Gerenciador de idioma em português."""
    return LangManager("pt-BR")


@pytest.fixture
def lang_en() -> LangManager:
    """Gerenciador de idioma em inglês."""
    return LangManager("en")


@pytest.fixture
def sample_tokens_pt() -> list[Token]:
    """Tokens de exemplo para testes de parser."""
    return [
        Token(type=TokenType.NUMBER, value=2),
        Token(type=TokenType.PLUS),
        Token(type=TokenType.NUMBER, value=3),
        Token(type=TokenType.EOF),
    ]


@pytest.fixture
def sample_tokens_complex_pt() -> list[Token]:
    """Tokens para expressão complexa."""
    return [
        Token(type=TokenType.SQRT),
        Token(type=TokenType.NUMBER, value=144),
        Token(type=TokenType.PLUS),
        Token(type=TokenType.NUMBER, value=3),
        Token(type=TokenType.EOF),
    ]
