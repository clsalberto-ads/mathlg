"""Gerenciador de internacionalização (i18n) do MathLg.

Singleton que gerencia o idioma atual e fornece os dicionários de
keywords para o tokenizer.

A troca de idioma é feita em runtime (/idioma ingles no REPL).
"""

from __future__ import annotations

from mathlg.i18n.base import KeywordMap
from mathlg.i18n.pt_br import create_pt_br_keywords
from mathlg.i18n.en import create_en_keywords


# Cache de dicionários (criados uma vez)
_KEYWORD_MAPS: dict[str, KeywordMap] = {
    "pt-BR": create_pt_br_keywords(),
    "en": create_en_keywords(),
}


class LangManager:
    """Gerenciador de idioma do MathLg.

    Usage:
        >>> mgr = LangManager("pt-BR")
        >>> mgr.current_lang
        'pt-BR'
        >>> mgr.current_keywords  # KeywordMap com palavras em pt-BR
        >>> mgr.set_lang("en")
        >>> mgr.current_lang
        'en'
    """

    _global_instance: LangManager | None = None

    def __init__(self, lang: str = "pt-BR") -> None:
        if lang not in _KEYWORD_MAPS:
            available = ", ".join(_KEYWORD_MAPS.keys())
            raise ValueError(f"Idioma não suportado: '{lang}'. Disponíveis: {available}")

        self._lang = lang
        # Configura instância global na primeira criação
        if LangManager._global_instance is None:
            LangManager._global_instance = self

    @property
    def current_lang(self) -> str:
        """Idioma atual."""
        return self._lang

    @property
    def current_keywords(self) -> KeywordMap:
        """Dicionário de keywords do idioma atual."""
        return _KEYWORD_MAPS[self._lang]

    def set_lang(self, lang: str) -> None:
        """Troca o idioma atual.

        Args:
            lang: Código do idioma ("pt-BR" ou "en").

        Raises:
            ValueError: Se o idioma não for suportado.
        """
        if lang not in _KEYWORD_MAPS:
            available = ", ".join(_KEYWORD_MAPS.keys())
            raise ValueError(f"Idioma não suportado: '{lang}'. Disponíveis: {available}")
        self._lang = lang

    @classmethod
    def get_instance(cls) -> LangManager:
        """Retorna a instância global do LangManager.

        Raises:
            RuntimeError: Se nenhuma instância foi criada ainda.
        """
        if cls._global_instance is None:
            cls._global_instance = cls()
        return cls._global_instance

    @classmethod
    def supported_languages(cls) -> list[str]:
        """Retorna lista de idiomas suportados."""
        return list(_KEYWORD_MAPS.keys())
