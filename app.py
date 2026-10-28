import altair as alt
import pandas as pd
import streamlit as st

from src.data_loader import load_data

st.set_page_config(
    page_title="Dashboards do Titanic Dataset",
    layout="wide",
)

st.title("Dashboards do Titanic Dataset")

df = load_data()

# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = ["age", "fare", "sibsp", "parch"]

# Sidebar: filtros (variáveis + intervalo)
with st.sidebar:
    st.header("Filtros")

    variaveis = st.multiselect(
        "Variáveis Quantitativas",
        options=VARS_QUANT,
        default=VARS_QUANT,
        help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
    )

    separar_por_classe = st.toggle(
        "Distinguir por Classe",
        value=False,
        help="Colore a distribuição pela classe (sobreviveu: Sobreviveu ou Não Sobreviveu).",
    )

    # Um slider de intervalo para cada variável selecionada
    intervalos = {}
    for var in variaveis:
        if pd.api.types.is_integer_dtype(df[var]):
            minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
        else:
            minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1
        intervalos[var] = st.slider(
            f"Intervalo de {var}",
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            key=f"intervalo_{var}",
        )

# Mantém só os passageiros dentro de todos os intervalos escolhidos
df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

st.caption(f"{len(df_filtrado)} de {len(df)} passageiros dentro dos intervalos escolhidos.")

# Cores do tema "oceano": azul profundo para Sobreviveu, azul acinzentado claro para Não Sobreviveu
COR_NAO_SOBREVIVEU = "#a9c4d6"
COR_SOBREVIVEU = "#1f6f8b"
COR_HISTOGRAMA = COR_SOBREVIVEU
CORES_CLASSE = alt.Scale(
    domain=["Não Sobreviveu", "Sobreviveu"], range=[COR_NAO_SOBREVIVEU, COR_SOBREVIVEU]
)

# Legenda das classes em texto, para caber no espaço livre da grade de histogramas
LEGENDA_CLASSE = (
    f"**Classe**  \n"
    f":color[■]{{foreground=\"{COR_NAO_SOBREVIVEU}\"}} Não Sobreviveu  \n"
    f":color[■]{{foreground=\"{COR_SOBREVIVEU}\"}} Sobreviveu"
)

aba_dashboard1, aba_dashboard2 = st.tabs(
    ["Dashboard 1: Correlação e Distribuição", "Dashboard 2: KPIs de Sobrevivência"]
)

# Dashboard 1: correlação (heatmap) à esquerda, distribuição (histograma) à direita
with aba_dashboard1:
    col_correlacao, col_distribuicao = st.columns([1, 1.5])

    with col_correlacao:
        st.subheader("Correlação (Spearman)")

        if len(variaveis) < 2:
            st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
        elif len(df_filtrado) < 30:
            st.warning("Poucos passageiros nos intervalos escolhidos para calcular a correlação.")
        else:
            # Matriz de correlação de Spearman das variáveis selecionadas, em formato longo (uma linha por célula)
            corr = (
                df_filtrado[variaveis]
                .corr(method="spearman")
                .rename_axis(index="var_y", columns="var_x")
                .stack()
                .rename("correlacao")
                .reset_index()
            )
            # Só o triângulo inferior, sem a diagonal (sempre 1): a matriz é simétrica, o resto é repetição
            ordem = {var: i for i, var in enumerate(variaveis)}
            corr = corr[corr["var_y"].map(ordem) > corr["var_x"].map(ordem)]

            base = alt.Chart(corr).encode(
                x=alt.X(
                    "var_x:N",
                    title=None,
                    sort=variaveis[:-1],  # a última variável só aparece nas linhas
                    axis=alt.Axis(labelAngle=0, labelFontSize=14),
                ),
                y=alt.Y("var_y:N", title=None, sort=variaveis[1:], axis=alt.Axis(labelFontSize=14)),  # a primeira só nas colunas
            )
            heatmap = base.mark_rect().encode(
                color=alt.Color(
                    "correlacao:Q",
                    title="Spearman",
                    scale=alt.Scale(scheme="redblue", domain=[-1, 1], reverse=True),
                    legend=alt.Legend(titleFontSize=14, labelFontSize=13),
                ),
                tooltip=["var_x", "var_y", alt.Tooltip("correlacao:Q", format=".2f")],
            )
            valores = base.mark_text(fontSize=16).encode(
                text=alt.Text("correlacao:Q", format=".2f"),
                color=alt.condition(
                    "abs(datum.correlacao) > 0.5", alt.value("white"), alt.value("black")
                ),
            )

            st.altair_chart(
                (heatmap + valores).properties(height=380),
                width="stretch",
                alt="Mapa de calor (triângulo inferior, sem a diagonal) da correlação de Spearman entre as variáveis quantitativas selecionadas",
            )

    with col_distribuicao:
        st.subheader("Distribuição")

        if not variaveis:
            st.warning("Selecione pelo menos 1 variável para ver a distribuição.")
        elif df_filtrado.empty:
            st.warning("Nenhum passageiro dentro dos intervalos escolhidos.")
        else:
            # Com número par de variáveis não sobra espaço na grade: a legenda vai acima dela
            if separar_por_classe and len(variaveis) % 2 == 0:
                st.markdown(LEGENDA_CLASSE)

            # Um histograma por variável selecionada, em grade de 2 colunas (cada um com a sua escala)
            for inicio in range(0, len(variaveis), 2):
                colunas = st.columns(2)
                for coluna, var in zip(colunas, variaveis[inicio : inicio + 2]):
                    histograma = (
                        alt.Chart(df_filtrado[[var, "sobreviveu"]])
                        .mark_bar()
                        .encode(
                            x=alt.X(f"{var}:Q", bin=alt.Bin(maxbins=20), title=var),
                            y=alt.Y("count()", title="Passageiros"),
                            tooltip=[alt.Tooltip("count()", title="Passageiros")],
                        )
                        .properties(height=200)
                    )
                    if separar_por_classe:
                        histograma = histograma.encode(
                            color=alt.Color(
                                "sobreviveu:N",
                                title="Classe",
                                scale=CORES_CLASSE,
                                legend=None,
                            ),
                            tooltip=["sobreviveu", alt.Tooltip("count()", title="Passageiros")],
                        )
                    else:
                        histograma = histograma.mark_bar(color=COR_HISTOGRAMA)

                    with coluna:
                        st.altair_chart(histograma, width="stretch", alt=f"Histograma da variável {var}")

                # Número ímpar de variáveis: a legenda ocupa o espaço que sobrou na última linha
                if separar_por_classe and len(colunas) == 2 and len(variaveis[inicio : inicio + 2]) == 1:
                    colunas[1].markdown(LEGENDA_CLASSE)

# Dashboard 2: KPIs no topo e taxa de sobrevivência por grupo (clicar numa barra atualiza os KPIs)
GRUPOS = {"sex": "Sexo", "class": "Classe da passagem", "embark_town": "Porto de embarque"}

with aba_dashboard2:
    agrupar_por = st.segmented_control(
        "Agrupar por",
        options=list(GRUPOS),
        format_func=GRUPOS.get,
        default="sex",
        required=True,
        help="Variável categórica usada para agrupar os passageiros no gráfico de barras.",
    )

    if df_filtrado.empty:
        st.warning("Nenhum passageiro dentro dos intervalos escolhidos.")
    else:
        area_kpis = st.container()  # os KPIs aparecem acima, mas dependem do clique no gráfico abaixo

        # Taxa de sobrevivência e número de passageiros de cada grupo
        por_grupo = (
            df_filtrado.assign(sobreviveu_num=df_filtrado["sobreviveu"].eq("Sobreviveu"))
            .groupby(agrupar_por, observed=True)
            .agg(passageiros=("sobreviveu_num", "size"), taxa=("sobreviveu_num", "mean"))
            .reset_index()
        )

        clique = alt.selection_point(name="clique", fields=[agrupar_por])
        barras = (
            alt.Chart(por_grupo)
            .mark_bar(color=COR_SOBREVIVEU)
            .encode(
                x=alt.X(f"{agrupar_por}:N", title=GRUPOS[agrupar_por], axis=alt.Axis(labelAngle=0)),
                y=alt.Y("taxa:Q", title="Taxa de sobrevivência", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1])),
                opacity=alt.condition(clique, alt.value(1), alt.value(0.3)),
                tooltip=[
                    alt.Tooltip(f"{agrupar_por}:N", title=GRUPOS[agrupar_por]),
                    alt.Tooltip("passageiros:Q", title="Passageiros"),
                    alt.Tooltip("taxa:Q", title="Taxa de sobrevivência", format=".1%"),
                ],
            )
            .add_params(clique)
            .properties(height=360)
        )

        st.subheader(f"Taxa de sobrevivência por {GRUPOS[agrupar_por].lower()}")
        st.caption("Clique em uma barra para ver os KPIs só daquele grupo (shift + clique seleciona mais de um).")
        evento = st.altair_chart(barras, key=f"barras_{agrupar_por}", on_select="rerun", width="stretch")

        itens = evento.selection.get("clique", [])
        grupos_selecionados = [item[agrupar_por] for item in itens]
        selecionado = (
            df_filtrado[df_filtrado[agrupar_por].isin(grupos_selecionados)]
            if grupos_selecionados
            else df_filtrado
        )

        taxa_geral = df_filtrado["sobreviveu"].eq("Sobreviveu").mean()
        taxa_selecionado = selecionado["sobreviveu"].eq("Sobreviveu").mean()
        idade_media = selecionado["age"].mean()

        with area_kpis:
            st.markdown(
                f"**Grupo:** {', '.join(map(str, grupos_selecionados)) if grupos_selecionados else 'todos os passageiros'}"
            )
            kpi1, kpi2, kpi3, kpi4 = st.columns(4, border=True)
            kpi1.metric("Passageiros", f"{len(selecionado)}")
            kpi2.metric(
                "Taxa de sobrevivência",
                f"{taxa_selecionado:.1%}",
                delta=f"{(taxa_selecionado - taxa_geral) * 100:+.1f} p.p. vs. geral" if grupos_selecionados else None,
            )
            kpi3.metric("Idade média", "—" if pd.isna(idade_media) else f"{idade_media:.1f} anos")
            kpi4.metric("Tarifa mediana", f"£ {selecionado['fare'].median():.2f}")
