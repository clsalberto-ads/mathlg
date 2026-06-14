"""Definição dos nós da Árvore Sintática Abstrata (AST) do MathLg.

Cada nó representa um constructo da linguagem. A AST é produzida pelo
parser e consumida pelo semantic analyzer e evaluator.

Usamos dataclasses para simplicidade e type hints rigorosos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mathlg.lang.tokens import Token


class BinOp(Enum):
    """Operadores binários."""
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    AND = auto()
    OR = auto()


class UnaryOpEnum(Enum):
    """Operadores unários."""
    PLUS = auto()       # + (não usado na prática, mas suportado)
    MINUS = auto()      # -
    NOT = auto()        # nao
    NEG = auto()        # menos unário (negativo)


class MathFunction(Enum):
    """Funções matemáticas embutidas."""
    SQRT = auto()
    SIN = auto()
    COS = auto()
    LOG = auto()
    ABS = auto()
    ROUND = auto()
    POWER = auto()       # binário, mas tratado como função


class CompareOp(Enum):
    """Operadores de comparação. Usado como tipo para o campo `op`."""
    GT = auto()
    LT = auto()
    EQ = auto()
    GTE = auto()
    LTE = auto()
    NEQ = auto()


# --- AST Node Definitions ---


@dataclass
class Program:
    """Raiz da AST. Contém uma lista de statements."""
    statements: list["Statement"] = field(default_factory=list)


@dataclass
class Statement:
    """Classe base para statements."""
    pass


@dataclass
class Expression(Statement):
    """Classe base para expressões."""
    pass


# --- Literais ---


@dataclass
class NumberLiteral(Expression):
    """Literal numérico (int ou float)."""
    value: int | float


@dataclass
class StringLiteral(Expression):
    """Literal de string."""
    value: str


@dataclass
class BoolLiteral(Expression):
    """Literal booleano."""
    value: bool


# --- Identificadores e Atribuição ---


@dataclass
class Identifier(Expression):
    """Referência a uma variável."""
    name: str


@dataclass
class Assignment(Statement):
    """Atribuição de valor a uma variável: x = <expressão>"""
    target: Identifier
    value: Expression


# --- Operações ---


@dataclass
class BinaryOp(Expression):
    """Operação binária: left <op> right"""
    op: BinOp
    left: Expression
    right: Expression


@dataclass
class UnaryOp(Expression):
    """Operação unária: <op> operand"""
    op: UnaryOpEnum
    operand: Expression


@dataclass
class Comparison(Expression):
    """Comparação: left <op> right"""
    op: CompareOp
    left: Expression
    right: Expression


@dataclass
class MathFunctionCall(Expression):
    """Chamada de funcao matemática embutida: sqrt(operand)"""
    func: MathFunction
    arguments: list[Expression]


# --- Control Flow ---


@dataclass
class IfStatement(Statement):
    """Condicional: if <condition> <then_block> [else <else_block>]"""
    condition: Expression
    then_body: list[Statement]
    else_body: list[Statement] | None = None


@dataclass
class WhileLoop(Statement):
    """Loop enquanto: while <condition> <body>"""
    condition: Expression
    body: list[Statement]


@dataclass
class ForLoop(Statement):
    """Loop para: for <var> = <start> to <end> <body>"""
    variable: Identifier
    start: Expression
    end: Expression
    body: list[Statement]


# --- Funções ---


@dataclass
class FunctionDef(Statement):
    """Definição de funcao: fn <name>(<params>) <body>"""
    name: str
    params: list[str]
    body: list[Statement]


@dataclass
class FunctionCall(Expression):
    """Chamada de funcao definida pelo usuário."""
    name: str
    arguments: list[Expression]


@dataclass
class ReturnStatement(Statement):
    """Retorno de valor de uma funcao."""
    value: Expression | None = None


# --- Print ---


@dataclass
class PrintStatement(Statement):
    """Exibe o valor de uma expressão no console. "mostre"."""
    expression: Expression


# --- Export ---


@dataclass
class ExportStatement(Statement):
    """Exportação de resultados."""
    format: str  # "csv" ou "json"


# --- Utilitário: repr com indentação ---


def ast_repr(node: object, indent: int = 0) -> str:
    """Retorna representação legível da AST (para debugging)."""
    prefix = "  " * indent

    match node:
        case Program(statements):
            lines = [f"{prefix}Program("]
            for stmt in statements:
                lines.append(ast_repr(stmt, indent + 1))
            lines.append(f"{prefix})")
            return "\n".join(lines)

        case NumberLiteral(value=v):
            return f"{prefix}Number({v})"

        case StringLiteral(value=v):
            return f"{prefix}String({v!r})"

        case BoolLiteral(value=v):
            return f"{prefix}Bool({v})"

        case Identifier(name=n):
            return f"{prefix}Identifier({n})"

        case Assignment(target=t, value=v):
            return f"{prefix}Assignment(\n{ast_repr(t, indent+1)}\n{ast_repr(v, indent+1)}\n{prefix})"

        case BinaryOp(op=op, left=l, right=r):
            return f"{prefix}BinaryOp({op.name},\n{ast_repr(l, indent+1)}\n{ast_repr(r, indent+1)}\n{prefix})"

        case Comparison(op=op, left=l, right=r):
            return f"{prefix}Comparison({op.name},\n{ast_repr(l, indent+1)}\n{ast_repr(r, indent+1)}\n{prefix})"

        case UnaryOp(op=op, operand=o):
            return f"{prefix}UnaryOp({op.name},\n{ast_repr(o, indent+1)}\n{prefix})"

        case MathFunctionCall(func=f, arguments=args):
            args_str = "\n".join(ast_repr(a, indent + 1) for a in args)
            return f"{prefix}MathFn({f.name},\n{args_str}\n{prefix})"

        case IfStatement(condition=c, then_body=t, else_body=e):
            result = f"{prefix}If(\n{ast_repr(c, indent+1)}\n{prefix}  then:"
            for stmt in t:
                result += f"\n{ast_repr(stmt, indent+2)}"
            if e:
                result += f"\n{prefix}  else:"
                for stmt in e:
                    result += f"\n{ast_repr(stmt, indent+2)}"
            result += f"\n{prefix})"
            return result

        case WhileLoop(condition=c, body=b):
            result = f"{prefix}While(\n{ast_repr(c, indent+1)}"
            for stmt in b:
                result += f"\n{ast_repr(stmt, indent+1)}"
            result += f"\n{prefix})"
            return result

        case ForLoop(variable=v, start=s, end=e, body=b):
            result = f"{prefix}For({v.name}, {ast_repr(s, indent+1)}, {ast_repr(e, indent+1)}"
            for stmt in b:
                result += f"\n{ast_repr(stmt, indent+1)}"
            result += f"\n{prefix})"
            return result

        case FunctionDef(name=n, params=p, body=b):
            result = f"{prefix}Function({n}({', '.join(p)}):"
            for stmt in b:
                result += f"\n{ast_repr(stmt, indent+1)}"
            result += f"\n{prefix})"
            return result

        case FunctionCall(name=n, arguments=args):
            args_str = ", ".join(ast_repr(a, indent + 1) for a in args)
            return f"{prefix}Call({n}, [{args_str}])"

        case ReturnStatement(value=v):
            return f"{prefix}Return(\n{ast_repr(v, indent+1)}\n{prefix})" if v else f"{prefix}Return()"

        case PrintStatement(expression=e):
            return f"{prefix}Print(\n{ast_repr(e, indent+1)}\n{prefix})"

        case ExportStatement(format=f):
            return f"{prefix}Export({f})"

        case None:
            return f"{prefix}None"

        case _:
            return f"{prefix}Unknown({type(node).__name__})"
