"""Analisador semântico do MathLg.

Responsabilidades:
  1. Type checking: verificar se operandos têm tipos compatíveis.
  2. Scope resolution: verificar se variáveis/funções foram definidas.
  3. Function arity: verificar número de argumentos.
  4. Loop/if conditions: verificar se condição é booleana.
  5. Anotar a AST com informações de tipo para o evaluator.

O analisador NÃO modifica a AST — produz uma lista de erros semânticos.
"""

from __future__ import annotations

from mathlg.lang.ast_nodes import (
    Assignment,
    BinaryOp, BinOp,
    BoolLiteral,
    CompareOp,
    Comparison,
    ExportStatement,
    Expression,
    ForLoop,
    FunctionCall,
    FunctionDef,
    Identifier,
    IfStatement,
    MathFunction, MathFunctionCall,
    NumberLiteral,
    PrintStatement,
    Program,
    ReturnStatement,
    Statement,
    StringLiteral,
    UnaryOp, UnaryOpEnum,
    WhileLoop,
)
from mathlg.math.types import MathLgType
from mathlg.interpreter.environment import Environment
from mathlg.semantic.errors import SemanticError


class TypeEnvironment:
    """Ambiente de tipos compartilhado entre chamadas do SemanticAnalyzer.

    Mantém uma pilha de escopos com tipos de variáveis/funções.
    Não interfere com o Environment de valores do evaluator.
    Oferece fallback opcional para consultar o Environment quando
    um nome não é encontrado nos escopos internos.
    """

    def __init__(self, fallback_env: Environment | None = None) -> None:
        self._scopes: list[dict[str, MathLgType]] = [{}]
        self._fallback = fallback_env

    def set(self, name: str, type_: MathLgType) -> None:
        """Registra o tipo de um nome no escopo atual."""
        self._scopes[-1][name] = type_

    def get(self, name: str) -> MathLgType | None:
        """Busca o tipo de um nome (escopos internos primeiro, depois fallback)."""
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        if self._fallback is not None:
            return self._fallback.resolve(name)
        return None

    def push_scope(self) -> None:
        """Abre um novo escopo."""
        self._scopes.append({})

    def pop_scope(self) -> None:
        """Fecha o escopo atual."""
        if len(self._scopes) > 1:
            self._scopes.pop()


class SemanticAnalyzer:
    """Percorre a AST e valida restrições semânticas.

    Usa rastreamento interno de tipos (NÃO polui o environment de valores
    do evaluator). Para resolução de nomes, primeiro verifica os tipos
    internos e depois consulta o environment como fallback.

    Attributes:
        env: Ambiente de valores (read-only) para resolução de nomes pré-definidos.
        errors: Lista de erros semânticos encontrados.
    """

    def __init__(self, type_env: TypeEnvironment | None = None) -> None:
        self.type_env = type_env or TypeEnvironment()
        self.errors: list[SemanticError] = []

    # --- Análise ---

    def analyze(self, node: object) -> MathLgType:
        """Analisa um nó da AST.

        Returns:
            O tipo MathLg do resultado da expressão, ou NoneType.

        Raises:
            SemanticError: Adiciona erro à lista self.errors em vez de levantar.
                           Isso permite coletar múltiplos erros em uma passada.
        """
        try:
            return self._analyze(node)
        except SemanticError as e:
            self.errors.append(e)
            return MathLgType.NULL

    def _analyze(self, node: object) -> MathLgType:
        """Implementação interna da análise, que pode levantar SemanticError."""
        match node:
            case Program(statements=stmts):
                return self._analyze_program(stmts)

            case NumberLiteral():
                return MathLgType.INTEGER if isinstance(node.value, int) else MathLgType.DECIMAL

            case StringLiteral():
                return MathLgType.TEXT

            case BoolLiteral():
                return MathLgType.LOGICAL

            case Identifier(name=name):
                return self._resolve_identifier(name)

            case Assignment(target=Identifier(name=name), value=value):
                val_type = self._analyze(value)
                self.type_env.set(name, val_type)
                return val_type

            case BinaryOp(op=op, left=left, right=right):
                return self._analyze_binary_op(op, left, right)

            case UnaryOp(operand=operand):
                return self._analyze(operand)

            case Comparison(left=left, right=right):
                left_type = self._analyze(left)
                right_type = self._analyze(right)

                # Permite comparar INTEGER com DECIMAL (coerção implícita)
                numeric_types = {MathLgType.INTEGER, MathLgType.DECIMAL}
                if left_type in numeric_types and right_type in numeric_types:
                    return MathLgType.LOGICAL

                if left_type != right_type:
                    raise SemanticError(
                        f"Comparação entre tipos incompatíveis: {left_type} e {right_type}"
                    )
                return MathLgType.LOGICAL

            case MathFunctionCall(func=func, arguments=args):
                return self._analyze_math_function(func, args)

            case FunctionDef(name=name, params=params, body=body):
                return self._analyze_function_def(name, params, body)

            case FunctionCall(name=name, arguments=args):
                return self._analyze_function_call(name, args)

            case IfStatement(condition=cond, then_body=then_b, else_body=else_b):
                return self._analyze_if(cond, then_b, else_b)

            case WhileLoop(condition=cond, body=body):
                return self._analyze_while(cond, body)

            case ForLoop(variable=Identifier(name=v_name), start=start, end=end, body=body):
                return self._analyze_for(v_name, start, end, body)

            case ReturnStatement(value=value):
                return self._analyze(value) if value else MathLgType.NULL

            case ExportStatement():
                return MathLgType.NULL

            case PrintStatement(expression=expr):
                return self._analyze(expr)

            case None:
                return MathLgType.NULL

            case _:
                raise SemanticError(f"Nó desconhecido na AST: {type(node).__name__}")

    def _analyze_program(self, statements: list[Statement]) -> MathLgType:
        result = MathLgType.NULL
        for stmt in statements:
            result = self._analyze(stmt)
        return result

    def _resolve_identifier(self, name: str) -> MathLgType:
        resolved = self.type_env.get(name)
        if resolved is None:
            raise SemanticError(f"Variável não definida: '{name}'")
        return resolved

    def _analyze_binary_op(self, op: BinOp, left: Expression, right: Expression) -> MathLgType:
        left_type = self._analyze(left)
        right_type = self._analyze(right)

        # Operações lógicas (AND, OR) exigem booleanos
        if op in (BinOp.AND, BinOp.OR):
            if left_type != MathLgType.LOGICAL:
                raise SemanticError(f"AND/OR espera operando lógico, encontrado {left_type}")
            if right_type != MathLgType.LOGICAL:
                raise SemanticError(f"AND/OR espera operando lógico, encontrado {right_type}")
            return MathLgType.LOGICAL

        # Operações aritméticas (+, -, *, /) exigem números
        if left_type not in (MathLgType.INTEGER, MathLgType.DECIMAL):
            raise SemanticError(f"Operação aritmética espera número, encontrado {left_type}")
        if right_type not in (MathLgType.INTEGER, MathLgType.DECIMAL):
            raise SemanticError(f"Operação aritmética espera número, encontrado {right_type}")

        # int + int = int, float + qualquer = float
        if left_type == MathLgType.DECIMAL or right_type == MathLgType.DECIMAL:
            return MathLgType.DECIMAL
        return MathLgType.INTEGER

    def _analyze_math_function(self, func, args: list[Expression]) -> MathLgType:
        for arg in args:
            arg_type = self._analyze(arg)
            if arg_type not in (MathLgType.INTEGER, MathLgType.DECIMAL):
                raise SemanticError(
                    f"Função matemática espera número, encontrado {arg_type}"
                )

        # sqrt, sin, cos, log, abs, round, power retornam float
        return MathLgType.DECIMAL

    def _analyze_function_def(
        self, name: str, params: list[str], body: list[Statement]
    ) -> MathLgType:
        # Cria um novo escopo de tipos para a função
        self.type_env.push_scope()

        # Define parâmetros como números no escopo da função
        for param in params:
            self.type_env.set(param, MathLgType.DECIMAL)

        # Analisa o corpo
        result_type = MathLgType.NULL
        for stmt in body:
            result_type = self._analyze(stmt)

        # Fecha o escopo da função e registra a função no escopo externo
        self.type_env.pop_scope()
        self.type_env.set(name, MathLgType.FUNCTION)

        return MathLgType.FUNCTION

    def _analyze_function_call(self, name: str, args: list[Expression]) -> MathLgType:
        resolved = self.type_env.get(name)
        if resolved is None:
            raise SemanticError(f"Função não definida: '{name}'")

        for arg in args:
            self._analyze(arg)

        return MathLgType.DECIMAL  # função retorna número por padrão

    def _analyze_if(
        self,
        cond: Expression,
        then_body: list[Statement],
        else_body: list[Statement] | None,
    ) -> MathLgType:
        cond_type = self._analyze(cond)
        if cond_type != MathLgType.LOGICAL:
            raise SemanticError(
                f"Condição if espera valor lógico, encontrado {cond_type}"
            )

        # Bloco then tem seu próprio escopo
        self.type_env.push_scope()
        for stmt in then_body:
            self._analyze(stmt)
        self.type_env.pop_scope()

        if else_body:
            self.type_env.push_scope()
            for stmt in else_body:
                self._analyze(stmt)
            self.type_env.pop_scope()

        return MathLgType.NULL

    def _analyze_while(self, cond: Expression, body: list[Statement]) -> MathLgType:
        cond_type = self._analyze(cond)
        if cond_type != MathLgType.LOGICAL:
            raise SemanticError(
                f"Condição while espera valor lógico, encontrado {cond_type}"
            )

        self.type_env.push_scope()
        for stmt in body:
            self._analyze(stmt)
        self.type_env.pop_scope()

        return MathLgType.NULL

    def _analyze_for(
        self, var_name: str, start: Expression, end: Expression, body: list[Statement]
    ) -> MathLgType:
        self._analyze(start)
        self._analyze(end)

        self.type_env.push_scope()
        self.type_env.set(var_name, MathLgType.INTEGER)

        for stmt in body:
            self._analyze(stmt)

        self.type_env.pop_scope()
        return MathLgType.NULL


def analyze(
    ast: Program,
    env: Environment,
    type_env: TypeEnvironment | None = None,
) -> list[SemanticError]:
    """Função de conveniência para análise semântica.

    Args:
        ast: AST do programa.
        env: Ambiente de valores (escopo) atual — usado como fallback
             para resolução de tipos de variáveis já definidas pelo evaluator.
        type_env: Ambiente de tipos compartilhado entre chamadas.
                  Se None, cria um novo (tipos NÃO persistem entre chamadas).

    Returns:
        Lista de erros semânticos (vazia se OK).
    """
    if type_env is None:
        # Cria um TypeEnvironment com fallback para o env de valores
        type_env = TypeEnvironment(fallback_env=env)
    analyzer = SemanticAnalyzer(type_env)
    analyzer.analyze(ast)
    return analyzer.errors
