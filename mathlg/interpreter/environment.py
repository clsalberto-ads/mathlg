"""Ambiente (escopo) do MathLg.

Gerencia variáveis, funções e seus valores em escopos aninhados.
Suporta escopo léxico (estático) através de encadeamento de ambientes.
"""

from __future__ import annotations

from typing import Any

from mathlg.math.types import MathLgType


class Environment:
    """Um escopo de execução do MathLg.

    Cada Environment tem um dicionário de variáveis e uma referência
    ao escopo externo (outer). A resolução de nomes sobe a cadeia
    até encontrar a definição.

    Attributes:
        store: Mapeamento nome → (valor, tipo).
        outer: Escopo externo (None para escopo global).
    """

    def __init__(self, outer: Environment | None = None) -> None:
        self.store: dict[str, tuple[Any, MathLgType]] = {}
        self.outer = outer

    def define(self, name: str, value: Any, type_: MathLgType | None = None) -> None:
        """Define uma variável no escopo atual.

        Args:
            name: Nome da variável.
            value: Valor inicial.
            type_: Tipo MathLg (opcional — inferido do valor se omitido).
        """
        if type_ is None:
            type_ = MathLgType.infer(value)
        self.store[name] = (value, type_)

    def resolve(self, name: str) -> MathLgType | None:
        """Resolve o tipo de uma variável, subindo a cadeia de escopos.

        Args:
            name: Nome da variável.

        Returns:
            Tipo MathLg da variável, ou None se não encontrada.
        """
        if name in self.store:
            return self.store[name][1]
        if self.outer is not None:
            return self.outer.resolve(name)
        return None

    def get(self, name: str) -> Any:
        """Obtém o valor de uma variável, subindo a cadeia de escopos.

        Args:
            name: Nome da variável.

        Returns:
            Valor da variável.

        Raises:
            NameError: Se a variável não estiver definida.
        """
        if name in self.store:
            return self.store[name][0]
        if self.outer is not None:
            return self.outer.get(name)
        raise NameError(f"Variável não definida: '{name}'")

    def set(self, name: str, value: Any, type_: MathLgType | None = None) -> None:
        """Atualiza o valor de uma variável existente.

        A variável deve já estar definida em algum escopo da cadeia.

        Args:
            name: Nome da variável.
            value: Novo valor.

        Raises:
            NameError: Se a variável não estiver definida.
        """
        if name in self.store:
            if type_ is None:
                type_ = MathLgType.infer(value)
            self.store[name] = (value, type_)
        elif self.outer is not None:
            self.outer.set(name, value, type_)
        else:
            raise NameError(f"Variável não definida: '{name}'")

    def __repr__(self) -> str:
        vars_str = ", ".join(f"{k}={v[0]}" for k, v in self.store.items())
        return f"Environment({vars_str})"
