"""Hierarquia de erros do MathLg.

Toda exceção levantada pela linguagem herda de MathLgError.
Isso permite que o REPL e o runner capturem erros da linguagem
separadamente de erros do Python.
"""

from __future__ import annotations


class MathLgError(Exception):
    """Classe base para todos os erros da linguagem MathLg."""

    def __init__(self, message: str, **context: object) -> None:
        self.message = message
        self.context = context
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        if self.context:
            ctx = ", ".join(f"{k}={v!r}" for k, v in self.context.items())
            return f"{self.message} [{ctx}]"
        return self.message


class LexerError(MathLgError):
    """Erro de tokenização: caractere não reconhecido, padrão inválido."""

    def __init__(
        self,
        message: str,
        text: str | None = None,
        pos: int | None = None,
    ) -> None:
        ctx: dict[str, object] = {}
        if text is not None and pos is not None:
            ctx["context"] = text[max(0, pos - 10):pos + 10]
            ctx["pos"] = pos
        super().__init__(message, **ctx)


class ParserError(MathLgError):
    """Erro de sintaxe: expressão mal formada, token inesperado."""


class SemanticError(MathLgError):
    """Erro semântico: tipo incompatível, variável não definida, escopo."""


class RuntimeError_(MathLgError):
    """Erro em tempo de execução: divisão por zero, domínio inválido.

    Nome com underline para não colidir com builtin RuntimeError.
    """
