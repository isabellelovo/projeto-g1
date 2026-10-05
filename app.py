import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Análise Climática no Brasil",
    page_icon="🌤️",
    layout="wide"
)

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        section[data-testid="stSidebar"] {
            background-color: #f4f6f8;
        }

        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 14px;
        }

        h1, h2, h3 {
            color: #334155;
        }
    </style>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv("dados/simulacao_clima_brasil.csv")
df = df.drop_duplicates()
df["data"] = pd.to_datetime(df["data"])

colunas_numericas = [
    "ano",
    "mes",
    "temperatura_media",
    "temperatura_maxima",
    "temperatura_minima",
    "chuva_mm",
    "umidade",
    "velocidade_vento",
    "eventos_extremos"
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

colunas_texto = [
    "regiao",
    "uf",
    "cidade",
    "nivel_alerta"
]

for coluna in colunas_texto:
    df[coluna] = df[coluna].astype(str).str.strip()

df["nivel_alerta"] = pd.Categorical(
    df["nivel_alerta"],
    categories=["Baixo", "Médio", "Alto", "Crítico"],
    ordered=True
)

df = df.dropna(subset=["data", "regiao", "uf", "cidade"])

meses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

df["trimestre"] = df["data"].dt.quarter
df["nome_mes"] = df["mes"].map(meses)
df["amplitude_termica"] = (
    df["temperatura_maxima"] - df["temperatura_minima"]
)
df["teve_evento_extremo"] = np.where(
    df["eventos_extremos"] > 0,
    "Sim",
    "Não"
)

colunas_correlacao = [
    "temperatura_media",
    "chuva_mm",
    "umidade",
    "velocidade_vento",
    "eventos_extremos"
]

st.title("🌤️ Análise Climática e Eventos Extremos no Brasil")

st.markdown(
    """
    **Dashboard interativo para análise das condições climáticas registradas no Brasil entre 2015 e 2024.**

    A aplicação permite comparar períodos e regiões, acompanhar a ocorrência de eventos
    extremos e observar possíveis relações entre temperatura, chuva, umidade e velocidade do vento.
    """
)

st.caption(
    "Disciplina: Linguagens de Programação | "
    "Discente: Isabelle Pinheiro Lovo | "
    "RA: 1016112 | "
    "Docente: Alexandre Neves Louzada"
)

st.divider()

st.sidebar.title("🔎 Filtros")

st.sidebar.markdown(
    """
    Utilize os filtros abaixo para explorar os dados.
    Os indicadores, tabelas e gráficos serão atualizados
    de acordo com as opções selecionadas.
    """
)

anos_disponiveis = sorted(df["ano"].unique())

anos_selecionados = st.sidebar.multiselect(
    "Ano",
    options=anos_disponiveis,
    default=anos_disponiveis
)

regioes_disponiveis = sorted(df["regiao"].unique())

regioes_selecionadas = st.sidebar.multiselect(
    "Região",
    options=regioes_disponiveis,
    default=regioes_disponiveis
)

alertas_disponiveis = df["nivel_alerta"].dropna().unique().tolist()

alertas_selecionados = st.sidebar.multiselect(
    "Nível de alerta",
    options=alertas_disponiveis,
    default=alertas_disponiveis
)

df_filtrado = df[
    df["ano"].isin(anos_selecionados)
    & df["regiao"].isin(regioes_selecionadas)
    & df["nivel_alerta"].isin(alertas_selecionados)
].copy()

if df_filtrado.empty:
    st.warning(
        "Nenhum registro foi encontrado para a combinação de filtros selecionada."
    )
    st.stop()

temperatura = df_filtrado["temperatura_media"].mean()
chuva = df_filtrado["chuva_mm"].mean()
eventos = df_filtrado["eventos_extremos"].sum()
percentual = (
    df_filtrado["teve_evento_extremo"].eq("Sim").mean() * 100
)

st.subheader("📊 Indicadores principais")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Temperatura média",
        f"{temperatura:.2f} °C"
    )

with col2:
    st.metric(
        "Chuva média",
        f"{chuva:.2f} mm"
    )

with col3:
    st.metric(
        "Eventos extremos",
        f"{int(eventos)}"
    )

with col4:
    st.metric(
        "Registros com eventos",
        f"{percentual:.2f}%"
    )

st.divider()

aba_visao_geral, aba_temporal, aba_regional, aba_correlacao = st.tabs(
    [
        "📊 Visão Geral",
        "📈 Análise Temporal",
        "📍 Análise Regional",
        "🔎 Correlação"
    ]
)

with aba_visao_geral:
    st.subheader("📊 Visão geral")

    st.write(
        """
        Esta seção resume as condições climáticas das regiões selecionadas,
        apresentando as médias de temperatura e chuva e o total de eventos extremos.
        """
    )

    tabela = (
        df_filtrado.groupby("regiao")
        .agg(
            temperatura_media=("temperatura_media", "mean"),
            chuva_media=("chuva_mm", "mean"),
            eventos_extremos=("eventos_extremos", "sum")
        )
        .reset_index()
    )

    tabela = tabela.rename(
        columns={
            "regiao": "Região",
            "temperatura_media": "Temperatura média (°C)",
            "chuva_media": "Chuva média (mm)",
            "eventos_extremos": "Eventos extremos"
        }
    )

    st.dataframe(
        tabela.round(2),
        use_container_width=True,
        hide_index=True
    )

    eventos_regiao = (
        df_filtrado.groupby("regiao", as_index=False)["eventos_extremos"]
        .sum()
        .sort_values("eventos_extremos", ascending=False)
    )

    fig_visao = px.bar(
        eventos_regiao,
        x="regiao",
        y="eventos_extremos",
        title="Eventos Extremos por Região",
        labels={
            "regiao": "Região",
            "eventos_extremos": "Quantidade de eventos"
        },
        color_discrete_sequence=["#4f86a6"]
    )

    fig_visao.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_visao,
        use_container_width=True
    )

    regiao_destaque = eventos_regiao.iloc[0]

    st.info(
        f"""
        **Interpretação:** considerando os filtros selecionados,
        **{regiao_destaque["regiao"]}** apresenta a maior quantidade de eventos extremos,
        com **{int(regiao_destaque["eventos_extremos"])} eventos**.

        A temperatura média do período selecionado é de **{temperatura:.2f} °C**
        e a chuva média é de **{chuva:.2f} mm**.
        """
    )

with aba_temporal:
    st.subheader("📈 Análise temporal")

    st.write(
        """
        Esta seção mostra como a quantidade de eventos extremos varia ao longo dos anos,
        permitindo comparar os diferentes períodos selecionados.
        """
    )

    eventos_ano = (
        df_filtrado.groupby("ano", as_index=False)["eventos_extremos"]
        .sum()
        .sort_values("ano")
    )

    fig_ano = px.line(
        eventos_ano,
        x="ano",
        y="eventos_extremos",
        markers=True,
        title="Eventos Extremos por Ano",
        labels={
            "ano": "Ano",
            "eventos_extremos": "Quantidade de eventos"
        },
        color_discrete_sequence=["#4f86a6"]
    )

    fig_ano.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_ano,
        use_container_width=True
    )

    if len(eventos_ano) > 1:
        primeiro_ano = eventos_ano.iloc[0]
        ultimo_ano = eventos_ano.iloc[-1]

        diferenca = (
            ultimo_ano["eventos_extremos"]
            - primeiro_ano["eventos_extremos"]
        )

        if diferenca > 0:
            tendencia = "aumento"
        elif diferenca < 0:
            tendencia = "redução"
        else:
            tendencia = "estabilidade"

        st.info(
            f"""
            **Interpretação:** no primeiro ano selecionado foram registrados
            **{int(primeiro_ano["eventos_extremos"])} eventos extremos** e,
            no último, **{int(ultimo_ano["eventos_extremos"])}**.

            A comparação entre esses dois pontos indica **{tendencia}**
            na quantidade de eventos extremos.
            """
        )
    else:
        st.info(
            "Apenas um ano está selecionado. Para comparar a evolução temporal, "
            "selecione dois ou mais anos na barra lateral."
        )

with aba_regional:
    st.subheader("📍 Análise regional")

    st.write(
        """
        Esta seção compara a ocorrência de eventos extremos entre as regiões,
        facilitando a identificação das áreas que mais se destacam nos dados selecionados.
        """
    )

    eventos_regiao = (
        df_filtrado.groupby("regiao", as_index=False)["eventos_extremos"]
        .sum()
        .sort_values("eventos_extremos", ascending=False)
    )

    fig_regiao = px.bar(
        eventos_regiao,
        x="regiao",
        y="eventos_extremos",
        title="Total de Eventos Extremos por Região",
        labels={
            "regiao": "Região",
            "eventos_extremos": "Quantidade de eventos"
        },
        color_discrete_sequence=["#e0b84d"]
    )

    fig_regiao.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_regiao,
        use_container_width=True
    )

    regiao_lider = eventos_regiao.iloc[0]

    st.info(
        f"""
        **Interpretação:** considerando os filtros selecionados,
        a região com maior quantidade de eventos extremos é
        **{regiao_lider["regiao"]}**, com
        **{int(regiao_lider["eventos_extremos"])} eventos**.
        """
    )

with aba_correlacao:
    st.subheader("🔎 Correlação entre variáveis")

    st.write(
        """
        A matriz de correlação permite observar possíveis relações entre temperatura,
        chuva, umidade, velocidade do vento e eventos extremos.
        Valores próximos de 1 ou -1 indicam relações lineares mais fortes.
        """
    )

    correlacao_filtrada = df_filtrado[colunas_correlacao].corr()

    nomes_correlacao = {
        "temperatura_media": "Temperatura",
        "chuva_mm": "Chuva",
        "umidade": "Umidade",
        "velocidade_vento": "Vento",
        "eventos_extremos": "Eventos"
    }

    correlacao_exibicao = correlacao_filtrada.rename(
        index=nomes_correlacao,
        columns=nomes_correlacao
    )

    fig_correlacao = px.imshow(
        correlacao_exibicao,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Correlação entre Variáveis",
        labels={"color": "Correlação"}
    )

    st.plotly_chart(
        fig_correlacao,
        use_container_width=True
    )

    st.info(
        """
        **Como interpretar:** correlações positivas indicam que duas variáveis tendem
        a variar na mesma direção, enquanto correlações negativas indicam variação
        em direções opostas. A correlação mostra uma associação entre as variáveis,
        mas não significa que uma seja a causa da outra.
        """
    )

st.divider()

st.subheader("📝 Conclusão Executiva")

eventos_regiao_conclusao = (
    df_filtrado.groupby("regiao")["eventos_extremos"]
    .sum()
    .sort_values(ascending=False)
)

regiao_conclusao = eventos_regiao_conclusao.idxmax()

st.markdown(
    f"""
    Considerando os filtros selecionados, a análise apresenta uma
    **temperatura média de {temperatura:.2f} °C**, uma
    **chuva média de {chuva:.2f} mm** e um total de
    **{int(eventos)} eventos extremos**.

    A região com maior quantidade de eventos extremos é
    **{regiao_conclusao}**. Os resultados permitem comparar as condições
    climáticas entre diferentes períodos e regiões, enquanto a análise de
    correlação auxilia na observação de possíveis relações entre as variáveis.
    """
)

st.divider()

st.caption(
    "Projeto acadêmico desenvolvido por Isabelle Pinheiro Lovo | "
    "Disciplina: Linguagens de Programação | "
    "Docente: Alexandre Neves Louzada"
)
