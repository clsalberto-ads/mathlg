"""Interface base para exportadores."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Exporter(ABC):
    """Classe base para formatos de exportação."""

    @abstractmethod
    def export(self, data: list[dict[str, Any]], filepath: str) -> None:
        """Exporta dados para um arquivo.

        Args:
            data: Lista de dicionários com os dados.
            filepath: Caminho do arquivo de saída.
        """
        ...
