"""English keyword dictionary for MathLg.

Maps natural language expressions (English) to normalized tokens
(always in English) that the parser understands.
"""

from mathlg.i18n.base import KeywordMap
from mathlg.lang.tokens import TokenType


def create_en_keywords() -> KeywordMap:
    """Creates and returns the English keyword dictionary.

    Returns:
        KeywordMap configured with English words and expressions.
    """
    km = KeywordMap(name="en")

    km.extend({
        # Commands
        "calculate": TokenType.CALC,
        "calc": TokenType.CALC,
        "compute": TokenType.CALC,
        "show": TokenType.CALC,
        "print": TokenType.CALC,

        # Basic operators
        "plus": TokenType.PLUS,
        "add": TokenType.PLUS,
        "minus": TokenType.MINUS,
        "subtract": TokenType.MINUS,
        "times": TokenType.TIMES,
        "multiplied by": TokenType.TIMES,
        "divided by": TokenType.DIVIDE,
        "over": TokenType.DIVIDE,

        # Math functions
        "square root of": TokenType.SQRT,
        "square root": TokenType.SQRT,
        "sqrt": TokenType.SQRT,
        "power of": TokenType.POWER,
        "to the power of": TokenType.POWER,
        "raised to": TokenType.POWER,
        "sine of": TokenType.SIN,
        "sine": TokenType.SIN,
        "sin": TokenType.SIN,
        "cosine of": TokenType.COS,
        "cosine": TokenType.COS,
        "cos": TokenType.COS,
        "logarithm of": TokenType.LOG,
        "natural log of": TokenType.LOG,
        "log of": TokenType.LOG,
        "log": TokenType.LOG,
        "absolute value of": TokenType.ABS,
        "absolute value": TokenType.ABS,
        "abs": TokenType.ABS,
        "round": TokenType.ROUND,

        # Booleans
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "not": TokenType.NOT,

        # Comparison
        "greater than": TokenType.GT,
        "greater": TokenType.GT,
        "less than": TokenType.LT,
        "less": TokenType.LT,
        "equal to": TokenType.EQ,
        "equal": TokenType.EQ,
        "equals": TokenType.EQ,
        "greater or equal to": TokenType.GTE,
        "greater or equal": TokenType.GTE,
        "less or equal to": TokenType.LTE,
        "less or equal": TokenType.LTE,
        "different from": TokenType.NEQ,
        "different": TokenType.NEQ,
        "not equal to": TokenType.NEQ,

        # Control flow
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "for": TokenType.FOR,
        "to": TokenType.FOR,

        # Functions
        "function": TokenType.FN,
        "fn": TokenType.FN,
        "def": TokenType.FN,
        "return": TokenType.RETURN,

        # Export
        "export": TokenType.EXPORT,
    })

    return km
