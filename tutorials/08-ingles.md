# Tutorial 08: MathLg em Inglês

Este tutorial demonstra como usar o MathLg no idioma inglês. Basta ativar o modo com `--lang=en` na linha de comando ou usar `/idioma en` no REPL. A sintaxe é idêntica à versão em português, apenas o vocabulário muda.

Execute com: `mathlg --lang=en tutorials/08-ingles.mlg`

## 1. Basic Arithmetic

Operadores aritméticos em inglês: `plus`, `minus`, `times`, `divided by`. Símbolos matemáticos (`+`, `-`, `*`, `/`) também funcionam.

```mlg
print "=== 1. BASIC ARITHMETIC ==="
print 2 plus 3                        # 5
print 10 minus 4                      # 6
print 7 times 6                       # 42
print 20 divided by 4                 # 5.0
print 2 + 3                           # 5 (symbol +)
print (2 plus 3) times 4             # 20
```

> **O que acontece:** Cada operação usa palavras-chave em inglês. `plus` soma, `minus` subtrai, `times` multiplica e `divided by` divide. Parênteses controlam a precedência: `(2 plus 3) times 4` soma primeiro, depois multiplica.

## 2. Math Functions

Funções matemáticas também têm nomes em inglês, com versões completas e abreviadas.

```mlg
print "=== 2. MATH FUNCTIONS ==="
print square root of 144              # 12.0
print power of 2 to the power of 3    # 8
print sine of 0                       # 0.0
print cosine of 0                     # 1.0
print logarithm of 1                  # 0.0
print absolute value of -10           # 10
print round 3.7                       # 4

short forms
print sqrt(25)                        # 5.0
print sin(0)                          # 0.0
print cos(0)                          # 1.0
print abs(-5)                         # 5
print log(1)                          # 0.0
```

> **O que acontece:** Funções podem ser escritas por extenso (`square root of`, `sine of`) ou na forma abreviada com parênteses (`sqrt()`, `sin()`), assim como em português. Ambas produzem o mesmo resultado.

## 3. Variables

Variáveis funcionam da mesma forma, com atribuição usando `=` e exibição com `print`.

```mlg
print "=== 3. VARIABLES ==="
x = 10
y = 5
print x plus y                        # 15
print x times y                       # 50
print x minus 3                       # 7
result = x * y + 2
print result                          # 52
```

> **O que acontece:** A declaração e uso de variáveis é idêntica ao português, apenas os operadores textuais mudam para inglês. Expressões podem misturar operadores textuais e simbólicos.

## 4. Comparisons

Operadores de comparação em inglês: `greater than`, `less than`, `equal to`, `not equal to`, `greater or equal to`, `less or equal to`.

```mlg
print "=== 4. COMPARISONS ==="
print 10 greater than 5                # true
print 3 less than 8                    # true
print 5 equal to 5                     # true
print 10 not equal to 5                # true
print 10 greater or equal to 10        # true
print 3 less or equal to 5             # true
```

> **O que acontece:** Cada operador de comparação tem seu correspondente em inglês. `greater than` é maior que, `less than` é menor que, `equal to` é igual a, e assim por diante. Todos retornam `true` ou `false`.

## 5. Booleans

Valores e operadores booleanos em inglês: `true`, `false`, `and`, `or`, `not`.

```mlg
print "=== 5. BOOLEANS ==="
print true and false                   # false
print true or false                    # true
print not true                         # false
```

> **O que acontece:** Os valores booleanos são `true` e `false` em inglês. `and` exige que ambos sejam verdadeiros, `or` exige pelo menos um e `not` inverte o valor.

## 6. Conditionals

Condicionais usam `if` e `else` no lugar de `se` e `senao`.

```mlg
print "=== 6. CONDITIONALS ==="
age = 20
if age > 18: print "adult" else: print "minor"    # adult

score = 75
if score >= 60: print "passed" else: print "failed"  # passed
```

> **O que acontece:** A estrutura é idêntica: `if condicao: comando else: comando`. A diferença é apenas o vocabulário. O corpo continua na mesma linha da condição.

## 7. Loops

Loops usam `while` e `for` com `to` no lugar de `enquanto` e `para`/`ate`.

```mlg
print "=== 7. LOOPS ==="
counter = 0
while counter < 5: counter = counter + 1
print counter                         # 5

for i = 1 to 5: print i               # 1, 2, 3, 4, 5
```

> **O que acontece:** `while` repete enquanto a condição for verdadeira. `for i = 1 to 5` itera de 1 a 5, igual ao `para i = 1 ate 5` em português. A única diferença é a palavra-chave.

## 8. Functions

Funções em inglês usam `function` e `return` no lugar de `funcao` e `retorne`.

```mlg
print "=== 8. FUNCTIONS ==="
function double(x): return x * 2
print double(5)                       # 10

function sum(a, b): return a + b
print sum(3, 4)                       # 7

function factorial(n): if n <= 1: return 1 else: return n * factorial(n - 1)
print factorial(5)                    # 120
```

> **O que acontece:** `function` declara a função, `return` retorna o valor. Funções podem conter condicionais e chamadas recursivas, como `factorial`. A sintaxe é a mesma do português, apenas com palavras em inglês.
