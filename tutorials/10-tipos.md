# Tutorial 10: Sistema de Tipos

Entenda os tipos de dados suportados pelo MathLg: inteiros, decimais, textos (strings) e valores lógicos (booleanos). Aprenda também a usar a função `tipo()` para descobrir o tipo de qualquer valor ou expressão.

---

## 1. Tipo Inteiro

Números inteiros não possuem casa decimal. Em MathLg, qualquer número sem ponto é automaticamente tratado como inteiro.

```mlg
mostre "=== 1. TIPO INTEIRO ==="
a = 42
mostre a                           # 42
mostre tipo(a)                     # inteiro

b = -10
mostre tipo(b)                     # inteiro

c = 0
mostre tipo(c)                     # inteiro
```

> **O que acontece:** Os valores `42`, `-10` e `0` são todos do tipo `inteiro`. Note que números negativos e o zero também são inteiros válidos.

---

## 2. Tipo Decimal

Números decimais possuem ponto flutuante e representam valores com casas decimais.

```mlg
mostre "=== 2. TIPO DECIMAL ==="
pi = 3.14159
mostre pi                          # 3.14159
mostre tipo(pi)                    # decimal

gravidade = 9.8
mostre tipo(gravidade)             # decimal
```

> **O que acontece:** `3.14159` (pi) e `9.8` (aceleração da gravidade) são do tipo `decimal`. Qualquer número que contenha um ponto decimal é classificado como decimal.

---

## 3. Tipo Texto (String)

Textos são sequências de caracteres delimitadas por aspas duplas.

```mlg
mostre "=== 3. TIPO TEXTO ==="
nome = "MathLg"
mostre nome                        # MathLg
mostre tipo(nome)                  # texto

saudacao = "Ola, mundo!"
mostre saudacao                    # Ola, mundo!
mostre tipo(saudacao)              # texto
```

> **O que acontece:** Tanto `"MathLg"` quanto `"Ola, mundo!""` são do tipo `texto`. Strings podem conter letras, números, espaços e outros caracteres.

---

## 4. Tipo Lógico (Booleano)

Valores lógicos representam verdadeiro ou falso, usados principalmente em condições e comparações.

```mlg
mostre "=== 4. TIPO LOGICO ==="
v = verdadeiro
mostre v                           # True
mostre tipo(v)                     # lógico

f = falso
mostre f                           # False
mostre tipo(f)                     # lógico
```

> **O que acontece:** `verdadeiro` e `falso` são os dois únicos valores do tipo `lógico`. São equivalentes aos booleanos `True` e `False` de outras linguagens.

---

## 5. Tipo de Expressões

A função `tipo()` também pode ser aplicada a expressões, revelando o tipo do resultado antes mesmo de ele ser calculado.

```mlg
mostre "=== 5. TIPO DE EXPRESSOES ==="
mostre tipo(42)                    # inteiro
mostre tipo(3.14)                  # decimal
mostre tipo("texto")               # texto
mostre tipo(verdadeiro)            # lógico
mostre tipo(2 + 3)                 # inteiro
mostre tipo(10 / 2)                # decimal (divisao sempre float)
mostre tipo(10 > 5)                # lógico
mostre tipo(raiz de 144)          # decimal
```

> **O que acontece:** Expressões aritméticas mantêm o tipo dos operandos (`2 + 3` é `inteiro`), mas a divisão sempre produz `decimal` mesmo com divisão exata. Comparações (`10 > 5`) resultam em `lógico`. Funções matemáticas como `raiz de` também retornam `decimal`.
