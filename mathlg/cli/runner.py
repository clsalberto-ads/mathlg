"""Runner de arquivos .mlg.

Carrega um arquivo, executa linha a linha no interpretador MathLg,
e opcionalmente exporta os resultados.
"""

from pathlib import Path

from mathlg.lang.tokenizer import tokenize
from mathlg.lang.parser import parse
from mathlg.semantic.analyzer import analyze
from mathlg.interpreter.evaluator import evaluate
from mathlg.interpreter.environment import Environment
from mathlg.i18n.manager import LangManager
from mathlg.semantic.errors import MathLgError
from mathlg.export.csv_exporter import export_csv
from mathlg.export.json_exporter import export_json


def run_file(
    filepath: str | Path,
    lang: str = "pt-BR",
    export: str | None = None,
) -> None:
    """Executa um arquivo .mlg.

    O arquivo é lido e cada linha não vazia é processada pelo pipeline
    completo: tokenize → parse → analyze → evaluate.

    Args:
        filepath: Caminho para o arquivo .mlg.
        lang: Idioma do código fonte (pt-BR ou en).
        export: Formato de exportação (csv, json, ou None).

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        MathLgError: Se houver erro de execução.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    if path.suffix not in (".mlg", ".txt", ""):
        print(f"Aviso: extensão incomum '{path.suffix}'. Esperado .mlg")

    lang_manager = LangManager(lang)
    env = Environment()
    resultados: list[dict] = []

    conteudo = path.read_text(encoding="utf-8")
    linhas = [linha.strip() for linha in conteudo.split("\n") if linha.strip()]

    for linha in linhas:
        # Pula comentários (linhas começando com #)
        if linha.startswith("#"):
            continue

        try:
            tokens = tokenize(linha, lang=lang_manager.current_lang)
            ast = parse(tokens)
            errors = analyze(ast, env)
            if errors:
                for err in errors:
                    print(f"Erro em '{linha}': {err}")
                continue

            resultado = evaluate(ast, env)
            if resultado is not None:
                print(resultado)
                resultados.append({
                    "expression": linha,
                    "result": str(resultado),
                    "lang": lang_manager.current_lang,
                })

        except MathLgError as e:
            print(f"Erro em '{linha}': {e}")

    if export and resultados:
        stem = path.stem
        if export == "csv":
            export_csv(resultados, f"{stem}.csv")
            print(f"Resultados exportados para: {stem}.csv")
        elif export == "json":
            export_json(resultados, f"{stem}.json")
            print(f"Resultados exportados para: {stem}.json")
