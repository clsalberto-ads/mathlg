"""Definição de tokens da linguagem MathLg.

Todos os tokens são normalizados para inglês internamente.
O tokenizer faz a tradução do dicionário i18n para estes tokens.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    """Todos os tipos de token da linguagem MathLg.

    Nomenclatura em inglês porque é a representação interna.
    O i18n mapeia palavras em pt-BR ou EN para estes tokens.
    """

    # Palavras-chave de cálculo
    CALC = auto()       # "calcule" / "calculate"

    # Operadores binários
    PLUS = auto()       # "mais" / "plus"
    MINUS = auto()      # "menos" / "minus"
    TIMES = auto()      # "vezes" / "times"
    DIVIDE = auto()     # "dividido por" / "divided by"

    # Operadores unários / funções matemáticas
    SQRT = auto()       # "raiz quadrada de" / "square root of"
    POWER = auto()      # "potencia de ... elevado a" / "power of"
    SIN = auto()        # "seno de" / "sine of"
    COS = auto()        # "cosseno de" / "cosine of"
    LOG = auto()        # "logaritmo de" / "logarithm of"
    ABS = auto()        # "valor absoluto de" / "absolute value of"
    ROUND = auto()      # "arredondar" / "round"

    # Atribuição e variáveis
    ASSIGN = auto()     # "="
    IDENTIFIER = auto() # nome de variável

    # Funções definidas pelo usuário
    FN = auto()         # "funcao" / "function"
    RETURN = auto()     # "retorna" / "return"

    # Control flow
    IF = auto()         # "se" / "if"
    ELSE = auto()       # "senao" / "else"
    WHILE = auto()      # "enquanto" / "while"
    FOR = auto()        # "para" / "for"

    # Booleanos e comparação
    TRUE = auto()       # "verdadeiro" / "true"
    FALSE = auto()      # "falso" / "false"
    AND = auto()        # "e" / "and"
    OR = auto()         # "ou" / "or"
    NOT = auto()        # "nao" / "not"
    GT = auto()         # "maior que" / "greater than"
    LT = auto()         # "menor que" / "less than"
    EQ = auto()         # "igual a" / "equal to"
    GTE = auto()        # "maior ou igual a" / "greater or equal"
    LTE = auto()        # "menor ou igual a" / "less or equal"
    NEQ = auto()        # "diferente de" / "different from"

    # Literais
    NUMBER = auto()     # número (int ou float)
    STRING = auto()     # texto entre aspas
    LPAREN = auto()     # "("
    RPAREN = auto()     # ")"

    # Estrutura
    COMMA = auto()      # ","
    COLON = auto()      # ":" (para blocos)
    NEWLINE = auto()    # quebra de linha
    INDENT = auto()     # indentação (para blocos)

    # Export
    EXPORT = auto()     # "exportar" / "export"

    # Fim do arquivo
    EOF = auto()        # fim da entrada


@dataclass(frozen=True)
class Token:
    """Um token na stream de entrada.

    Attributes:
        type: Tipo do token (normalizado em inglês).
        value: Valor literal do token (ex: "3.14" para NUMBER,
               "x" para IDENTIFIER, None para keywords).
        span: Tupla (início, fim) da posição no texto original.
    """

    type: TokenType
    value: str | float | None = None
    span: tuple[int, int] | None = None

    def __repr__(self) -> str:
        if self.value is not None:
            return f"Token({self.type.name}, {self.value!r})"
        return f"Token({self.type.name})"
