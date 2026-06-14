# Tutorial 11: Recursão

Aprenda a criar funções que chamam a si mesmas — um dos conceitos mais poderosos da programação. Toda função recursiva precisa de dois elementos: um **caso base** (que encerra a recursão) e um **caso recursivo** (onde a função chama a si mesma).

> **Atenção:** Recursão muito profunda (>1000 chamadas) pode causar estouro de pilha!

---

## 1. Fatorial

O fatorial de `n` (escrito `n!`) é o produto de todos os inteiros de 1 até `n`. Por definição, `0! = 1` e `1! = 1`.

**Caso base:** `fatorial(0) = 1`, `fatorial(1) = 1`  
**Caso recursivo:** `fatorial(n) = n * fatorial(n-1)`

```mlg
mostre "=== 1. FATORIAL ==="

funcao fatorial(n): se n <= 1: retorna 1 senao: retorna n * fatorial(n-1)

mostre fatorial(0)                 # 1
mostre fatorial(1)                 # 1
mostre fatorial(5)                 # 120
mostre fatorial(7)                 # 5040
mostre fatorial(10)                # 3628800
```

> **O que acontece:** `5! = 5 × 4 × 3 × 2 × 1 = 120`, `7! = 5040`, `10! = 3628800`. Quando `n <= 1`, a função retorna 1 (caso base); caso contrário, multiplica `n` pelo fatorial de `n-1`.

---

## 2. Fibonacci

A sequência de Fibonacci começa com 0 e 1, e cada termo subsequente é a soma dos dois anteriores.

**Caso base:** `fib(0) = 0`, `fib(1) = 1`  
**Caso recursivo:** `fib(n) = fib(n-1) + fib(n-2)`

```mlg
mostre "=== 2. FIBONACCI ==="

funcao fib(n): se n <= 1: retorna n senao: retorna fib(n-1) + fib(n-2)

mostre fib(0)                      # 0
mostre fib(1)                      # 1
mostre fib(5)                      # 5
mostre fib(10)                     # 55
mostre fib(15)                     # 610
```

> **O que acontece:** A sequência gerada é `0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610...`. `fib(15) = 610`. Note que cada chamada gera duas novas chamadas recursivas, tornando este algoritmo exponencial — ideal para valores pequenos.

---

## 3. Potência Recursiva

Calcula `b` elevado a `e` (potenciação) usando multiplicação sucessiva.

**Caso base:** `potencia(base, 0) = 1`  
**Caso recursivo:** `potencia(base, exp) = base * potencia(base, exp-1)`

```mlg
mostre "=== 3. POTENCIA RECURSIVA ==="

funcao potencia(b, e): se e == 0: retorna 1 senao: retorna b * potencia(b, e-1)

mostre potencia(2, 3)              # 8
mostre potencia(5, 0)              # 1
mostre potencia(3, 4)              # 81
```

> **O que acontece:** `2³ = 8`, `5⁰ = 1` (todo número elevado a zero é 1), `3⁴ = 81`. O caso base é quando o expoente é zero, retornando 1.

---

## 4. Somatório Recursivo

Soma todos os inteiros de 1 até `n` usando recursão, em vez de um laço.

**Caso base:** `somatorio(1) = 1`  
**Caso recursivo:** `somatorio(n) = n + somatorio(n-1)`

```mlg
mostre "=== 4. SOMATORIO ==="

funcao somatorio(n): se n <= 1: retorna 1 senao: retorna n + somatorio(n-1)

mostre somatorio(5)                # 15 = 1+2+3+4+5
mostre somatorio(10)               # 55 = 1+2+...+10
mostre somatorio(100)              # 5050
```

> **O que acontece:** A soma de 1 a 5 é 15, de 1 a 10 é 55, de 1 a 100 é 5050. Este é o mesmo problema do Tutorial 9, mas resolvido com recursão em vez de iteração.

---

## 5. Contagem Regressiva Recursiva

Exibe uma contagem regressiva de `n` até 1, demonstrando uma função recursiva com efeito colateral (impressão na tela).

```mlg
mostre "=== 5. CONTAGEM ==="

funcao contagem(n): se n < 1: retorna 0 senao: mostre n retorna contagem(n-1)

contagem(5)
# saida: 5, 4, 3, 2, 1
```

> **O que acontece:** A função imprime o valor atual de `n` antes de chamar a si mesma com `n-1`. Quando `n < 1`, retorna 0 e a recursão termina. A saída é a contagem regressiva `5, 4, 3, 2, 1`.
