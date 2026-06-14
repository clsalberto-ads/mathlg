# Tutorial 07: Exportação de Resultados (CSV / JSON)

Este tutorial ensina como exportar o histórico de resultados do MathLg para formatos CSV e JSON. A exportação permite analisar expressões, resultados e timestamps em planilhas ou scripts externos.

## 1. Sobre a Exportação

O MathLg pode registrar cada operação realizada em um arquivo de histórico. Para ativar, use a flag `--export` ao iniciar.

```mlg
mostre "=== EXPORTACAO ==="
mostre "Para exportar resultados:"
mostre "1. Execute: mathlg --export csv"
mostre "2. Faca operacoes no REPL"
mostre "3. Digite: exportar csv"
mostre ""
mostre "Ou execute um arquivo com export:"
mostre "  mathlg --export csv arquivo.mlg"
mostre ""
mostre "O arquivo 'historico.csv' sera gerado com:"
mostre "  expressao, resultado, timestamp"
mostre ""
```

> **O que acontece:** Esta seção exibe instruções de uso. A exportação é ativada via linha de comando com `--export csv` ou `--export json`, e o comando `exportar csv` (ou `exportar json`) gera o arquivo com os dados acumulados.

## 2. Exemplo de Dados Exportados

Operações realizadas durante a sessão são registradas no histórico para exportação.

```mlg
x = 10
y = 20
mostre x + y
```

> **O que acontece:** Cada expressão avaliada (como `x + y`) é armazenada no histórico interno. Quando o comando `exportar csv` é executado (com a flag `--export` ativada), um arquivo `historico.csv` é gerado contendo todas as expressões, seus resultados e o momento em que foram executadas.

## 3. Comando de Exportação

O comando `exportar csv` finaliza o processo e gera o arquivo de saída.

```mlg
exportar csv
```

> **O que acontece:** Este comando só funciona quando o MathLg foi iniciado com a flag `--export csv`. Ele escreve o arquivo `historico.csv` no diretório atual com o formato: `expressão, resultado, timestamp`. O mesmo processo se aplica para `exportar json`, que gera `historico.json`.
