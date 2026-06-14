"""Exportador JSON para resultados do MathLg."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any


def export_json(data: list[dict[str, Any]], filepath: str) -> None:
    """Exporta resultados para arquivo JSON.

    O JSON inclui metadados: versão do MathLg, timestamp, e contagem.

    Args:
        data: Lista de dicionários com campos: expression, result, lang.
        filepath: Caminho do arquivo .json de saída.

    Raises:
        IOError: Se não for possível escrever o arquivo.

    Exemplos:
        >>> export_json([
        ...     {"expression": "2 + 2", "result": "4", "lang": "pt-BR"},
        ... ], "output.json")
    """
    from mathlg import __version__

    output = {
        "metadata": {
            "version": __version__,
            "timestamp": datetime.now().isoformat(),
            "count": len(data),
        },
        "results": data,
    }

    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
