# Tutorial 02: Funções Matemáticas Avançadas

Este tutorial apresenta as funções matemáticas embutidas da MathLg: raiz quadrada, potência, seno, cosseno, logaritmo, valor absoluto e arredondamento. Você também verá como combiná-las em expressões.

## 1. Raiz Quadrada

A função `raiz quadrada de` calcula a raiz quadrada de um número. Pode ser usada com expressões e funções aninhadas.

```mlg
mostre "=== 1. RAIZ QUADRADA ==="
mostre raiz quadrada de 144
mostre raiz quadrada de 2
mostre raiz quadrada de 0
mostre raiz quadrada de (9 mais 16)
mostre raiz quadrada de (raiz quadrada de 16)
```

> **O que acontece:** A raiz de 144 é 12.0, de 2 é aproximadamente 1.4142, de 0 é 0.0. A expressão `sqrt(9+16)` = sqrt(25) = 5.0. Raízes aninhadas: `sqrt(sqrt(16))` = sqrt(4.0) = 2.0.

## 2. Potência

A função `potencia de ... elevado a` eleva um número a outro.

```mlg
mostre "=== 2. POTENCIA ==="
mostre potencia de 2 elevado a 3
mostre potencia de 5 elevado a 2
mostre potencia de 10 elevado a 0
mostre potencia de 2 elevado a 10
mostre potencia de (2+1) elevado a 2
```

> **O que acontece:** 2³ = 8, 5² = 25, 10⁰ = 1, 2¹⁰ = 1024. Expressões entre parênteses são avaliadas primeiro: `(2+1)²` = 3² = 9.

## 3. Seno e Cosseno

As funções `seno de` e `cosseno de` operam em radianos.

```mlg
mostre "=== 3. SENO E COSSENO ==="
mostre seno de 0
mostre seno de 1
mostre cosseno de 0
mostre cosseno de 1
```

> **O que acontece:** sen(0) = 0.0, sen(1) ≈ 0.8414, cos(0) = 1.0, cos(1) ≈ 0.5403.

## 4. Logaritmo Natural

A função `logaritmo de` (ou o atalho `log de`) calcula o logaritmo natural (base e).

```mlg
mostre "=== 4. LOGARITMO ==="
mostre logaritmo de 1
mostre logaritmo de 100
mostre log de 10
```

> **O que acontece:** ln(1) = 0.0, ln(100) ≈ 4.6052, ln(10) ≈ 2.3026. O atalho `log de` funciona como sinônimo.

## 5. Valor Absoluto

A função `valor absoluto de` retorna o valor absoluto (módulo) de um número.

```mlg
mostre "=== 5. VALOR ABSOLUTO ==="
mostre valor absoluto de -10
mostre valor absoluto de 5
mostre valor absoluto de 0
mostre valor absoluto de -3.14
```

> **O que acontece:** |-10| = 10, |5| = 5, |0| = 0, |-3.14| = 3.14. A função remove o sinal negativo, se houver.

## 6. Arredondamento

A função `arredondar` arredonda um número decimal para o inteiro mais próximo.

```mlg
mostre "=== 6. ARREDONDAMENTO ==="
mostre arredondar 3.7
mostre arredondar 3.2
mostre arredondar -2.7
mostre arredondar 4.5
mostre arredondar 0.0
```

> **O que acontece:** 3.7 → 4, 3.2 → 3, -2.7 → -3, 4.5 → 4 ou 5 (segundo a regra de arredondamento bancário do Python), 0.0 → 0.

## 7. Combinações de Funções

Funções podem ser combinadas livremente com operadores aritméticos e outras funções.

```mlg
mostre "=== 7. COMBINACOES ==="
mostre raiz quadrada de 144 + 3
mostre seno de 0 + cosseno de 0
mostre potencia de 2 elevado a 3 - 1
mostre valor absoluto de (-10+3)
mostre raiz de (potencia de 3 elevado a 2)
```

> **O que acontece:** `sqrt(144) + 3` = 12.0 + 3 = 15.0, `sen(0) + cos(0)` = 0.0 + 1.0 = 1.0, `2³ - 1` = 8 - 1 = 7, `|-10+3|` = |-7| = 7, `sqrt(3²)` = sqrt(9) = 3.0. Perceba que `raiz` é um atalho para `raiz quadrada`.
