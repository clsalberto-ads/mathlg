"""Exportador CSV para resultados do MathLg."""

from __future__ import annotations

import csv
from typing import Any


def export_csv(data: list[dict[str, Any]], filepath: str) -> None:
    """Exporta resultados para arquivo CSV.

    Args:
        data: Lista de dicionários com campos: expression, result, lang.
        filepath: Caminho do arquivo .csv de saída.

    Raises:
        IOError: Se não for possível escrever o arquivo.

    Exemplos:
        >>> export_csv([
        ...     {"expression": "2 + 2", "result": "4", "lang": "pt-BR"},
        ...     {"expression": "sqrt 144", "result": "12.0", "lang": "pt-BR"},
        ... ], "output.csv")
    """
    if not data:
        return

    fieldnames = list(data[0].keys())

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
