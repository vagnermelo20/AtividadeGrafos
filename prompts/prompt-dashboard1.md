# Prompt: rascunho do Dashboard 1 → esqueleto do app

## Contexto

Disciplina de Análise e Visualização de Dados (Cesar School). Dataset Titanic, já tratado na EDA e salvo em `data/clean/dataset.csv`. Dashboard 1: correlação + distribuição das variáveis quantitativas.

## Entrada

Rascunho em `entregas/rascunho-dashboard1.png`: sidebar com filtros (variáveis + intervalo); área principal com Correlação (heatmap) à esquerda e Distribuição (histograma) à direita.

Variáveis quantitativas: `age`, `fare`, `sibsp`, `parch`. Classe: `sobreviveu`.

## Restrições

- Gerar só o esqueleto estrutural, sem lógica de dados nos gráficos.
- Usar placeholders (`# TODO`) nos espaços dos gráficos.
- Widgets mínimos: 1 seletor de variáveis e 1 slider de intervalo.
- Carregar os dados via `src/data_loader.py`.

## Formato de saída

Um único `app.py`, pronto para `streamlit run app.py`.
