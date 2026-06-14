# Tutorial 01: Operações Aritméticas Básicas

Este tutorial ensina as quatro operações fundamentais da MathLg: adição, subtração, multiplicação e divisão. Você também aprenderá sobre precedência de operadores e como usar parênteses para controlar a ordem de cálculo.

## 1. Adição

A adição pode ser feita com a palavra `mais` ou com o símbolo `+`. A MathLg aceita números inteiros, negativos e decimais.

```mlg
mostre "=== 1. ADICAO ==="
mostre 2 mais 3
mostre 10 mais 20
mostre 0 mais 0
mostre -5 mais 8
mostre 2 + 3
mostre 2.5 mais 3.2
```

> **O que acontece:** cada linha é processada individualmente. Os resultados exibidos são, respectivamente: 5, 30, 0, 3 (soma com negativo), 5 (usando símbolo `+`) e 5.7 (soma decimal).

## 2. Subtração

A subtração usa `menos` ou o símbolo `-`. Resultados negativos são suportados naturalmente.

```mlg
mostre "=== 2. SUBTRACAO ==="
mostre 10 menos 4
mostre 100 menos 1
mostre 5 menos 10
mostre 10 - 4
mostre 10 menos 0
```

> **O que acontece:** 6, 99, -5 (subtração com resultado negativo), 6 (usando `-`) e 10 (subtrair zero não altera o valor).

## 3. Multiplicação

Multiplicação pode ser escrita como `vezes`, `multiplicado por` ou com o símbolo `*`.

```mlg
mostre "=== 3. MULTIPLICACAO ==="
mostre 7 vezes 6
mostre 3 multiplicado por 4
mostre 5 * 8
mostre 10 vezes 0
mostre 2.5 vezes 3
```

> **O que acontece:** 42, 12, 40 (usando `*`), 0 (todo número vezes zero é zero) e 7.5 (multiplicação decimal).

## 4. Divisão

A divisão usa `dividido por` ou o símbolo `/`. O resultado é sempre um número decimal.

```mlg
mostre "=== 4. DIVISAO ==="
mostre 20 dividido por 4
mostre 10 / 3
mostre 7 dividido por 2
mostre 0 dividido por 5
```

> **O que acontece:** 5.0 (resultado decimal exato), 3.333... (divisão não exata), 3.5 e 0.0 (zero dividido por qualquer número é zero).

## 5. Precedência de Operadores

Assim como na matemática tradicional, multiplicação e divisão têm precedência sobre adição e subtração. Use parênteses para alterar essa ordem.

```mlg
mostre "=== 5. PRECEDENCIA ==="
mostre 2 mais 3 vezes 4
mostre (2 mais 3) vezes 4
mostre 10 menos 3 vezes 2
mostre 20 / 2 mais 3
mostre 20 / (2 mais 3)
mostre 2 mais 3 menos 1
mostre 10 * 2 / 4
```

> **O que acontece:** A primeira linha resulta em 14 (multiplicação primeiro). Com parênteses, `(2+3)*4` = 20. A expressão `10 - 3*2` = 4, `20/2 + 3` = 13.0, `20/(2+3)` = 4.0. Operações de mesma precedência (`+` e `-`) são avaliadas da esquerda para a direita.

## 6. Números Grandes

A MathLg trabalha com números grandes sem limitações práticas.

```mlg
mostre "=== 6. NUMEROS GRANDES ==="
mostre 1000000 * 1000000
mostre 999999 + 1
```

> **O que acontece:** 1000000000000 (um milhão ao quadrado) e 1000000 (milhão). Não há estouro de precisão para inteiros neste domínio.
