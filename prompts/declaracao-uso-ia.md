# Declaração de Uso de IA

**Nome:** Vagner Montenegro
**Data:** 22/10/2026 (Aula 21) e 27/10/2026 (Aula 22)

## Ferramenta

Claude Code (Claude Opus 5.5).

## Aula 21

### Prompt usado

O prompt completo está em [prompt-dashboard1.md](prompt-dashboard1.md).

### O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:** estrutura do `app.py` (sidebar com seletor de variáveis e sliders de intervalo, área principal em duas colunas) e células de exportação dos datasets no notebook.
- **Modificado:** variáveis e classe ajustadas para o Titanic (`age`, `fare`, `sibsp`, `parch` e `sobreviveu`).
- **Rejeitado:** gráficos (heatmap e histograma), deixados como `# TODO` porque entram na próxima aula.

## Aula 22

### Prompt usado

O prompt completo está em [prompt-dashboard2.md](prompt-dashboard2.md).

### O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:** heatmap de Spearman e histogramas em Altair no Dashboard 1, abas para os dois dashboards, 4 KPIs com `st.metric` e gráfico de barras da taxa de sobrevivência por grupo com clique (`on_select`) atualizando os KPIs.
- **Modificado:** cores trocadas para uma paleta "oceano" (azul) ligada ao tema do Titanic, aplicada também ao `.streamlit/config.toml`; tarifa mostrada pela mediana em vez da média, porque `fare` é muito assimétrica.
- **Rejeitado:** mais de 4 KPIs, para não passar do limite de 3 a 5 indicado na aula.
