# Tutorial 12: Casos Extremos (Edge Cases)

Conheça situações limite e comportamentos especiais do MathLg: operações com zero, números negativos, grandes valores, expressões aninhadas, strings vazias, múltiplos espaços e muito mais.

---

## 1. Operações com Zero

O zero é um valor especial em qualquer linguagem. Veja como MathLg se comporta com ele nas quatro operações básicas.

```mlg
mostre "=== 1. OPERACOES COM ZERO ==="
mostre 0 + 0                       # 0
mostre 0 * 100                     # 0
mostre 100 * 0                     # 0
mostre 0 / 5                       # 0.0
mostre 5 + 0                       # 5
mostre 5 - 0                       # 5
```

> **O que acontece:** Zero somado ou subtraído não altera o valor. Multiplicar por zero sempre resulta em zero. Dividir zero por qualquer número resulta em `0.0` (decimal). Qualquer número dividido por zero causaria um erro (não testado aqui).

---

## 2. Números Negativos

MathLg suporta números negativos e expressões unárias com o sinal de menos.

```mlg
mostre "=== 2. NUMEROS NEGATIVOS ==="
mostre -5                          # -5
mostre -10 + 3                     # -7
mostre -5 * -3                     # 15
mostre -10 / 2                     # -5.0
mostre valor absoluto de -42       # 42
```

> **O que acontece:** Negativos seguem as regras matemáticas: `-5 * -3 = 15` (negativo × negativo = positivo). A função `valor absoluto de` retorna o valor positivo de qualquer número.

---

## 3. Números Grandes

MathLg pode trabalhar com números grandes, limitados apenas pela capacidade de memória.

```mlg
mostre "=== 3. NUMEROS GRANDES ==="
mostre 999999999                   # 999999999
mostre 1000000 * 1000000           # 1000000000000
```

> **O que acontece:** O número `999999999` é exibido sem perda de precisão. A multiplicação `1.000.000 × 1.000.000 = 1.000.000.000.000` (um trilhão) é calculada corretamente.

---

## 4. Resultados Decimais

Operações que produzem resultados não inteiros são representadas como decimais.

```mlg
mostre "=== 4. DECIMAIS ==="
mostre 10 / 3                      # 3.333...
mostre 7 * 0.5                     # 3.5
mostre 10 + 0.5                    # 10.5
```

> **O que acontece:** `10 / 3` produz uma dízima periódica. Quando um decimal participa de uma operação com um inteiro, o resultado é decimal (`7 * 0.5 = 3.5`, `10 + 0.5 = 10.5`).

---

## 5. Parênteses Aninhados

Parênteses controlam a precedência de operadores, permitindo expressões complexas e aninhadas.

```mlg
mostre "=== 5. PARENTESES ==="
mostre 2 + 3 * 4                   # 14
mostre (2 + 3) * 4                 # 20
mostre ((2 + 3) * 4) - 1          # 19
mostre (10 - (2 + 3)) * 2          # 10
```

> **O que acontece:** Sem parênteses, a multiplicação tem precedência sobre a adição (`2 + 3 * 4 = 14`). Com parênteses, a adição é feita primeiro (`(2 + 3) * 4 = 20`). Parênteses podem ser aninhados em múltiplos níveis.

---

## 6. Funções Aninhadas

Funções matemáticas podem receber expressões ou outras funções como argumentos.

```mlg
mostre "=== 6. FUNCOES ANINHADAS ==="
mostre raiz de (4 + 5)             # 3.0 = sqrt(9)
mostre valor absoluto de (-(5+3))  # 8 = abs(-8)
mostre raiz de (potencia de 3 elevado a 2)  # 3.0 = sqrt(9)
```

> **O que acontece:** `raiz de (4 + 5)` calcula `sqrt(9) = 3.0`. `valor absoluto de (-(5+3))` calcula `abs(-8) = 8`. Funções podem ser compostas: `raiz de (potencia de 3 elevado a 2)` é `sqrt(3²) = 3.0`.

---

## 7. Strings

Strings podem ser vazias ou conter texto com espaços e caracteres especiais.

```mlg
mostre "=== 7. STRINGS ==="
vazia = ""
mostre vazia                       # (vazio)
texto = "MathLg v0.1"
mostre texto                       # MathLg v0.1
```

> **O que acontece:** Uma string vazia (`""`) não imprime nada. Strings podem conter espaços, números e versões sem problemas.

---

## 8. Múltiplos Espaços

Espaços extras entre tokens são ignorados pelo interpretador.

```mlg
mostre "=== 8. ESPACOS EXTRAS ==="
mostre 2       +       3           # 5 (espacos sao ignorados)
```

> **O que acontece:** Múltiplos espaços entre `2`, `+` e `3` não afetam o resultado. O interpretador trata todos os espaços em branco como delimitadores, ignorando a quantidade.

---

## 9. Atribuição Encadeada

Variáveis podem ser usadas em novas atribuições, criando cadeias de dependência.

```mlg
mostre "=== 9. ATRIBUICOES ==="
x = 10
y = x + 1
z = y * 2
mostre x                           # 10
mostre y                           # 11
mostre z                           # 22
```

> **O que acontece:** O valor flui através das variáveis: `x = 10`, `y = 10 + 1 = 11`, `z = 11 * 2 = 22`. Cada variável pode referenciar variáveis definidas anteriormente.

---

## 10. Operadores Unários

Operadores unários atuam sobre um único valor: negação (`-`) e negação lógica (`nao`).

```mlg
mostre "=== 10. OPERADORES UNARIOS ==="
mostre -(5 + 3)                    # -8
mostre nao verdadeiro               # False
mostre nao (10 > 5)                # False
```

> **O que acontece:** `-(5 + 3)` primeiro soma `5 + 3 = 8` e depois inverte o sinal: `-8`. `nao verdadeiro` nega o valor lógico, resultando em `False`. `nao (10 > 5)` primeiro avalia a comparação (`True`) e depois a nega.
