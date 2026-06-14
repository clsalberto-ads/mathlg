"""Tokenizador do MathLg: texto em linguagem natural → stream de tokens.

A abordagem é pragmática:
  1. Tenta casar keywords (multi-palavra primeiro, depois simples)
  2. Tenta casar patterns (números, strings, símbolos)
  3. Trata resto como identificador ou erro

NÃO usamos spaCy, NLTK ou NLP library porque a gramática do MathLg
é controlada (semi-formal). Não é português livre.

A ORDEM IMPORTA: keywords multi-palavra ("raiz quadrada de", "dividido por")
são testadas ANTES de palavras individuais para evitar que "dividido" seja
tokenizado como IDENTIFIER antes de vermos "dividido por".
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from mathlg.lang.tokens import Token, TokenType
from mathlg.semantic.errors import LexerError

if TYPE_CHECKING:
    from mathlg.i18n.base import KeywordMap


# Patterns para coisas que NÃO são palavras-chave de linguagem natural.
# Números, strings, e símbolos:
PATTERNS: list[tuple[str, type | None]] = [
    # Comentários (descartados)
    (r"#.*", None),
    # Números: float antes de int para . casar "3.14" antes de "3"
    (r"\d+\.\d+", float),
    (r"\d+", int),
    # Strings com aspas
    (r'"[^"]*"', str),
    (r"'[^']*'", str),
    # Operadores simbólicos
    (r"==", str),  # IGUALDADE ANTES de ASSIGN simples
    (r"=", str),
    (r"\(", str),
    (r"\)", str),
    (r",", str),
    (r":", str),
    # Operadores simbólicos adicionais
    (r"\+", str),
    (r"\-", str),
    (r"\*", str),
    (r"/", str),
    (r">=", str),
    (r"<=", str),
    (r"!=", str),
    (r">", str),
    (r"<", str),
]


def tokenize(text: str, lang: str = "pt-BR") -> list[Token]:
    """Transforma texto em linguagem natural em uma lista de tokens.

    A ordem de matching é:
      1. Keywords multi-palavra (ordenadas da mais longa para a mais curta)
      2. Keywords de palavra única
      3. Patterns regex (números, strings, símbolos)
      4. Identificador genérico (se começar com letra/underscore)
      5. Erro (se nada casar)

    Args:
        text: A linha de comando em linguagem natural.
        lang: Idioma do texto ("pt-BR" ou "en").

    Returns:
        Lista de tokens normalizados.

    Raises:
        LexerError: Se encontrar um caractere não reconhecido.
    """
    from mathlg.i18n.manager import LangManager

    lang_manager = LangManager(lang)
    keyword_map = lang_manager.current_keywords

    # Keywords ordenadas da mais longa para a mais curta
    sorted_keywords = sorted(
        keyword_map.patterns.items(), key=lambda x: len(x[0]), reverse=True
    )

    tokens: list[Token] = []
    pos = 0

    while pos < len(text):
        # Pula espaços em branco
        if text[pos] in (" ", "\t", "\n"):
            pos += 1
            continue

        # 1. Tenta keywords (multi-palavra testadas primeiro)
        keyword_match = _try_match_keyword(text, pos, sorted_keywords)
        if keyword_match is not None:
            token_type, end_pos = keyword_match
            # Armazena o texto original da keyword no token (útil para
            # quando keywords como "e" (AND) viram nome de parâmetro)
            raw_text = text[pos:end_pos]
            tokens.append(Token(type=token_type, value=raw_text, span=(pos, end_pos)))
            pos = end_pos
            continue

        # 2. Tenta patterns (números, strings, símbolos)
        pattern_match = _match_pattern(text, pos)
        if pattern_match is not None:
            raw_value, value_type, end_pos = pattern_match
            token = _process_match(raw_value, value_type, keyword_map, pos, end_pos)
            if token is not None:
                tokens.append(token)
            pos = end_pos
            continue

        # 3. Tenta identificador (Unicode-aware: suporta ç, ã, ê etc.)
        ident_match = _match_identifier(text, pos)
        if ident_match is not None:
            raw_value, end_pos = ident_match
            lower_val = raw_value.lower()

            # Verifica se é keyword de palavra única
            if lower_val in keyword_map.patterns:
                tokens.append(
                    Token(type=keyword_map.patterns[lower_val], span=(pos, end_pos))
                )
            else:
                tokens.append(
                    Token(type=TokenType.IDENTIFIER, value=raw_value, span=(pos, end_pos))
                )
            pos = end_pos
            continue

        # 4. Nada casou → erro
        raise LexerError(
            f"Caractere não reconhecido: {text[pos]!r} na posição {pos}",
            text=text,
            pos=pos,
        )

    tokens.append(Token(type=TokenType.EOF, span=(len(text), len(text))))
    return tokens


def _try_match_keyword(
    text: str, pos: int, sorted_keywords: list[tuple[str, TokenType]]
) -> tuple[TokenType, int] | None:
    """Tenta casar keywords (mais longas primeiro) na posição atual.

    A verificação de fim de palavra garante que "raiz" não case
    parcialmente com "raiz quadrada de" quando na verdade é "raizeira".
    """
    remaining = text[pos:].lower()

    for keyword_text, token_type in sorted_keywords:
        if remaining.startswith(keyword_text):
            next_pos = pos + len(keyword_text)
            # Garante que a keyword terminou em boundary de palavra
            if next_pos >= len(text) or text[next_pos] in (
                " ", "\t", "\n", ")", "(", ",", ":", "'", '"'
            ):
                return (token_type, next_pos)

    return None


def _match_pattern(
    text: str, pos: int
) -> tuple[str, type | None, int] | None:
    """Tenta casar um pattern regex (número, string, símbolo)."""
    for pattern, value_type in PATTERNS:
        m = re.match(pattern, text[pos:])
        if m:
            return (m.group(0), value_type, pos + m.end())
    return None


def _match_identifier(
    text: str, pos: int
) -> tuple[str, int] | None:
    """Tenta casar um identificador (Unicode-aware).

    Aceita letras Unicode (incluindo acentos, ç, ñ), dígitos e underscore.
    NÃO pode começar com dígito (isso já foi capturado por NUMBER).
    """
    m = re.match(r"[^\W\d_](\w|')*", text[pos:], re.UNICODE)
    if m:
        return (m.group(0), pos + m.end())
    return None


def _process_match(
    raw_value: str,
    value_type: type | None,
    keyword_map: "KeywordMap",
    start_pos: int,
    end_pos: int,
) -> Token | None:
    """Processa um match de pattern e retorna o token."""
    # Comentários descartados
    if value_type is None:
        return None

    # Números
    if value_type in (int, float):
        val = float(raw_value) if value_type is float else int(raw_value)
        return Token(type=TokenType.NUMBER, value=val, span=(start_pos, end_pos))

    # Strings literais
    if value_type is str and raw_value.startswith(('"', "'")):
        return Token(
            type=TokenType.STRING,
            value=raw_value[1:-1],
            span=(start_pos, end_pos),
        )

    # Símbolos
    if value_type is str:
        symbol_map = {
            "=": TokenType.ASSIGN,
            "==": TokenType.EQ,  # IGUALDADE (comparação)
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            ",": TokenType.COMMA,
            ":": TokenType.COLON,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.TIMES,
            "/": TokenType.DIVIDE,
            ">": TokenType.GT,
            "<": TokenType.LT,
            ">=": TokenType.GTE,
            "<=": TokenType.LTE,
            "!=": TokenType.NEQ,
        }
        if raw_value in symbol_map:
            return Token(type=symbol_map[raw_value], span=(start_pos, end_pos))

    return None
