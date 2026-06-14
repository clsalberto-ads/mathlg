# Tutorial 09: Programas Completos

Combine todos os recursos da linguagem MathLg em programas funcionais que resolvem problemas reais. Este tutorial demonstra desde uma calculadora de IMC até algoritmos clássicos como Fibonacci, Bhaskara e fatorial.

---

## 1. Calculadora de IMC

Calcula o Índice de Massa Corporal (IMC) a partir do peso e altura, classificando o resultado em categorias como "Abaixo do peso", "Peso normal", "Sobrepeso" ou "Obesidade".

```mlg
mostre "=== PROGRAMA 1: IMC ==="
peso = 70
altura = 1.75
imc = peso / (altura * altura)
mostre imc
se imc < 18.5: mostre "Abaixo do peso"
se imc >= 18.5 and imc < 25: mostre "Peso normal"
se imc >= 25 and imc < 30: mostre "Sobrepeso"
se imc >= 30: mostre "Obesidade"
```

> **O que acontece:** com `peso = 70` e `altura = 1.75`, o IMC calculado é `22.86`, classificado como "Peso normal". O programa usa condicionais encadeadas (`se`) para determinar a faixa.

---

## 2. Equação do Segundo Grau (Bhaskara)

Resolve equações de segundo grau da forma `ax² + bx + c = 0` usando a fórmula de Bhaskara, com funções auxiliares para calcular delta e sua raiz.

```mlg
mostre "=== PROGRAMA 2: BHASKARA ==="
funcao delta(a, b, c): retorna (b * b) - (4 * a * c)
funcao raiz_delta(a, b, c): se delta(a, b, c) < 0: retorna -1 senao: retorna raiz quadrada de delta(a, b, c)
funcao bhaskara(a, b, c): se delta(a, b, c) < 0: mostre "sem raizes" senao: mostre (-b + raiz_delta(a, b, c)) / (2 * a) mostre (-b - raiz_delta(a, b, c)) / (2 * a)

mostre "x² - 5x + 6 = 0"
bhaskara(1, -5, 6)                # x1=3, x2=2

mostre "x² - 4 = 0"
bhaskara(1, 0, -4)                # x1=2, x2=-2
```

> **O que acontece:** Para `x² - 5x + 6 = 0`, as raízes são `3` e `2`. Para `x² - 4 = 0`, as raízes são `2` e `-2`. O programa demonstra funções que chamam outras funções (`bhaskara` chama `raiz_delta` que chama `delta`).

---

## 3. Números Primos

Verifica se um número é primo testando divisibilidade por candidatos até a raiz quadrada do número.

```mlg
mostre "=== PROGRAMA 3: PRIMOS ==="
funcao eh_primo(n): se n < 2: retorna falso i = 2 enquanto i * i <= n: se n - (n / i * i) == 0: retorna falso i = i + 1 retorna verdadeiro

mostre eh_primo(7)                 # True
mostre eh_primo(10)                # False
mostre eh_primo(2)                 # True
mostre eh_primo(1)                 # False
mostre eh_primo(17)                # True
```

> **O que acontece:** A função `eh_primo` retorna `verdadeiro` apenas para números primos: `7`, `2` e `17` são primos; `10` e `1` não são. O algoritmo usa um laço `enquanto` que testa divisores até a raiz quadrada de `n`, e detecta a divisibilidade verificando se `n - (n / i * i) == 0` (equivalente ao operador `%` de outras linguagens).

---

## 4. Fibonacci Recursivo

Gera o enésimo termo da sequência de Fibonacci usando recursão: `fib(n) = fib(n-1) + fib(n-2)`.

```mlg
mostre "=== PROGRAMA 4: FIBONACCI ==="
funcao fib(n): se n <= 1: retorna n senao: retorna fib(n-1) + fib(n-2)
mostre fib(0)                      # 0
mostre fib(1)                      # 1
mostre fib(5)                      # 5
mostre fib(10)                     # 55
```

> **O que acontece:** `fib(0) = 0`, `fib(1) = 1`, `fib(5) = 5`, `fib(10) = 55`. A sequência gerada é `0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55...`. Cada chamada recursiva desdobra-se em duas novas chamadas até atingir os casos base.

---

## 5. Conversão de Temperatura

Converte temperaturas entre Celsius e Fahrenheit usando fórmulas matemáticas.

```mlg
mostre "=== PROGRAMA 5: TEMPERATURA ==="
funcao c_to_f(c): retorna (c * 9 / 5) + 32
funcao f_to_c(f): retorna (f - 32) * 5 / 9
mostre "0C = " c_to_f(0)          # 32.0
mostre "100C = " c_to_f(100)      # 212.0
mostre "98.6F = " f_to_c(98.6)    # 37.0
```

> **O que acontece:** `0°C = 32°F`, `100°C = 212°F` (ponto de ebulição), `98.6°F = 37°C` (temperatura corporal). As funções demonstram expressões aritméticas com parênteses para controlar a precedência.

---

## 6. Fatorial

Calcula o fatorial de um número de duas formas: recursiva e iterativa (com laço `enquanto`).

```mlg
mostre "=== PROGRAMA 6: FATORIAL ==="
funcao fatorial(n): se n <= 1: retorna 1 senao: retorna n * fatorial(n-1)
mostre fatorial(0)                 # 1
mostre fatorial(5)                 # 120
mostre fatorial(10)                # 3628800

funcao fatorial_while(n): res = 1 i = 1 enquanto i <= n: res = res * i i = i + 1 retorna res
mostre fatorial_while(5)           # 120
mostre fatorial_while(7)           # 5040
```

> **O que acontece:** `5! = 120`, `10! = 3628800`. A versão recursiva (`fatorial`) é mais concisa; a versão iterativa (`fatorial_while`) é mais eficiente em memória. Ambas produzem o mesmo resultado.

---

## 7. Média Aritmética

Calcula a média simples de três valores.

```mlg
mostre "=== PROGRAMA 7: MEDIA ==="
a = 8
b = 9
c = 7
media = (a + b + c) / 3
mostre media                       # 8.0
```

> **O que acontece:** `(8 + 9 + 7) / 3 = 8.0`. O resultado é decimal porque a divisão em MathLg sempre produz um número decimal.

---

## 8. Tabuada

Exibe a tabuada de multiplicação de um número usando o laço `para`.

```mlg
mostre "=== PROGRAMA 8: TABUADA ==="
n = 7
para i = 1 ate 10: mostre n * i    # 7, 14, ..., 70
```

> **O que acontece:** O laço `para i = 1 ate 10` itera de 1 a 10, multiplicando `n` por cada valor. A saída é a tabuada completa do 7.

---

## 9. Somatório

Soma todos os números inteiros de 1 até `n` usando um laço `enquanto`.

```mlg
mostre "=== PROGRAMA 9: SOMATORIO ==="
funcao somatorio(n): s = 0 i = 1 enquanto i <= n: s = s + i i = i + 1 retorna s
mostre somatorio(10)               # 55
mostre somatorio(100)              # 5050
```

> **O que acontece:** A soma de 1 a 10 é 55; a soma de 1 a 100 é 5050. Este é um exemplo clássico de acumulador com laço de repetição.
