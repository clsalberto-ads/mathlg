# Tutorial 04: Funções Definidas pelo Usuário

Este tutorial ensina como criar e usar suas próprias funções na MathLg. Funções permitem encapsular cálculos e reutilizá-los com diferentes argumentos, tornando o código mais modular e organizado.

> **Regra importante:** o corpo da função deve estar na **mesma linha** que a definição, pois a MathLg processa uma linha por vez.

## 1. Função com Um Parâmetro

A sintaxe para definir uma função é `funcao nome(parametro): corpo`. O valor de retorno é especificado com `retorna`.

```mlg
mostre "=== 1. FUNCAO SIMPLES ==="
funcao dobro(x): retorna x * 2
mostre dobro(5)
mostre dobro(10)
mostre dobro(-3)
```

> **O que acontece:** a função `dobro(x)` retorna `x * 2`. Chamando com 5 retorna 10, com 10 retorna 20, e com -3 retorna -6.

## 2. Função com Dois Parâmetros

Funções podem receber múltiplos parâmetros separados por vírgula.

```mlg
mostre "=== 2. DOIS PARAMETROS ==="
funcao soma(a, b): retorna a + b
mostre soma(3, 4)
mostre soma(10, 20)
mostre soma(-5, 5)
```

> **O que acontece:** a função `soma(a, b)` retorna a soma dos dois argumentos: 3+4 = 7, 10+20 = 30, -5+5 = 0.

## 3. Composição (Função Chamando Função)

Funções podem chamar outras funções, permitindo construir comportamentos complexos a partir de blocos simples.

```mlg
mostre "=== 3. COMPOSICAO ==="
funcao quadrado(n): retorna n * n
funcao soma_quad(a, b): retorna quadrado(a) + quadrado(b)
mostre soma_quad(3, 4)
```

> **O que acontece:** `soma_quad(3, 4)` chama `quadrado(3)` = 9 e `quadrado(4)` = 16, retornando 9 + 16 = 25. É o teorema de Pitágoras para os catetos 3 e 4.

## 4. Função Matemática

Use funções para implementar fórmulas matemáticas, como a área de um círculo.

```mlg
mostre "=== 4. FUNCAO MATEMATICA ==="
funcao area_circulo(r): retorna 3.14159 * (r * r)
mostre area_circulo(5)
mostre area_circulo(10)
```

> **O que acontece:** a área de um círculo de raio 5 é aproximadamente 78.53975, e de raio 10 é aproximadamente 314.159.

## 5. Função com Expressão Complexa

Funções podem conter expressões com múltiplos operadores, como a fórmula de Bhaskara (cálculo do delta).

```mlg
mostre "=== 5. EXPRESSAO COMPLEXA ==="
funcao delta(a, b, c): retorna (b * b) - (4 * a * c)
mostre delta(1, 5, 6)
mostre delta(1, -5, 6)
mostre delta(2, 4, 2)
```

> **O que acontece:** para a equação x² + 5x + 6, delta = 25 - 24 = 1. Para x² - 5x + 6, delta = 25 - 24 = 1. Para 2x² + 4x + 2, delta = 16 - 16 = 0.

## 6. Função com If/Else Inline

Funções podem usar a estrutura condicional `se ... senao` para tomar decisões.

```mlg
mostre "=== 6. FUNCAO COM IF/ELSE ==="
funcao absoluto(n): se n < 0: retorna -n senao: retorna n
mostre absoluto(-5)
mostre absoluto(3)
```

> **O que acontece:** se o argumento for negativo, retorna seu valor positivo (`-n`); caso contrário, retorna o próprio `n`. `absoluto(-5)` = 5 e `absoluto(3)` = 3.

## 7. Conversão de Temperatura

Um exemplo prático: converter graus Celsius para Fahrenheit.

```mlg
mostre "=== 7. CONVERSAO ==="
funcao c_para_f(c): retorna (c * 9 / 5) + 32
mostre c_para_f(0)
mostre c_para_f(100)
mostre c_para_f(30)
```

> **O que acontece:** 0 °C = 32.0 °F (ponto de congelamento), 100 °C = 212.0 °F (ponto de ebulição) e 30 °C = 86.0 °F.

## 8. Função Sem Return

Uma função pode executar uma ação sem retornar valor, usando apenas o comando `mostre` para exibir um resultado.

```mlg
mostre "=== 8. SEM RETURN ==="
funcao mostra_dobro(x): mostre x * 2
mostra_dobro(7)
```

> **O que acontece:** a função `mostra_dobro(x)` exibe o dobro do valor diretamente com `mostre`, sem usar `retorna`. Ao chamar com 7, o resultado 14 é impresso na tela.
