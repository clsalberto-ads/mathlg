# MathLg — Linguagem Matemática em Linguagem Natural

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-110%20passing-brightgreen)

**MathLg** é uma linguagem de programação especializada em operações matemáticas que interpreta comandos em **linguagem natural** (português e inglês). Digite expressões como você pensa: `"raiz quadrada de 144 mais 3"` e obtenha o resultado imediatamente.

```bash
pip install mathlg
mathlg
>> 2 mais 3
5
>> raiz quadrada de 144
12.0
>> sair
```

> **Propósito acadêmico:** MathLg foi criada como projeto de faculdade para demonstrar conceitos de compiladores, parsing, AST (Árvore Sintática Abstrata) e interpretação de linguagens — com o diferencial de interface em linguagem natural.

---

## Índice

- [Instalação](#instalação)
- [Início Rápido](#início-rápido)
- [Modos de Uso](#modos-de-uso)
- [Operações Suportadas](#operações-suportadas)
- [Estrutura da Linguagem](#estrutura-da-linguagem)
- [Tutoriais](#tutoriais)
- [Arquitetura](#arquitetura)
- [Desenvolvimento](#desenvolvimento)
- [Licença](#licença)

---

## Instalação

### Via pip (recomendado)

```bash
pip install mathlg
```

### Via fonte

```bash
git clone https://github.com/seu-usuario/mathlg.git
cd mathlg
pip install -e .
```

### Dependências

**Runtime:** zero dependências externas. Python puro.

**Desenvolvimento:** `pytest`, `ruff`, `mypy`

```bash
pip install -r requirements.txt
```

---

## Início Rápido

### 1. REPL Interativo

Execute `mathlg` no terminal para abrir o REPL (Read-Eval-Print Loop):

```bash
mathlg
```

Digite expressões e veja os resultados imediatamente:

```
>> 2 mais 3
5
>> 10 menos 4 vezes 2
2
>> raiz quadrada de 144
12.0
>> x = 10
10
>> x mais 5
15
>> sair
```

### 2. Executar Arquivo .mlg

Crie um arquivo com extensão `.mlg` e execute:

```bash
echo "2 mais 3" > exemplo.mlg
mathlg exemplo.mlg
```

### 3. Modo Inglês

```bash
mathlg --lang=en
```

```
>> 2 plus 3
5
>> square root of 144
12.0
>> exit
```

---

## Modos de Uso

| Comando | Descrição |
|---------|-----------|
| `mathlg` | REPL interativo em português (padrão) |
| `mathlg --lang=en` | REPL em inglês |
| `mathlg arquivo.mlg` | Executa arquivo `.mlg` |
| `mathlg --export csv` | REPL com exportação CSV habilitada |
| `mathlg --help` | Ajuda completa |

---

## Operações Suportadas

### Operações Básicas

| Português | Inglês | Símbolo | Exemplo | Resultado |
|-----------|--------|---------|---------|-----------|
| `mais` | `plus` | `+` | `2 mais 3` | `5` |
| `menos` | `minus` | `-` | `10 menos 4` | `6` |
| `vezes` / `multiplicado por` | `times` / `multiplied by` | `*` | `7 vezes 6` | `42` |
| `dividido por` | `divided by` | `/` | `20 / 4` | `5.0` |

### Funções Matemáticas

| Português | Inglês | Exemplo | Resultado |
|-----------|--------|---------|-----------|
| `raiz quadrada de` | `square root of` / `sqrt` | `raiz quadrada de 144` | `12.0` |
| `potencia de ... elevado a` | `power of ... to the power of` | `potencia de 2 elevado a 3` | `8` |
| `seno de` | `sine of` / `sin` | `seno de 0` | `0.0` |
| `cosseno de` | `cosine of` / `cos` | `cosseno de 0` | `1.0` |
| `logaritmo de` / `log de` | `logarithm of` / `log` | `logaritmo de 1` | `0.0` |
| `valor absoluto de` | `absolute value of` / `abs` | `valor absoluto de -10` | `10` |
| `arredondar` | `round` | `arredondar 3.7` | `4` |

### Comparações

| Português | Inglês | Símbolo |
|-----------|--------|---------|
| `maior que` | `greater than` | `>` |
| `menor que` | `less than` | `<` |
| `igual a` | `equal to` / `equals` | — |
| `maior ou igual a` | `greater or equal to` | `>=` |
| `menor ou igual a` | `less or equal to` | `<=` |
| `diferente de` | `different from` / `not equal to` | `!=` |

### Booleanos

| Português | Inglês | Exemplo |
|-----------|--------|---------|
| `verdadeiro` / `verdade` | `true` | `10 maior que 5` → `verdadeiro` |
| `falso` | `false` | `3 maior que 10` → `falso` |
| `e` | `and` | `verdadeiro e falso` → `falso` |
| `ou` | `or` | `verdadeiro ou falso` → `verdadeiro` |
| `nao` | `not` | `nao verdadeiro` → `falso` |

---

## Estrutura da Linguagem

### Variáveis

```python
x = 10
preco = 49.90
nome = "Matematica"
resultado = x mais 5       # 15
x = x mais 1               # incremento: 11
```

### Funções

```python
funcao dobro(x): retorna x vezes 2
dobro(5)                   # 10

funcao soma(a, b): retorna a mais b
soma(3, 4)                 # 7
```

### Condicionais

```python
se x maior que 10: mostre "grande"
se x maior que 10: mostre "grande" senao: mostre "pequeno"
```

### Loops

```python
# While
contador = 0
enquanto contador menor que 5:
  contador = contador mais 1

# For
para i = 1 ate 10: mostre i
```

### Tipos de Dados

| Tipo | Exemplo | Descrição |
|------|---------|-----------|
| `inteiro` | `42` | Número inteiro |
| `decimal` | `3.14` | Ponto flutuante |
| `texto` | `"Olá"` | String |
| `lógico` | `verdadeiro` | Booleano |

### Exportação

```python
exportar csv     # Exporta histórico como CSV
exportar json    # Exporta histórico como JSON
```

---

## Tutoriais

O diretório [`tutorials/`](tutorials/) contém exemplos práticos de todas as operações:

| Tutorial | Arquivo | Assunto |
|----------|---------|---------|
| 01 | [`01-operacoes-basicas.mlg`](tutorials/01-operacoes-basicas.mlg) | Operações básicas (+, -, *, /) |
| 02 | [`02-operacoes-avancadas.mlg`](tutorials/02-operacoes-avancadas.mlg) | Funções matemáticas (sqrt, sin, cos, log) |
| 03 | [`03-variaveis.mlg`](tutorials/03-variaveis.mlg) | Variáveis e atribuição |
| 04 | [`04-funcoes.mlg`](tutorials/04-funcoes.mlg) | Funções definidas pelo usuário |
| 05 | [`05-controle-de-fluxo.mlg`](tutorials/05-controle-de-fluxo.mlg) | Condicionais e loops |
| 06 | [`06-comparacoes-booleanos.mlg`](tutorials/06-comparacoes-booleanos.mlg) | Comparações e lógica booleana |
| 07 | [`07-exportacao.mlg`](tutorials/07-exportacao.mlg) | Exportação CSV/JSON |
| 08 | [`08-ingles.mlg`](tutorials/08-ingles.mlg) | Uso em inglês |
| 09 | [`09-exemplos-completos.mlg`](tutorials/09-exemplos-completos.mlg) | Programas completos (IMC, Fibonacci, Bhaskara) |

Para executar um tutorial:

```bash
mathlg tutorial/01-operacoes-basicas.mlg
```

Ou abra o REPL e digite os comandos manualmente.

---

## Arquitetura

```
mathlg/
├── cli/              # Interface de linha de comando
│   ├── repl.py       # REPL interativo
│   ├── runner.py     # Executor de arquivos .mlg
│   └── config.py     # Parsing de argumentos (argparse)
├── lang/             # Núcleo da linguagem
│   ├── tokenizer.py  # Tokenizador (texto → tokens)
│   ├── parser.py     # Parser descendente recursivo (tokens → AST)
│   ├── ast_nodes.py  # Definição dos nós da AST
│   └── tokens.py     # Tipos de token
├── semantic/         # Análise semântica
│   ├── analyzer.py   # Type checking + resolução de escopo
│   └── errors.py     # Hierarquia de exceções
├── interpreter/      # Interpretador
│   ├── evaluator.py  # Avaliador (AST → valores)
│   ├── environment.py# Ambiente (escopo de variáveis)
│   └── builtins.py   # Funções nativas
├── math/             # Motor matemático
│   ├── engine.py     # Operações (+,-,*,/, sqrt, sin, cos, ...)
│   └── types.py      # Sistema de tipos (MathLgType)
├── i18n/             # Internacionalização
│   ├── manager.py    # Gerenciador de idiomas
│   ├── pt_br.py      # Dicionário português (94+ keywords)
│   └── en.py         # Dicionário inglês (97+ keywords)
├── export/           # Exportação de resultados
│   ├── csv_exporter.py
│   └── json_exporter.py
└── tests/            # Testes (110 testes, 100% passing)
    ├── test_tokenizer.py
    ├── test_parser.py
    ├── test_evaluator.py
    ├── test_semantic.py
    ├── test_integration.py
    └── test_export.py
```

**Fluxo de execução:**

```
Texto: "raiz quadrada de 144 mais 3"
  ↓ tokenizer
Tokens: [SQRT, NUMBER(144), PLUS, NUMBER(3)]
  ↓ parser
AST: BinaryOp(PLUS, MathFn(SQRT, 144), 3)
  ↓ semantic analyzer
AST anotada (type checking, escopo)
  ↓ evaluator
Resultado: 12.0 + 3 = 15.0
```

---

## Desenvolvimento

### Rodar testes

```bash
pytest                          # Todos os testes
pytest -v                       # Modo verboso
pytest mathlg/tests/test_tokenizer.py  # Apenas tokenizador
pytest --cov=mathlg             # Com cobertura
```

### Verificar tipagem

```bash
mypy mathlg
```

### Verificar estilo

```bash
ruff check mathlg
```

### 110 testes, 100% passando

```
$ pytest -v
============================= 110 passed in 0.17s ==============================
```

---

## Licença

MIT — livre para uso, estudo, modificação e distribuição.

---

## Sobre

Projeto acadêmico de faculdade. Construído com Python puro para demonstrar conceitos de:

- **Tokenização** (regex + pattern matching)
- **Parsing** (recursive descent manual)
- **AST** (Abstract Syntax Tree)
- **Análise semântica** (type checking)
- **Interpretação** (tree-walking evaluator)
- **Internacionalização** (dicionários de keywords comutáveis)

---

*"Digite como você pensa. Calcule como você precisa."*
