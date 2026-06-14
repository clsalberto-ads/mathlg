"""Testes do tokenizador do MathLg.

Categorias de teste:
    1. Operações básicas em pt-BR
    2. Operações básicas em EN
    3. Funções matemáticas
    4. Atribuição de variáveis
    5. Números (int, float, negativos)
    6. Strings
    7. Booleanos
    8. Comparação
    9. Edge cases (string vazia, números grandes, palavras desconhecidas)
"""

from __future__ import annotations

import pytest

from mathlg.lang.tokenizer import tokenize
from mathlg.lang.tokens import TokenType
from mathlg.semantic.errors import LexerError


class TestTokenizerBasicPt:
    """Testes de tokenização básica em português."""

    def test_simple_addition(self) -> None:
        tokens = tokenize("2 mais 3", "pt-BR")
        types = [t.type for t in tokens]
        assert types == [TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER, TokenType.EOF]

    def test_simple_subtraction(self) -> None:
        tokens = tokenize("10 menos 4", "pt-BR")
        types = [t.type for t in tokens]
        assert types == [TokenType.NUMBER, TokenType.MINUS, TokenType.NUMBER, TokenType.EOF]

    def test_simple_multiplication(self) -> None:
        tokens = tokenize("7 vezes 6", "pt-BR")
        types = [t.type for t in tokens]
        assert types == [TokenType.NUMBER, TokenType.TIMES, TokenType.NUMBER, TokenType.EOF]

    def test_simple_division(self) -> None:
        tokens = tokenize("20 dividido por 4", "pt-BR")
        types = [t.type for t in tokens]
        assert types == [TokenType.NUMBER, TokenType.DIVIDE, TokenType.NUMBER, TokenType.EOF]

    def test_number_values(self) -> None:
        tokens = tokenize("42 mais 3.14", "pt-BR")
        assert tokens[0].value == 42
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[2].value == 3.14
        assert tokens[2].type == TokenType.NUMBER


class TestTokenizerBasicEn:
    """Testes de tokenização básica em inglês."""

    def test_simple_addition(self) -> None:
        tokens = tokenize("2 plus 3", "en")
        types = [t.type for t in tokens]
        assert types == [TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER, TokenType.EOF]

    def test_keyword_variations(self) -> None:
        tokens = tokenize("5 times 3", "en")
        assert tokens[1].type == TokenType.TIMES

        tokens = tokenize("5 multiplied by 3", "en")
        assert tokens[1].type == TokenType.TIMES

    def test_calculate_keyword(self) -> None:
        tokens = tokenize("calculate 10 plus 20", "en")
        assert tokens[0].type == TokenType.CALC


class TestTokenizerMathFunctions:
    """Testes de funções matemáticas."""

    def test_sqrt_pt(self) -> None:
        tokens = tokenize("raiz quadrada de 144", "pt-BR")
        assert tokens[0].type == TokenType.SQRT
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].value == 144

    def test_sqrt_en(self) -> None:
        tokens = tokenize("square root of 144", "en")
        assert tokens[0].type == TokenType.SQRT
        assert tokens[1].type == TokenType.NUMBER

    def test_sin_pt(self) -> None:
        tokens = tokenize("seno de 0", "pt-BR")
        assert tokens[0].type == TokenType.SIN
        assert tokens[1].type == TokenType.NUMBER

    def test_cos_en(self) -> None:
        tokens = tokenize("cosine of 0", "en")
        assert tokens[0].type == TokenType.COS
        assert tokens[1].type == TokenType.NUMBER

    def test_power_pt(self) -> None:
        tokens = tokenize("potencia de 2 elevado a 3", "pt-BR")
        assert tokens[0].type == TokenType.POWER
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].value == 2
        assert tokens[2].type == TokenType.POWER
        assert tokens[3].type == TokenType.NUMBER
        assert tokens[3].value == 3

    def test_log_pt(self) -> None:
        tokens = tokenize("logaritmo de 100", "pt-BR")
        assert tokens[0].type == TokenType.LOG
        assert tokens[1].type == TokenType.NUMBER
        assert tokens[1].value == 100


class TestTokenizerVariables:
    """Testes de atribuição e variáveis."""

    def test_assignment(self) -> None:
        tokens = tokenize("x = 10", "pt-BR")
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "x"
        assert tokens[1].type == TokenType.ASSIGN
        assert tokens[2].type == TokenType.NUMBER
        assert tokens[2].value == 10

    def test_variable_name(self) -> None:
        tokens = tokenize("resultado = 42", "pt-BR")
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "resultado"

    def test_variable_usage(self) -> None:
        tokens = tokenize("x mais y", "pt-BR")
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == "x"
        assert tokens[1].type == TokenType.PLUS
        assert tokens[2].type == TokenType.IDENTIFIER
        assert tokens[2].value == "y"


class TestTokenizerEdgeCases:
    """Testes de edge cases do tokenizador."""

    def test_empty_string(self) -> None:
        tokens = tokenize("", "pt-BR")
        assert tokens == [tokens[-1]] or len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_float_numbers(self) -> None:
        tokens = tokenize("3.14159", "pt-BR")
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 3.14159

    def test_multiple_spaces(self) -> None:
        tokens = tokenize("2   plus   3", "en")
        assert len(tokens) == 4  # NUMBER, PLUS, NUMBER, EOF

    def test_comment(self) -> None:
        tokens = tokenize("2 mais 3 # isso é um comentário", "pt-BR")
        types = [t.type for t in tokens]
        assert types == [TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER, TokenType.EOF]

    def test_invalid_character(self) -> None:
        with pytest.raises(LexerError):
            tokenize("2 @ 3", "pt-BR")

    def test_symbol_plus(self) -> None:
        tokens = tokenize("2+3", "en")
        types = [t.type for t in tokens]
        assert types[:3] == [TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER]

    def test_symbol_minus(self) -> None:
        tokens = tokenize("2 - 3", "en")
        types = [t.type for t in tokens]
        assert types[:3] == [TokenType.NUMBER, TokenType.MINUS, TokenType.NUMBER]

    def test_symbol_greater(self) -> None:
        tokens = tokenize("2 > 3", "en")
        assert tokens[1].type == TokenType.GT

    def test_string_literal_double(self) -> None:
        tokens = tokenize('"hello"', "en")
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello"

    def test_string_literal_single(self) -> None:
        tokens = tokenize("'texto'", "pt-BR")
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "texto"


class TestTokenizerBooleans:
    """Testes de booleanos."""

    def test_true_pt(self) -> None:
        tokens = tokenize("verdadeiro", "pt-BR")
        assert tokens[0].type == TokenType.TRUE

    def test_false_pt(self) -> None:
        tokens = tokenize("falso", "pt-BR")
        assert tokens[0].type == TokenType.FALSE

    def test_true_en(self) -> None:
        tokens = tokenize("true", "en")
        assert tokens[0].type == TokenType.TRUE


class TestTokenizerComparison:
    """Testes de operadores de comparação."""

    def test_greater_pt(self) -> None:
        tokens = tokenize("10 maior que 5", "pt-BR")
        assert tokens[1].type == TokenType.GT
        assert tokens[2].type == TokenType.NUMBER
        assert tokens[2].value == 5

    def test_less_en(self) -> None:
        tokens = tokenize("3 less than 10", "en")
        assert tokens[1].type == TokenType.LT

    def test_equal_pt(self) -> None:
        tokens = tokenize("x igual a 10", "pt-BR")
        assert tokens[1].type == TokenType.EQ
