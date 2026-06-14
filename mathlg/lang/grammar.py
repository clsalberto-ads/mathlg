"""Definição da gramática do MathLg em notação BNF-like.

A linguagem tem uma gramática de contexto controlado (não é português livre).

<program>         ::= <statement>+

<statement>       ::= <assignment>
                    | <function_definition>
                    | <if_statement>
                    | <while_loop>
                    | <for_loop>
                    | <expression>
                    | <export_statement>

<assignment>      ::= <identifier> "=" <expression>

<function_definition>
                  ::= ("funcao" | "function") <identifier> "(" <params> ")"
                      <block>

<params>          ::= <identifier> ("," <identifier>)* | ε

<if_statement>    ::= ("se" | "if") <expression> <block>
                      [ ("senao" | "else") <block> ]

<while_loop>      ::= ("enquanto" | "while") <expression> <block>

<for_loop>        ::= ("para" | "for") <identifier> "=" <expression>
                      ("ate" | "to") <expression> <block>

<block>           ::= ":" <statement>+   (linha atual com :)
                    | indent <statement>+ dedent

<export_statement> ::= ("exportar" | "export") ("csv" | "json")

<expression>      ::= <logical_or>

<logical_or>      ::= <logical_and> (("ou" | "or") <logical_and>)*

<logical_and>     ::= <comparison> (("e" | "and") <comparison>)*

<comparison>      ::= <addition> (("maior que" | "menor que" | "igual a"
                     | "maior ou igual" | "menor ou igual" | "diferente de")
                     <addition>)*

<addition>        ::= <term> (("mais" | "menos" | "plus" | "minus") <term>)*

<term>            ::= <factor> (("vezes" | "dividido por" | "times"
                     | "divided by") <factor>)*

<factor>          ::= ("nao" | "not")? <unary>

<unary>           ::= ("raiz quadrada de" | "square root of" |
                      "seno de" | "sine of" |
                      "cosseno de" | "cosine of" |
                      "logaritmo de" | "logarithm of" |
                      "valor absoluto de" | "absolute value of" |
                      "arredondar" | "round") <unary>
                    | ("potencia de" | "power of") <unary>
                      ("elevado a" | "to the power of") <unary>
                    | <primary>

<primary>         ::= <number>
                    | <string>
                    | <boolean>
                    | <identifier>
                    | <function_call>
                    | "(" <expression> ")"

<function_call>   ::= <identifier> "(" <arguments> ")"

<arguments>       ::= <expression> ("," <expression>)* | ε

<number>          ::= <integer> | <float>
<integer>         ::= [0-9]+
<float>           ::= [0-9]+ "." [0-9]+
<string>          ::= '"' [^"]* '"' | "'" [^']* "'"
<boolean>         ::= "verdadeiro" | "falso" | "true" | "false"
<identifier>      ::= [a-zA-Z_][a-zA-Z0-9_]*
"""

# Nota: Esta gramática é para documentação. O parser real implementa
# este mesmo conjunto de regras via recursive descent manual.
# A precedência é:
#   1. Parênteses (mais alta)
#   2. Unário (sqrt, sin, cos, log, abs, not)
#   3. Potência
#   4. Multiplicação / Divisão
#   5. Adição / Subtração
#   6. Comparação
#   7. AND lógico
#   8. OR lógico (mais baixa)

PRECEDENCE: dict[str, int] = {
    "or": 1,
    "and": 2,
    "not": 3,
    "comparison": 4,
    "addition": 5,
    "term": 6,
    "unary": 7,
    "power": 8,
}
