"""Entrypoint: python -m mathlg [arquivo.mlg] [opções]."""

import sys
from mathlg.cli.config import parse_args
from mathlg.cli.repl import run_repl
from mathlg.cli.runner import run_file


def main() -> None:
    """Ponto de entrada da CLI. Decide entre REPL ou execução de arquivo."""
    args = parse_args()

    if args.file:
        run_file(args.file, lang=args.lang, export=args.export)
    else:
        run_repl(lang=args.lang, export=args.export)


if __name__ == "__main__":
    main()
