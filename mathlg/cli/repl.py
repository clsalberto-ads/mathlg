"""REPL interativo: loop read-eval-print para MathLg.

MVP usa input() puro. Sem prompt_toolkit por enquanto.
Se histórico entre sessões ou autocomplete forem necessários,
substituir o loop por prompt_toolkit é uma troca limpa.
"""

import sys

from mathlg.lang.tokenizer import tokenize
from mathlg.lang.parser import parse
from mathlg.semantic.analyzer import analyze
from mathlg.interpreter.evaluator import evaluate
from mathlg.interpreter.environment import Environment
from mathlg.i18n.manager import LangManager
from mathlg.export.csv_exporter import export_csv
from mathlg.export.json_exporter import export_json
from mathlg.semantic.errors import MathLgError


def run_repl(lang: str = "pt-BR", export: str | None = None) -> None:
    """Inicia o loop REPL interativo.

    Aceita comandos linha a linha. Comandos especiais:
        /idioma <lang>  — troca idioma em runtime
        /export <fmt>   — define formato de exportação
        /ajuda          — mostra ajuda rápida
        sair / exit     — encerra

    Args:
        lang: Idioma inicial (pt-BR ou en).
        export: Formato de exportação (csv, json, ou None).
    """
    lang_manager = LangManager(lang)
    env = Environment()
    resultados: list[dict] = []

    boas_vindas = (
        "MathLg v0.1 — Digite 'sair' para encerrar"
        if lang == "pt-BR"
        else "MathLg v0.1 — Type 'exit' to quit"
    )
    print(boas_vindas)

    while True:
        try:
            linha = input("mlg> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not linha:
            continue

        # Comandos internos do REPL (começam com /)
        if linha.startswith("/"):
            _handle_repl_command(linha, lang_manager)
            continue

        # Comandos de saída
        if linha.lower() in ("sair", "exit", "quit"):
            break

        try:
            # Pipeline completo
            tokens = tokenize(linha, lang=lang_manager.current_lang)
            ast = parse(tokens)
            errors = analyze(ast, env)
            if errors:
                for err in errors:
                    print(f"Erro: {err}")
                continue

            resultado = evaluate(ast, env)

            if resultado is not None:
                print(resultado)

                # Acumula para exportação
                resultados.append({
                    "expression": linha,
                    "result": str(resultado),
                    "lang": lang_manager.current_lang,
                })

        except MathLgError as e:
            print(f"Erro: {e}")
        except Exception as e:
            print(f"Erro interno: {e}")

    # Exporta se solicitado
    if export and resultados:
        _export_resultados(resultados, export)


def _handle_repl_command(comando: str, lang_manager: LangManager) -> None:
    """Processa comandos internos do REPL."""
    partes = comando.lower().split()

    if partes[0] == "/idioma" or partes[0] == "/language":
        if len(partes) > 1:
            lang_manager.set_lang(partes[1])
            print(f"Idioma alterado para: {lang_manager.current_lang}")
        else:
            print(f"Idioma atual: {lang_manager.current_lang}")

    elif partes[0] == "/ajuda" or partes[0] == "/help":
        _show_help(lang_manager.current_lang)

    else:
        print(f"Comando desconhecido: {comando}")


def _show_help(lang: str) -> None:
    """Exibe ajuda rápida no REPL."""
    if lang == "pt-BR":
        print("""
Comandos MathLg:
  calcular <expressão>         — Executa uma expressão matemática
  <var> = <expressão>          — Atribui valor a uma variável
  funcao <nome>(<params>)      — Define uma funcao
  se <cond> ... senao ...      — Condicional
  enquanto <cond> ...          — Loop
  exportar csv/json             — Exporta resultados

Operações: mais, menos, vezes, dividido por, raiz quadrada de,
           potencia de, seno de, cosseno de, logaritmo de

Comandos REPL:
  /idioma <lang>  — Troca idioma
  /ajuda           — Esta ajuda
  sair             — Encerra
""")
    else:
        print("""
MathLg Commands:
  calculate <expression>       — Evaluate a math expression
  <var> = <expression>         — Assign to variable
  function <name>(<params>)    — Define a function
  if <cond> ... else ...       — Conditional
  while <cond> ...             — Loop
  export csv/json               — Export results

Operators: plus, minus, times, divided by, square root of,
           power of, sine of, cosine of, logarithm of

REPL Commands:
  /language <lang>  — Switch language
  /help             — This help
  exit              — Quit
""")


def _export_resultados(resultados: list[dict], formato: str) -> None:
    """Exporta resultados acumulados."""
    if formato == "csv":
        export_csv(resultados, "resultados.csv")
        print(f"Resultados exportados para: resultados.csv")
    elif formato == "json":
        export_json(resultados, "resultados.json")
        print(f"Resultados exportados para: resultados.json")
