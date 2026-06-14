# Tutorial 03: Variáveis e Atribuição

Este tutorial ensina como armazenar e reutilizar valores usando variáveis na MathLg. Você aprenderá atribuição, uso em expressões, reatribuição e como criar nomes descritivos para organizar seus cálculos.

## 1. Atribuição Simples

Variáveis são criadas com a sintaxe `nome = valor`. A MathLg aceita números, textos (strings) e valores booleanos.

```mlg
mostre "=== 1. ATRIBUICAO ==="
x = 10
preco = 49.90
nome = "Matematica"
logico = verdadeiro

mostre x
mostre preco
mostre nome
mostre logico
```

> **O que acontece:** as variáveis `x`, `preco`, `nome` e `logico` armazenam, respectivamente: um inteiro (10), um decimal (49.9), uma string ("Matematica") e um booleano (verdadeiro). O comando `mostre` exibe o valor armazenado.

## 2. Uso em Expressões

Variáveis podem ser usadas em expressões aritméticas como se fossem os próprios números.

```mlg
mostre "=== 2. USO EM EXPRESSOES ==="
x = 10
mostre x + 5
mostre x * 2
mostre x - 3
mostre x / 2
```

> **O que acontece:** com `x = 10`, as expressões resultam em: 15 (10+5), 20 (10*2), 7 (10-3) e 5.0 (10/2).

## 3. Reatribuição

Uma variável pode ter seu valor alterado quantas vezes for necessário. O novo valor pode ser calculado a partir do valor anterior.

```mlg
mostre "=== 3. REATRIBUICAO ==="
x = 10
x = x + 1
mostre x
x = x * 2
mostre x
x = x - 5
mostre x
x = x / 2
mostre x
```

> **O que acontece:** a variável `x` começa em 10, é incrementada para 11, depois dobrada para 22, reduzida em 5 para 17 e finalmente dividida por 2 para 8.5. Cada operação usa o valor atual de `x` para calcular o próximo.

## 4. Múltiplas Variáveis

É possível usar várias variáveis em uma mesma expressão, tornando o código mais legível.

```mlg
mostre "=== 4. MULTIPLAS VARIAVEIS ==="
a = 5
b = 10
resultado = a + b * 2
mostre resultado

total = a + b
mostre total
```

> **O que acontece:** `a + b * 2` = 5 + (10 * 2) = 25 (a multiplicação tem precedência). Já `a + b` = 15. Os nomes descritivos (`resultado`, `total`) ajudam a entender o propósito.

## 5. Variáveis em Funções Matemáticas

Variáveis podem ser passadas como argumentos para funções matemáticas como `raiz quadrada`, `potencia` e `valor absoluto`.

```mlg
mostre "=== 5. VARIAVEIS EM FUNCOES ==="
valor = 144
mostre raiz quadrada de valor

base = 2
exp = 10
mostre potencia de base elevado a exp

neg = -42
mostre valor absoluto de neg
```

> **O que acontece:** a raiz quadrada de `valor` (144) é 12.0, a potência de `base` (2) elevado a `exp` (10) é 1024, e o valor absoluto de `neg` (-42) é 42.

## 6. Exemplo Prático: Conversão de Unidades

Variáveis facilitam a conversão entre unidades de medida de forma clara e reutilizável.

```mlg
mostre "=== 6. CONVERSAO DE UNIDADES ==="
metros = 100
cm = metros * 100
mostre cm
mm = cm * 10
mostre mm
```

> **O que acontece:** 100 metros equivalem a 10000 centímetros, que por sua vez equivalem a 100000 milímetros. Cada etapa usa o resultado anterior como entrada.

## 7. Nomes Descritivos

Usar nomes descritivos para variáveis torna o código autoexplicativo, como neste exemplo de cálculo de área e perímetro de um retângulo.

```mlg
mostre "=== 7. NOMES DESCRITIVOS ==="
largura = 8
altura = 5
area = largura * altura
mostre area
perimetro = 2 * (largura + altura)
mostre perimetro
```

> **O que acontece:** a área do retângulo 8 × 5 é 40, e o perímetro calculado por `2 * (8 + 5)` é 26. Os nomes `largura`, `altura`, `area` e `perimetro` comunicam claramente o propósito de cada valor.
