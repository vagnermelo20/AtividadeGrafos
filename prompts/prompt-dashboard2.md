# Prompt: Dashboard 1 completo + Dashboard 2 (KPIs)

## Contexto

Disciplina de Análise e Visualização de Dados (Cesar School). Dataset Titanic em `data/clean/dataset.csv`. O `app.py` já tem a sidebar do Dashboard 1 (seletor de variáveis + sliders de intervalo). Aula 22: completar o Dashboard 1 e estruturar o Dashboard 2 (KPIs).

## Entrada

- Rascunhos em `entregas/rascunho-dashboard1.png` e `entregas/rascunho-dashboard2.png`.
- Métricas definidas em `entregas/justificativa-metricas.md`: passageiros, taxa de sobrevivência, idade média e tarifa mediana.
- Widgets do Dashboard 2: seletor "Agrupar por" (`sex`, `class`, `embark_town`) e clique numa barra.

## Restrições

- Gráficos com Altair (`st.altair_chart`), seguindo o `app.py` e o `ALTAIR-CROSSFILTER.md` da professora.
- Dados via `src/data_loader.py` com `@st.cache_data`.
- Dois dashboards em `st.tabs`; KPIs com `st.metric` (3 a 5).
- Tratar 0, 1 e 2+ variáveis selecionadas sem erro.

## Formato de saída

O `app.py` completo, pronto para `streamlit run app.py`.
