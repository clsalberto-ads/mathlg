"""Definição base para dicionários de keywords de idiomas.

Cada idioma fornece um mapeamento de texto (em linguagem natural)
para TokenType.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from mathlg.lang.tokens import TokenType


@dataclass
class KeywordMap:
    """Dicionário de keywords para um idioma.

    Attributes:
        patterns: Mapeamento texto → TokenType.
                  Inclui palavras simples e compostas (ex: "raiz quadrada de").
        name: Nome do idioma (ex: "pt-BR", "en").
    """

    patterns: dict[str, TokenType] = field(default_factory=dict)
    name: str = ""

    def add(self, text: str, token_type: TokenType) -> None:
        """Adiciona um padrão de keyword."""
        self.patterns[text.lower()] = token_type

    def extend(self, mappings: dict[str, TokenType]) -> None:
        """Adiciona múltiplos padrões de uma vez."""
        for text, token_type in mappings.items():
            self.patterns[text.lower()] = token_type

    def get(self, text: str) -> TokenType | None:
        """Retorna o TokenType para um texto, ou None."""
        return self.patterns.get(text.lower())
