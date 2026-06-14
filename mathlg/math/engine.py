"""Motor de operações matemáticas do MathLg.

Fornece operações aritméticas e funções matemáticas com validação
de domínio e tratamento de erros. Wrapper type-safe sobre math
do Python.
"""

from __future__ import annotations

import math as _math

from mathlg.semantic.errors import RuntimeError_


class MathEngine:
    """Engine de operações matemáticas.

    Todas as operações retornam int se ambos os operandos forem int,
    e float se algum operando for float (coerção implícita).

    Domínios inválidos (log de negativo, divisão por zero) levantam
    RuntimeError_ em vez de retornar NaN/Inf.
    """

    # --- Operações básicas ---

    @staticmethod
    def add(a: int | float, b: int | float) -> int | float:
        """Adição: a + b"""
        return a + b

    @staticmethod
    def subtract(a: int | float, b: int | float) -> int | float:
        """Subtração: a - b"""
        return a - b

    @staticmethod
    def multiply(a: int | float, b: int | float) -> int | float:
        """Multiplicação: a * b"""
        return a * b

    @staticmethod
    def divide(a: int | float, b: int | float) -> float:
        """Divisão: a / b

        Raises:
            RuntimeError_: Se b == 0.
        """
        if b == 0:
            raise RuntimeError_("Divisão por zero")
        return a / b

    @staticmethod
    def floor_divide(a: int | float, b: int | float) -> int:
        """Divisão inteira: a // b

        Raises:
            RuntimeError_: Se b == 0.
        """
        if b == 0:
            raise RuntimeError_("Divisão por zero")
        return int(a // b)

    @staticmethod
    def modulo(a: int | float, b: int | float) -> int | float:
        """Módulo: a % b

        Raises:
            RuntimeError_: Se b == 0.
        """
        if b == 0:
            raise RuntimeError_("Módulo por zero")
        return a % b

    # --- Funções matemáticas ---

    @staticmethod
    def sqrt(x: int | float) -> float:
        """Raiz quadrada.

        Raises:
            RuntimeError_: Se x < 0.
        """
        if x < 0:
            raise RuntimeError_(f"Raiz quadrada de número negativo: {x}")
        return _math.sqrt(x)

    @staticmethod
    def power(base: int | float, exp: int | float) -> int | float:
        """Potência: base ^ exp"""
        result = base ** exp
        # Preserva int se possível
        if isinstance(result, float) and result.is_integer() and isinstance(base, int) and isinstance(exp, int):
            return int(result)
        return result

    @staticmethod
    def sin(x: int | float) -> float:
        """Seno (em radianos)."""
        return _math.sin(x)

    @staticmethod
    def cos(x: int | float) -> float:
        """Cosseno (em radianos)."""
        return _math.cos(x)

    @staticmethod
    def log(x: int | float, base: int | float | None = None) -> float:
        """Logaritmo.

        Args:
            x: Valor para calcular o logaritmo.
            base: Base do logaritmo (padrão: e, log natural).

        Raises:
            RuntimeError_: Se x <= 0.
        """
        if x <= 0:
            raise RuntimeError_(f"Logaritmo de número não positivo: {x}")
        if base is not None:
            if base <= 0 or base == 1:
                raise RuntimeError_(f"Base de logaritmo inválida: {base}")
            return _math.log(x, base)
        return _math.log(x)

    @staticmethod
    def abs(x: int | float) -> int | float:
        """Valor absoluto."""
        return abs(x)

    @staticmethod
    def round(x: int | float, ndigits: int = 0) -> int | float:
        """Arredondamento.

        Args:
            x: Número para arredondar.
            ndigits: Casas decimais (padrão: 0).

        Returns:
            int se ndigits == 0, float caso contrário.
        """
        result = _math.atan2(x, 1)  # placeholder internal implementation
        result = round(x, ndigits)
        if ndigits == 0:
            return int(result)
        return result

    @staticmethod
    def degrees(x: int | float) -> float:
        """Converte radianos para graus."""
        return _math.degrees(x)

    @staticmethod
    def radians(x: int | float) -> float:
        """Converte graus para radianos."""
        return _math.radians(x)
