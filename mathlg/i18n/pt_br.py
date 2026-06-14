"""Dicionário de keywords em português brasileiro para o MathLg.

Mapeia expressões em linguagem natural (português) para os tokens
normalizados (sempre em inglês) que o parser entende.
"""

from mathlg.i18n.base import KeywordMap
from mathlg.lang.tokens import TokenType


def create_pt_br_keywords() -> KeywordMap:
    """Cria e retorna o dicionário de keywords em português brasileiro.

    Returns:
        KeywordMap configurado com palavras e expressões em pt-BR.
    """
    km = KeywordMap(name="pt-BR")

    km.extend({
        # Comandos
        "calcule": TokenType.CALC,
        "calcular": TokenType.CALC,
        "calcula": TokenType.CALC,
        "mostre": TokenType.CALC,
        "mostrar": TokenType.CALC,

        # Operadores básicos
        "mais": TokenType.PLUS,
        "menos": TokenType.MINUS,
        "vezes": TokenType.TIMES,
        "multiplicado por": TokenType.TIMES,
        "dividido por": TokenType.DIVIDE,
        "dividido": TokenType.DIVIDE,

        # Funções matemáticas
        "raiz quadrada de": TokenType.SQRT,
        "raiz quadrada": TokenType.SQRT,
        "raiz": TokenType.SQRT,
        "potencia de": TokenType.POWER,
        "elevado a": TokenType.POWER,
        "seno de": TokenType.SIN,
        "seno": TokenType.SIN,
        "cosseno de": TokenType.COS,
        "cosseno": TokenType.COS,
        "logaritmo de": TokenType.LOG,
        "logaritmo natural de": TokenType.LOG,
        "log de": TokenType.LOG,
        "log": TokenType.LOG,
        "valor absoluto de": TokenType.ABS,
        "valor absoluto": TokenType.ABS,
        "arredondar": TokenType.ROUND,

        # Booleanos
        "verdadeiro": TokenType.TRUE,
        "falso": TokenType.FALSE,
        "verdade": TokenType.TRUE,
        "e": TokenType.AND,
        "ou": TokenType.OR,
        "nao": TokenType.NOT,

        # Comparação
        "maior que": TokenType.GT,
        "maior": TokenType.GT,
        "menor que": TokenType.LT,
        "menor": TokenType.LT,
        "igual a": TokenType.EQ,
        "igual": TokenType.EQ,
        "maior ou igual a": TokenType.GTE,
        "maior ou igual": TokenType.GTE,
        "menor ou igual a": TokenType.LTE,
        "menor ou igual": TokenType.LTE,
        "diferente de": TokenType.NEQ,
        "diferente": TokenType.NEQ,

        # Control flow
        "se": TokenType.IF,
        "senao": TokenType.ELSE,
        "enquanto": TokenType.WHILE,
        "para": TokenType.FOR,
        "ate": TokenType.FOR,

        # Funções
        "funcao": TokenType.FN,
        "retorna": TokenType.RETURN,

        # Export
        "exportar": TokenType.EXPORT,
        "exporta": TokenType.EXPORT,
    })

    return km
