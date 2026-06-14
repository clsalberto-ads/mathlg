# Tutorial 05: Controle de Fluxo (Condicionais e Loops)

Este tutorial ensina como controlar o fluxo de execução do programa usando condicionais (`se`/`senao`) e loops (`enquanto`/`para`). O corpo dos blocos deve estar na **mesma linha** que a condição, com comandos separados por espaço.

## 1. Condicional IF Simples

O `se` executa um comando apenas se a condição for verdadeira. A sintaxe é `se condicao: comando`.

```mlg
mostre "=== 1. IF SIMPLES ==="
x = 10
se x > 5: mostre "x > 5"                 # executa: x > 5
se x > 20: mostre "x > 20"               # nao executa
```

> **O que acontece:** A condição `x > 5` é verdadeira, então `"x > 5"` é exibido. Já `x > 20` é falso, então nada é mostrado. O `se` só executa o comando quando a condição é verdadeira.

## 2. Condicional IF/ELSE

O `se`/`senao` executa um comando quando a condição é verdadeira e outro quando é falsa.

```mlg
mostre "=== 2. IF/ELSE ==="
nota = 6
se nota >= 7: mostre "aprovado" senao: mostre "reprovado"   # reprovado

nota = 8
se nota >= 7: mostre "aprovado" senao: mostre "reprovado"   # aprovado
```

> **O que acontece:** Com `nota = 6`, a condição `nota >= 7` é falsa, então o branch `senao` executa e exibe `"reprovado"`. Com `nota = 8`, a condição é verdadeira e exibe `"aprovado"`.

## 3. IF com Atribuição

O `se` também pode executar atribuições de variáveis no corpo.

```mlg
mostre "=== 3. IF COM ATRIBUICAO ==="
saldo = 100
taxa = 0
se saldo > 50: taxa = 10
mostre taxa                              # 10

saldo = 30
taxa = 0
se saldo > 50: taxa = 10
mostre taxa                              # 0
```

> **O que acontece:** Quando `saldo > 50` é verdadeiro, `taxa` recebe 10. Quando é falso, `taxa` permanece 0. Isso permite definir valores condicionalmente de forma concisa.

## 4. IF/ELSE com Atribuição

Podemos combinar `se`/`senao` com atribuições para escolher um valor entre duas opções.

```mlg
mostre "=== 4. IF/ELSE ATRIBUICAO ==="
idade = 17
status = ""
se idade >= 18: status = "adulto" senao: status = "menor"
mostre status                            # menor

idade = 21
se idade >= 18: status = "adulto" senao: status = "menor"
mostre status                            # adulto
```

> **O que acontece:** A variável `status` recebe `"adulto"` se `idade >= 18`, ou `"menor"` caso contrário. É uma forma direta de atribuir valores diferentes baseados em uma condição.

## 5. IF com Operadores Lógicos

Condições podem usar operadores lógicos como `and` (e) para combinar múltiplas expressões.

```mlg
mostre "=== 5. IF LOGICO ==="
idade = 20
tem_carteira = verdadeiro
se idade > 18 and tem_carteira: mostre "pode dirigir" senao: mostre "nao pode"
# saida: pode dirigir
```

> **O que acontece:** Ambas as condições precisam ser verdadeiras: `idade > 18` (verdadeiro) **e** `tem_carteira` (verdadeiro). Como ambas são verdadeiras, o resultado é `"pode dirigir"`. Se qualquer uma fosse falsa, o `senao` executaria.

## 6. Loop Enquanto (While)

O `enquanto` repete um comando enquanto a condição for verdadeira. Sintaxe: `enquanto condicao: comando`.

```mlg
mostre "=== 6. LOOP ENQUANTO ==="
cont = 0
enquanto cont < 5: cont = cont + 1
mostre cont                              # 5

soma = 0
i = 1
enquanto i <= 10: soma = soma + i i = i + 1
mostre soma                              # 55
```

> **O que acontece:** No primeiro exemplo, `cont` incrementa de 0 até 5, quando a condição `cont < 5` se torna falsa. No segundo, o loop soma os números de 1 a 10, resultando em 55. Múltiplos comandos no corpo são separados por espaço.

## 7. Loop Para (For)

O `para` itera sobre uma faixa de valores. Sintaxe: `para var = inicio ate fim: comando`.

```mlg
mostre "=== 7. LOOP PARA ==="
para i = 1 ate 5: mostre i              # 1, 2, 3, 4, 5

tab = 7
para i = 1 ate 10: mostre tab * i       # 7, 14, ..., 70
```

> **O que acontece:** O primeiro loop exibe os números de 1 a 5. O segundo calcula e exibe a tabuada do 7 multiplicando cada número de 1 a 10 pela variável `tab`.

## 8. Exemplos Práticos com Loop

Aplicações reais usando loops para algoritmos clássicos.

```mlg
mostre "=== 8. EXEMPLOS PRATICOS ==="

n = 6
fat = 1
i = 1
enquanto i <= n: fat = fat * i i = i + 1
mostre fat                              # 720

base = 2
exp = 5
res = 1
i = 0
enquanto i < exp: res = res * base i = i + 1
mostre res                              # 32

n_reg = 5
enquanto n_reg > 0: mostre n_reg n_reg = n_reg - 1
# saida: 5, 4, 3, 2, 1
```

> **O que acontece:** O primeiro exemplo calcula o fatorial de 6 (6! = 720). O segundo calcula 2⁵ = 32 usando multiplicação repetida. O terceiro faz uma contagem regressiva de 5 até 1, exibindo cada valor.
