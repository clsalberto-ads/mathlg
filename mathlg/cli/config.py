"""Configuração da CLI via argparse."""

import argparse
import sys
from typing import NamedTuple


class CliArgs(NamedTuple):
    """Argumentos parseados da linha de comando."""

    file: str | None
    lang: str
    export: str | None


def parse_args(argv: list[str] | None = None) -> CliArgs:
    """Parseia argumentos da linha de comando.

    Suporta:
        python -m mathlg                       → REPL modo português
        python -m mathlg script.mlg            → executa arquivo
        python -m mathlg --lang en             → REPL modo inglês
        python -m mathlg script.mlg --export json
        python -m mathlg --help
    """
    parser = argparse.ArgumentParser(
        prog="mathlg",
        description="MathLg — Linguagem de programação matemática em linguagem natural",
        epilog="Exemplo: python -m mathlg exemplo.mlg --lang pt-BR --export json",
    )

    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Arquivo .mlg para executar (omita para entrar no REPL)",
    )

    parser.add_argument(
        "--lang",
        default="pt-BR",
        choices=["pt-BR", "en"],
        help="Idioma da interface (pt-BR ou en)",
    )

    parser.add_argument(
        "--export",
        default=None,
        choices=["csv", "json"],
        help="Formato de exportação dos resultados",
    )

    parsed = parser.parse_args(argv)

    return CliArgs(file=parsed.file, lang=parsed.lang, export=parsed.export)
