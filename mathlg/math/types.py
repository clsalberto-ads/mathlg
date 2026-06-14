"""Sistema de tipos do MathLg.

Tipos suportados no MVP:
    - INTEGER: números inteiros (int)
    - DECIMAL: números de ponto flutuante (float)
    - TEXT: strings
    - LOGICAL: booleanos (bool)
    - NULL: ausência de valor (None)
    - FUNCTION: função (callable, apenas para type checking)

O sistema é estático simplificado: tipos são verificados em tempo de
análise semântica, mas o evaluador pode fazer coerções implícitas
(ex: int + float → float).
"""

from __future__ import annotations

from enum import Enum, auto
from typing import Any


class MathLgType(Enum):
    """Tipos da linguagem MathLg."""

    INTEGER = auto()    # int
    DECIMAL = auto()    # float
    TEXT = auto()       # str
    LOGICAL = auto()    # bool
    NULL = auto()       # None
    FUNCTION = auto()   # callable (tipos de função)

    def __str__(self) -> str:
        return self.name.lower()

    def __repr__(self) -> str:
        return f"MathLgType.{self.name}"

    @staticmethod
    def infer(value: Any) -> MathLgType:
        """Infere o tipo MathLg a partir de um valor Python.

        Args:
            value: Valor Python para inferir o tipo.

        Returns:
            Tipo MathLg correspondente.

        Examples:
            >>> MathLgType.infer(42)
            <MathLgType.INTEGER: ...>
            >>> MathLgType.infer(3.14)
            <MathLgType.DECIMAL: ...>
            >>> MathLgType.infer("hello")
            <MathLgType.TEXT: ...>
            >>> MathLgType.infer(True)
            <MathLgType.LOGICAL: ...>
            >>> MathLgType.infer(None)
            <MathLgType.NULL: ...>
        """
        if isinstance(value, bool):
            return MathLgType.LOGICAL
        if isinstance(value, int):
            return MathLgType.INTEGER
        if isinstance(value, float):
            return MathLgType.DECIMAL
        if isinstance(value, str):
            return MathLgType.TEXT
        if value is None:
            return MathLgType.NULL
        return MathLgType.NULL  # fallback
