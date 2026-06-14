"""Avaliador (Evaluator) do MathLg.

Percorre a AST pós-análise semântica e executa cada nó, produzindo
valores concretos (int, float, str, bool) como resultado.
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
from mathlg.interpreter.builtins import BUILTINS
from mathlg.interpreter.environment import Environment
from mathlg.math.engine import MathEngine
from mathlg.math.types import MathLgType
from mathlg.semantic.errors import RuntimeError_


class ReturnSentinel(Exception):
    """Exceção interna para implementar return em funções.

    Quando o evaluator encontra um ReturnStatement, levanta esta exceção
    com o valor de retorno, que é capturada pelo caller da função.
    """

    def __init__(self, value: object) -> None:
        self.value = value


class Evaluator:
    """Avaliador de AST do MathLg.

    Attributes:
        env: Ambiente atual de execução.
        math: Engine de operações matemáticas.
    """

    def __init__(self, env: Environment | None = None) -> None:
        self.env = env or Environment()
        self.math = MathEngine()
        self._last_result: object = None

    def evaluate(self, node: object) -> object:
        """Avalia um nó da AST e retorna o valor resultante.

        Args:
            node: Nó da AST a ser avaliado.

        Returns:
            Valor resultante da avaliação.
        """
        match node:
            case Program(statements=stmts):
                return self._eval_program(stmts)

            case NumberLiteral(value=v):
                return v

            case StringLiteral(value=v):
                return v

            case BoolLiteral(value=v):
                return v

            case Identifier(name=name):
                return self.env.get(name)

            case Assignment(target=Identifier(name=name), value=value):
                val = self.evaluate(value)
                type_ = MathLgType.infer(val)
                self.env.define(name, val, type_)
                return val

            case BinaryOp(op=op, left=left, right=right):
                return self._eval_binary_op(op, left, right)

            case UnaryOp(op=op, operand=operand):
                return self._eval_unary_op(op, operand)

            case Comparison(op=op, left=left, right=right):
                return self._eval_compare(op, left, right)

            case MathFunctionCall(func=func, arguments=args):
                arg_vals = [self.evaluate(a) for a in args]
                return self._eval_math_function(func, arg_vals)

            case FunctionDef(name=name, params=params, body=body):
                # Armazena a definição da função no ambiente
                self.env.define(name, (params, body), MathLgType.FUNCTION)
                return None

            case FunctionCall(name=name, arguments=args):
                return self._eval_function_call(name, args)

            case IfStatement(condition=cond, then_body=then_b, else_body=else_b):
                return self._eval_if(cond, then_b, else_b)

            case WhileLoop(condition=cond, body=body):
                return self._eval_while(cond, body)

            case ForLoop(variable=Identifier(name=v_name), start=start, end=end, body=body):
                return self._eval_for(v_name, start, end, body)

            case ReturnStatement(value=value):
                val = self.evaluate(value) if value else None
                raise ReturnSentinel(val)

            case ExportStatement():
                return None

            case PrintStatement(expression=expr):
                val = self.evaluate(expr)
                print(val)
                return val

            case None:
                return None

            case _:
                raise RuntimeError_(f"Nó desconhecido na AST: {type(node).__name__}")

    def _eval_program(self, statements: list[Statement]) -> object:
        result = None
        for stmt in statements:
            result = self.evaluate(stmt)
        return result

    def _eval_binary_op(self, op: BinOp, left: Expression, right: Expression) -> object:
        lv = self.evaluate(left)
        rv = self.evaluate(right)

        # Garante que são numéricos
        lv = self._to_number(lv)
        rv = self._to_number(rv)

        match op:
            case BinOp.PLUS:
                return self.math.add(lv, rv)
            case BinOp.MINUS:
                return self.math.subtract(lv, rv)
            case BinOp.TIMES:
                return self.math.multiply(lv, rv)
            case BinOp.DIVIDE:
                return self.math.divide(lv, rv)
            case BinOp.AND:
                return bool(lv) and bool(rv)
            case BinOp.OR:
                return bool(lv) or bool(rv)

    def _eval_unary_op(self, op: UnaryOpEnum, operand: Expression) -> object:
        val = self.evaluate(operand)

        match op:
            case UnaryOpEnum.MINUS:
                return -self._to_number(val)
            case UnaryOpEnum.NOT:
                return not bool(val)
            case UnaryOpEnum.PLUS:
                return self._to_number(val)

    def _eval_compare(self, op: CompareOp, left: Expression, right: Expression) -> bool:
        lv = self.evaluate(left)
        rv = self.evaluate(right)

        # Comparações numéricas
        if isinstance(lv, (int, float)) and isinstance(rv, (int, float)):
            match op:
                case CompareOp.GT: return lv > rv
                case CompareOp.LT: return lv < rv
                case CompareOp.EQ: return lv == rv
                case CompareOp.GTE: return lv >= rv
                case CompareOp.LTE: return lv <= rv
                case CompareOp.NEQ: return lv != rv

        # Comparação genérica
        match op:
            case CompareOp.EQ: return lv == rv
            case CompareOp.NEQ: return lv != rv
            case _:
                raise RuntimeError_(
                    f"Comparação inválida entre {type(lv).__name__} e {type(rv).__name__}"
                )

    def _eval_math_function(self, func: MathFunction, arg_vals: list[object]) -> object:
        args = [self._to_number(a) for a in arg_vals]

        match func:
            case MathFunction.SQRT:
                return self.math.sqrt(args[0])
            case MathFunction.SIN:
                return self.math.sin(args[0])
            case MathFunction.COS:
                return self.math.cos(args[0])
            case MathFunction.LOG:
                return self.math.log(args[0])
            case MathFunction.ABS:
                return self.math.abs(args[0])
            case MathFunction.ROUND:
                return self.math.round(args[0])
            case MathFunction.POWER:
                return self.math.power(args[0], args[1])

    def _eval_function_call(self, name: str, args: list[Expression]) -> object:
        # Verifica se é built-in primeiro
        if name in BUILTINS:
            func, min_args, max_args = BUILTINS[name]
            arg_vals = [self.evaluate(a) for a in args]
            return func(*arg_vals)

        # Procura definição da função no ambiente
        resolved = self.env.resolve(name)
        if resolved is None:
            # Tenta como função matemática (caso o parser não tenha capturado)
            func_map = {
                "sqrt": MathFunction.SQRT,
                "sin": MathFunction.SIN,
                "cos": MathFunction.COS,
                "log": MathFunction.LOG,
                "abs": MathFunction.ABS,
                "pow": MathFunction.POWER,
            }
            if name in func_map:
                arg_vals = [self.evaluate(a) for a in args]
                return self._eval_math_function(func_map[name], arg_vals)

            raise RuntimeError_(f"Função não definida: '{name}'")

        # Função definida pelo usuário
        fn_def = self.env.get(name)
        if not isinstance(fn_def, tuple) or len(fn_def) != 2:
            raise RuntimeError_(f"'{name}' não é uma função")

        params, body = fn_def

        # Cria novo escopo para a chamada
        call_env = Environment(outer=self.env)
        arg_vals = [self.evaluate(a) for a in args]

        # Vincula parâmetros aos argumentos
        for param_name, arg_val in zip(params, arg_vals):
            call_env.define(param_name, arg_val)

        # Avalia corpo da função
        old_env = self.env
        self.env = call_env

        try:
            result = None
            for stmt in body:
                result = self.evaluate(stmt)
            return result
        except ReturnSentinel as ret:
            return ret.value
        finally:
            self.env = old_env

    def _eval_if(
        self,
        cond: Expression,
        then_body: list[Statement],
        else_body: list[Statement] | None,
    ) -> object:
        cond_val = self.evaluate(cond)

        if cond_val:
            result = None
            for stmt in then_body:
                result = self.evaluate(stmt)
            return result
        elif else_body:
            result = None
            for stmt in else_body:
                result = self.evaluate(stmt)
            return result

        return None

    def _eval_while(self, cond: Expression, body: list[Statement]) -> object:
        result = None
        while self.evaluate(cond):
            for stmt in body:
                result = self.evaluate(stmt)
        return result

    def _eval_for(self, var_name: str, start: Expression, end: Expression, body: list[Statement]) -> object:
        start_val = int(self._to_number(self.evaluate(start)))
        end_val = int(self._to_number(self.evaluate(end)))

        # Cria escopo para a variável do loop
        old_env = self.env
        self.env = Environment(outer=old_env)
        result = None

        try:
            for i in range(start_val, end_val + 1):
                self.env.define(var_name, i)
                for stmt in body:
                    result = self.evaluate(stmt)
            return result
        finally:
            self.env = old_env

    def _to_number(self, value: object) -> int | float:
        """Converte valor para número, se possível.

        Raises:
            RuntimeError_: Se o valor não for numérico.
        """
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    raise RuntimeError_(f"Não é um número: '{value}'")
        # Fallback: tenta converter via float()
        try:
            return float(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            raise RuntimeError_(f"Valor não numérico: {type(value).__name__}")


def evaluate(ast: Program, env: Environment) -> object:
    """Função de conveniência: avalia uma AST completa.

    Args:
        ast: AST do programa.
        env: Ambiente atual de execução.

    Returns:
        Valor resultante da última expressão.
    """
    evaluator = Evaluator(env)
    return evaluator.evaluate(ast)
