# ADR-001: Stack, Arquitetura e Decisões Críticas do MathLg

**Status:** Aceito
**Data:** 2026-06-13
**Autora:** Maya Chen
**Revisores:** Viktor Ramos (CEO), Nico Ferreira (PM)

## Contexto

MathLg é uma linguagem de programação acadêmica especializada em operações
matemáticas com interface em linguagem natural (pt-BR + EN). Orçamento zero,
time de 1 desenvolvedor, prazo acadêmico. 9 features obrigatórias no MVP.

O problema central: **como fazer parsing de linguagem natural matemática em
Python puro sem morrer de complexidade?**

---

## Stack

### Python 3.12+ — SIM. Rust/ANTLR+Java — NÃO.

| Critério | Python | Rust | ANTLR + Java |
|----------|--------|------|--------------|
| Curva de aprendizado | Baixa | Alta (lifetime, borrow checker) | Média (gramática separada) |
| Velocidade de iteração | Alta | Média (compilação lenta) | Média (gera código) |
| Ecossistema NLP | Maduro (NLTK, spaCy) | Imaturo | Inexistente |
| Custo operacional | pip install | build.rs, cross-compile | JRE, toolchain |
| Adequação acadêmica | Excelente (didático) | Ruim (complexidade desnecessária) | Médio (abstração extra) |

**Motivo principal:** O objetivo do projeto é **ensinar conceitos de linguagens
de programação**, não performance de execução. Python permite que o desenvolvedor
*veja* cada camada da arquitetura funcionando. Com Rust, metade do tempo vai pra
satisfazer o compilador. Com ANTLR + Java, você terceiriza o parser e perde o
aprendizado.

**Ressalva honesta:** Python puro é mais lento para interpretação. Para uma
linguagem acadêmica rodando expressões matemáticas de centenas de operações por
execução, a diferença é irrelevante. Se um dia precisar escalar para milhões de
operações/segundo, reavaliamos. Não será o caso.

### Bibliotecas

```yaml
Dependências obrigatórias:
  - NENHUMA (core funciona sem dependências externas)

Dependências opcionais (instaladas sob demanda):
  - rich: REPL bonito com syntax highlighting (sugiro, mas não obrigatório)
  - pytest: testes (obrigatório para dev, não para runtime)
  - pytest-cov: cobertura

Dependências EXPLICITAMENTE REJEITADAS:
  ❌ spaCy — modelo de 500MB+ para linguagem natural livre. Nossa "linguagem
     natural" é semi-estruturada (gramática controlada). spaCy é canhão para
     mata-mosca.
  ❌ ANTLR — gera código em Java ou Python. Adiciona passo de build,
     dependência de JRE, e esconde a lógica de parsing do desenvolvedor.
  ❌ Lark — parser generator. Melhor que ANTLR (puro Python), mas ainda
     adiciona camada de abstração que atrapalha o entendimento acadêmico.
  ❌ PLY (yacc/lex) — yacc para Python. Mesmo problema: gera parser que
     ninguém entende sem ler a documentação do PLY.
  ❌ NumPy — não precisamos de operações vetoriais no MVP.
```

### Gerenciamento de dependências

```
Usar: pip padrão + requirements.txt
Não usar: poetry, uv (overkill para projeto de 0 dependências runtime)
```

Se em qualquer momento o projeto tiver mais de 3 dependências runtime,
reavaliamos. Até lá, `pip install -r requirements.txt` resolve.

### Estratégia de testes

```
Framework: pytest (padrão da indústria Python)
Cobertura alvo: 80%+ (linhas de código, exceto CLI boilerplate)

Estratégia:
  - Unit tests: cada camada isolada (tokenizer, parser, evaluator)
  - Integration tests: "entrada → saída" (frase em PT → resultado numérico)
  - Fixtures: arquivos .mlg com casos de teste em tests/fixtures/
  - Doctest: APENAS para documentar exemplos de funções matemáticas
    (não usar doctest como estratégia principal — não escala)
```

---

## Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLI Layer (REPL + Runner)                    │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │  repl.py      │  │  runner.py       │  │  config.py          │  │
│  │  loop read-   │  │  carrega .mlg    │  │  args (lang,        │  │
│  │  eval-print   │  │  executa linha   │  │  export flags)      │  │
│  └──────┬───────┘  └────────┬─────────┘  └──────────────────────┘  │
│         │                    │                                       │
│         │    stdin/text      │  file content                         │
└─────────┼────────────────────┼───────────────────────────────────────┘
          │                    │
          ▼                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         LEXER / TOKENIZER                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  tokenizer.py                                                  │  │
│  │                                                               │  │
│  │  Entrada: "calcule a raiz quadrada de 144 mais 3"            │  │
│  │  Saída:   [KW_CALC, KW_SQRT, NUM(144), KW_PLUS, NUM(3)]      │  │
│  │                                                               │  │
│  │  i18n: consulta dicionário pt-BR → token normalizado          │  │
│  │  regex + pattern matching → token stream                      │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
└─────────────────────────────┼────────────────────────────────────────
                              │ token stream
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         PARSER (AST Builder)                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  parser.py + ast_nodes.py                                    │  │
│  │                                                              │  │
│  │  Entrada: [KW_CALC, KW_SQRT, NUM(144), KW_PLUS, NUM(3)]     │  │
│  │  Saída:                                                      │  │
│  │    Program                                                   │  │
│  │      └── BinaryOp(+)                                         │  │
│  │            ├── UnaryOp(SQRT)                                 │  │
│  │            │     └── Literal(144)                            │  │
│  │            └── Literal(3)                                    │  │
│  │                                                              │  │
│  │  Recursive descent parser manual (sem gerador)               │  │
│  │  Gramática LL(1) para linguagem controlada                   │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
└─────────────────────────────┼────────────────────────────────────────
                              │ AST
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SEMANTIC ANALYZER                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  analyzer.py                                                  │  │
│  │                                                              │  │
│  │  - Type checking (int + float = float, string * int = erro)  │  │
│  │  - Scope resolution (variável definida antes de usar?)       │  │
│  │  - Function arity (argumentos conferem?)                     │  │
│  │  - Loop bounds (condição booleana?)                          │  │
│  │                                                              │  │
│  │  Saída: AST anotada + lista de erros semânticos              │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
└─────────────────────────────┼────────────────────────────────────────
                              │ annotated AST
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INTERPRETER / EVALUATOR                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  evaluator.py + environment.py                               │  │
│  │                                                              │  │
│  │  - Walk AST nodes, executa cada um                          │  │
│  │  - Gerencia escopo (global/local)                           │  │
│  │  - Control flow (if/while)                                  │  │
│  │  - Function call (definição + invocação)                    │  │
│  │                                                              │  │
│  │  environment.py: dict encadeado (escopo léxico, dinâmico)    │  │
│  │  builtins.py: funções nativas (print, input, type, len)     │  │
│  └──────────────────────────┬────────────────────────────────────┘  │
└─────────────────────────────┼────────────────────────────────────────
                              │ valor final
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   MATH ENGINE                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  engine.py + types.py                                        │  │
│  │                                                              │  │
│  │  - Operações básicas: +, -, *, /, //, %                     │  │
│  │  - Funções: sqrt, pow, sin, cos, log, abs, round            │  │
│  │  - math module do Python como backend (math.sqrt, etc.)     │  │
│  │  - Validação de domínio (log de negativo → erro)            │  │
│  │  - Sistema de tipos: Inteiro, Decimal, Texto, Lógico, Nulo  │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                   EXPORT LAYER                                     │
│  ┌────────────────────┐  ┌────────────────────┐                   │
│  │  csv_exporter.py   │  │  json_exporter.py  │                   │
│  │  resultados → .csv │  │  resultados → .json│                   │
│  └────────────────────┘  └────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                   I18N LAYER                                       │
│  ┌────────────────┐  ┌────────────┐  ┌────────────┐               │
│  │  manager.py    │  │  pt_br.py  │  │  en.py     │               │
│  │  (singleton)   │  │  keywords  │  │  keywords  │               │
│  └────────────────┘  └────────────┘  └────────────┘               │
│  Tokenizer consulta LangManager.current() para patterns ativos   │
└─────────────────────────────────────────────────────────────────────┘
```

### Fluxo completo de execução

```
Usuário digita:  "calcule a raiz quadrada de 144 mais 3"

1. REPL          → recebe string "calcule a raiz quadrada de 144 mais 3"
2. Tokenizer     → [
                     KW_CALC(span=0-7),
                     KW_SQRT(span=8-25),
                     NUM(144, span=29-32),
                     KW_PLUS(span=33-37),
                     NUM(3, span=38-39)
                   ]
3. Parser        → Program(
                     body=BinaryOp(
                       op=PLUS,
                       left=UnaryOp(op=SQRT, operand=Literal(144)),
                       right=Literal(3)
                     )
                   )
4. Semantic      → OK (int + int = int, sqrt(144) válido)
5. Evaluator     → sqrt(144) = 12.0 → 12.0 + 3 = 15.0
6. REPL output   → "15.0"

Com export:
5a. Evaluator → resultado = 15.0
5b. Export    → {"expression": "calcule a raiz quadrada de 144 mais 3",
                  "result": 15.0, "timestamp": "2026-06-13T10:00:00"}
                  → resultado.json
```

---

## Decisões Críticas

### 1. NLP: Regex puro + parser manual

| Abordagem | Complexidade | Flexibilidade | Performance | Didático? |
|-----------|-------------|---------------|-------------|-----------|
| Regex puro + tokenizer manual | Baixa | Baixa | Altíssima | ✅ Excelente |
| Lark/ANTLR | Média | Média | Alta | ⚠️ Esconde lógica |
| spaCy/NLTK | Alta (modelo 500MB) | Alta | Baixa | ❌ Overkill |
| Regex + recursive descent | Média | Média | Alta | ✅ Ótimo |

**Decisão:** Regex para tokenizer + recursive descent parser manual.

Nossa "linguagem natural" é controlada. O usuário não vai digitar "me ajuda aí
com a raiz daquele número". A gramática do MathLg é semi-formal:

```
<program>     ::= <statement>+
<statement>   ::= <assignment>
                 | <function_def>
                 | <loop>
                 | <conditional>
                 | <expression>
                 | <export>
<expression>  ::= <term> (("mais" | "menos" | "vezes" | "dividido por") <term>)*
<term>        ::= <number>
                 | <variable>
                 | <function_call>
                 | "raiz quadrada de" <term>
                 | "potência de" <term> "elevado a" <term>
                 | "seno de" <term>
                 | "cosseno de" <term>
                 | "logaritmo de" <term>
                 | "(" <expression> ")"
```

Isso é gramática de **contexto controlado**. Não é português livre.
Regex + parser manual é a melhor relação custo-benefício.

### 2. i18n: Dicionário de keywords comutável

**Decisão:** Tokenizer consulta dicionário configurável. Parser trabalha com
tokens normalizados (sempre em inglês).

```
Internamente a linguagem usa tokens em inglês (KW_PLUS, KW_SQRT, etc.).
O tokenizer consulta o dicionário do idioma ativo e traduz para tokens
normalizados.

Vantagens:
  - Parser não sabe nem precisa saber em que idioma o usuário digitou
  - Adicionar novo idioma = novo dicionário, sem tocar no parser
  - Comutável em runtime: "/idioma ingles" ou "/language portuguese"
```

**O que NÃO fazer:** Não criar dois parsers. Não duplicar gramática.

### 3. REPL: `input()` puro no MVP

**Decisão:** `input()` puro. prompt_toolkit adiciona dependência para ganho
cosmético. Substituir depois se/quando histórico e autocomplete forem
necessários.

### 4. Tratamento de erros

**Decisão:** Hierarquia de exceções específica do MathLg.

```python
class MathLgError(Exception):
    """Base para todos os erros da linguagem."""

class LexerError(MathLgError):
    """Erro de tokenização (caractere inválido, etc.)."""

class ParserError(MathLgError):
    """Erro de sintaxe (expressão mal formada)."""

class SemanticError(MathLgError):
    """Erro semântico (tipo incompatível, variável não definida)."""

class RuntimeError(MathLgError):
    """Erro em tempo de execução (divisão por zero, log de negativo)."""
```

---

## O que NÃO vamos construir no MVP

| Funcionalidade | Motivo |
|---------------|--------|
| ❌ Debugger visual | Exige servidor web, protocolo DAP, UI — complexidade imensa para 0 valor acadêmico |
| ❌ IDE / LSP | LSP exige servidor background, JSON-RPC, integração VS Code — complexidade desnecessária |
| ❌ Compilador JIT (Numba, LLVM) | Otimização para problema que não temos. Sem benchmark, sem otimização. |
| ❌ Package manager / módulos | Tudo no escopo global no MVP. Import resolve depois. |
| ❌ Listas, dicts, tuplas | Requisito do MVP é int, float, string, bool apenas |
| ❌ Tipagem dinâmica avançada | Type checking básico resolve o MVP. Hindley-Milner fica para depois. |
| ❌ Concorrência / async | Zero casos de uso em operações matemáticas sequenciais |

---

## Estimativa de Esforço

| Camada | Esforço | Risco | Depende de |
|--------|---------|-------|------------|
| Tokenizer | Médio | 🟡 Edge cases de language natural | Nada |
| Parser | **Alto** | 🔴 Precedência, aninhamento, ambiguidade | Tokenizer |
| AST Nodes | Baixo | 🟢 Dataclasses simples | Nada |
| Semantic Analyzer | Médio | 🟡 Escopo, tipos | Parser + AST |
| Evaluator | Médio | 🟡 Control flow | Semantic |
| Environment | Baixo | 🟢 Dict encadeado | Nada |
| Math Engine | Baixo | 🟢 Wrapper de math.* | Types |
| REPL | Baixo | 🟢 input() loop | Evaluator |
| File Runner | Baixo | 🟢 read + exec | Evaluator |
| i18n | Baixo | 🟢 Dicionários | Tokenizer |
| Export | Baixo | 🟢 CSV/JSON | Evaluator |
| CLI (argparse) | Baixo | 🟢 Boilerplate | Nada |
| Testes | **Alto** | 🟡 Cobertura de edge cases | Todas |

**Total estimado: 2-3 semanas (1 dev full-time)**

| Período | Foco |
|---------|------|
| Semana 1 | Tokenizer + Parser + AST + Testes |
| Semana 2 | Evaluator + Environment + Math Engine + Semantic |
| Semana 3 | REPL + i18n + Export + CLI + Integração + Polish |

---

## Referências

- Pratt Parsing (Top-Down Operator Precedence) — Vaughan Pratt, 1973
- "Language Implementation Patterns" — Terence Parr
- "Crafting Interpreters" — Robert Nystrom (abordagem didática similar)
- Python `ast` module — referência de design para AST nodes

---
*"Simplicidade é pré-requisito para confiabilidade. Confiabilidade é
pré-requisito para tudo o mais."*
— Maya Chen
