# Justificativa das métricas — Dashboard 2

Dataset: Titanic (782 passageiros após o tratamento da EDA). Os cálculos foram testados antes em [notebooks/metricas-dashboard2.ipynb](../notebooks/metricas-dashboard2.ipynb).

**Widgets que controlam o dashboard:** os filtros de intervalo da sidebar (os mesmos do Dashboard 1), o seletor "Agrupar por" (sexo, classe da passagem ou porto de embarque) e o clique em uma barra do gráfico, que recalcula as métricas só para o grupo escolhido.

## Métrica 1: Passageiros
- **Variável:** contagem de linhas do dataset filtrado
- **O que mede:** quantos passageiros estão sendo analisados no recorte atual (filtros + grupo clicado).
- **Por que foi escolhida:** dá a base das outras métricas; uma taxa calculada sobre 59 pessoas (Queenstown) pesa diferente de uma calculada sobre 568 (Southampton).
- **Público-alvo:** visitantes de museu / estudantes interessados na história do Titanic.
- **Qual decisão pode ser apoiada por essa métrica?** Se o recorte é grande o suficiente para tirar conclusões ou se é melhor ampliar os filtros.
- **O que comunica ao público-alvo:** "estamos falando de X pessoas", o tamanho do grupo que está na tela.

## Métrica 2: Taxa de sobrevivência
- **Variável:** `sobreviveu` (Sobreviveu / Não Sobreviveu)
- **O que mede:** a proporção de passageiros do recorte que sobreviveram. Ao clicar num grupo, mostra também a variação em pontos percentuais em relação à taxa geral do recorte (41,0% no dataset completo).
- **Por que foi escolhida:** é a variável de interesse da EDA; a proporção resume o desfecho em um único número, sem exigir leitura de gráfico.
- **Público-alvo:** visitantes de museu / estudantes interessados na história do Titanic.
- **Qual decisão pode ser apoiada por essa métrica?** Quais grupos merecem destaque na narrativa (ex.: priorizar a regra "mulheres e crianças primeiro" ao explicar o resgate).
- **O que comunica ao público-alvo:** quem teve mais chance de sobreviver; por exemplo, 73,9% das mulheres sobreviveram, contra 21,6% dos homens.

## Métrica 3: Idade média
- **Variável:** `age` (anos)
- **O que mede:** a média de idade dos passageiros do recorte.
- **Por que foi escolhida:** `age` tem distribuição próxima de simétrica (assimetria de 0,37), então a média representa bem o grupo; ajuda a perceber se um grupo era mais jovem ou mais velho.
- **Público-alvo:** visitantes de museu / estudantes interessados na história do Titanic.
- **Qual decisão pode ser apoiada por essa métrica?** Se a idade ajuda a explicar a diferença de sobrevivência entre os grupos.
- **O que comunica ao público-alvo:** o perfil etário de quem estava a bordo (em média, 29,8 anos).

## Métrica 4: Tarifa mediana
- **Variável:** `fare` (libras esterlinas)
- **O que mede:** o valor do meio das tarifas pagas no recorte.
- **Por que foi escolhida:** `fare` é muito assimétrica (assimetria de 4,58; média de £ 34,60 contra mediana de £ 15,88), então a mediana descreve melhor o passageiro típico do que a média, que é puxada pelas passagens mais caras.
- **Público-alvo:** visitantes de museu / estudantes interessados na história do Titanic.
- **Qual decisão pode ser apoiada por essa métrica?** Se o poder aquisitivo (classe social) está ligado à sobrevivência do grupo selecionado.
- **O que comunica ao público-alvo:** quanto um passageiro típico daquele grupo pagou, uma forma simples de mostrar a diferença social entre as classes.
