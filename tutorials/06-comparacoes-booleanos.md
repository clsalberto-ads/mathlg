# Tutorial 06: Comparações e Booleanos

Este tutorial ensina como comparar valores usando operadores relacionais e como trabalhar com lógica booleana (`verdadeiro`/`falso`). Toda comparação retorna um valor booleano.

## 1. Comparações Numéricas

O MathLg oferece operadores textuais e simbólicos para comparar números.

```mlg
mostre "=== 1. MAIOR QUE ==="
mostre 10 > 5                          # True
mostre 5 > 10                          # False
mostre 5 > 5                           # False

mostre "=== 2. MENOR QUE ==="
mostre 3 < 10                          # True
mostre 10 < 3                          # False

mostre "=== 3. IGUAL A ==="
mostre 5 igual a 5                     # True
mostre 5 igual a 6                     # False
mostre 10 == 10                        # True (simbolo ==)

mostre "=== 4. MAIOR OU IGUAL ==="
mostre 10 >= 10                        # True
mostre 10 >= 5                         # True
mostre 5 >= 10                         # False

mostre "=== 5. MENOR OU IGUAL ==="
mostre 3 <= 3                          # True
mostre 3 <= 5                          # True
mostre 5 <= 3                          # False

mostre "=== 6. DIFERENTE ==="
mostre 10 != 5                         # True
mostre 10 != 10                        # False
```

> **O que acontece:** Cada operador compara dois números e retorna `True` ou `False`. É possível usar tanto palavras em português (`igual a`) quanto símbolos (`==`, `!=`, `>=`, `<=`). O MathLg aceita ambas as formas indistintamente.

## 2. Valores Booleanos

Os valores `verdadeiro` e `falso` são os blocos fundamentais da lógica booleana.

```mlg
mostre "=== 7. BOOLEANOS ==="
mostre verdadeiro                      # True
mostre falso                           # False
mostre verdade                         # True (sinonimo)
```

> **O que acontece:** `verdadeiro` e `verdade` são sinônimos que retornam `True`, e `falso` retorna `False`. Estes valores são usados em condições e operações lógicas.

## 3. Operador AND (E)

O `and` retorna `True` apenas quando **ambos** os operandos são verdadeiros.

```mlg
mostre "=== 8. OPERADOR AND ==="
mostre verdadeiro and verdadeiro       # True
mostre verdadeiro and falso            # False
mostre falso and verdadeiro            # False
mostre falso and falso                 # False

idade = 20
tem_carteira = verdadeiro
mostre idade > 18 and tem_carteira     # True
```

> **O que acontece:** A tabela verdade do `and` mostra que só há `True` quando todos os valores são verdadeiros. No exemplo prático, `idade > 18` (True) e `tem_carteira` (True) resultam em `True` — as duas condições precisam valer.

## 4. Operador OU (OR)

O `ou` retorna `True` quando **pelo menos um** dos operandos é verdadeiro.

```mlg
mostre "=== 9. OPERADOR OU ==="
mostre verdadeiro ou verdadeiro        # True
mostre verdadeiro ou falso             # True
mostre falso ou verdadeiro             # True
mostre falso ou falso                  # False

saldo = 0
tem_credito = verdadeiro
mostre saldo > 0 ou tem_credito        # True
```

> **O que acontece:** O `ou` só retorna `False` quando ambos os operandos são falsos. No exemplo, mesmo com `saldo = 0` (falso), `tem_credito` é verdadeiro, então o resultado é `True`.

## 5. Operador Não (NOT)

O `nao` inverte o valor booleano: `True` vira `False` e vice-versa.

```mlg
mostre "=== 10. OPERADOR NAO ==="
mostre nao verdadeiro                  # False
mostre nao falso                       # True
mostre nao (10 > 5)                    # False
mostre nao (10 < 5)                    # True
```

> **O que acontece:** `nao verdadeiro` é `False`, `nao falso` é `True`. Quando aplicado a expressões, `nao (10 > 5)` nega o resultado `True` para `False`, enquanto `nao (10 < 5)` nega `False` para `True`.

## 6. Expressões Booleanas Combinadas

Os operadores `and`, `ou` e `nao` podem ser combinados com parênteses para formar expressões complexas.

```mlg
mostre "=== 11. EXPRESSOES COMBINADAS ==="
mostre (10 > 5) and (3 < 8)            # True
mostre (10 > 5) ou (10 < 3)           # True
mostre nao (10 > 5)                   # False
mostre (10 > 5) and nao (10 < 3)      # True
```

> **O que acontece:** Parênteses definem a ordem de avaliação. `(10 > 5) and (3 < 8)` é True porque ambas as partes são verdadeiras. `(10 > 5) and nao (10 < 3)` combina `True and not False` = `True and True` = `True`.

## 7. Exemplo Prático: Aprovação

Aplicação de expressões booleanas para simular regras de negócio.

```mlg
mostre "=== 12. EXEMPLO PRATICO ==="
nota = 8
freq = 90
aprovado = nota >= 7 and freq >= 75
mostre aprovado                        # True

matricula_ativa = verdadeiro
curso_pago = verdadeiro
pode_assistir = matricula_ativa and curso_pago
mostre pode_assistir                   # True
```

> **O que acontece:** O primeiro exemplo verifica se um aluno foi aprovado: nota mínima 7 e frequência mínima 75%. O segundo verifica se um estudante pode assistir aula: matrícula ativa e curso pago. Ambos usam `and` porque todas as condições precisam ser satisfeitas.

## 8. Comparações com Operações

Comparações podem incluir expressões aritméticas completas.

```mlg
mostre "=== 13. COMPARACAO COM OPERACOES ==="
mostre (2 + 3) > 4                     # True  (5 > 4)
mostre (10 - 3) < 5                    # False (7 < 5)
mostre (6 * 2) igual a 12              # True  (12 == 12)
mostre (20 / 4) != 4                   # True  (5 != 4)
```

> **O que acontece:** As expressões dentro dos parênteses são avaliadas primeiro, depois o resultado é comparado. `(2 + 3) > 4` vira `5 > 4` (True), enquanto `(10 - 3) < 5` vira `7 < 5` (False).
