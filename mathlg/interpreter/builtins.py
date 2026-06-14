"""Funções embutidas (built-in) da linguagem MathLg.

Fornece funções acessíveis ao usuário sem definição explícita.
"""

from __future__ import annotations

from typing import Any


def builtin_print(*args: Any, **kwargs: Any) -> None:
    """Imprime valores no console. Mapeia 'mostre' / 'print'."""
    print(*args, **kwargs)


def builtin_type_of(value: Any) -> str:
    """Retorna o nome do tipo de um valor.

    >>> builtin_type_of(42)
    'inteiro'
    >>> builtin_type_of(3.14)
    'decimal'
    >>> builtin_type_of("texto")
    'texto'
    """
    from mathlg.math.types import MathLgType
    return MathLgType.infer(value).name.lower()


# Tabela de funções embutidas: nome → (função, número_min_args, número_max_args)
BUILTINS: dict[str, tuple[Any, int, int | None]] = {
    "mostre": (builtin_print, 1, None),
    "print": (builtin_print, 1, None),
    "tipo": (builtin_type_of, 1, 1),
    "type": (builtin_type_of, 1, 1),
}
