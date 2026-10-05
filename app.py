import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard Climático no Brasil",
    page_icon="☀️",
    layout="wide"
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #f7f9fa;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: #34424c;
        }

        h1 {
            margin-bottom: 0.3rem;
        }

        div[data-testid="stMetric"] {
            background-color: white;
            border: 1px solid #dbe3e8;
            border-top: 4px solid #3b82b8;
            border-radius: 10px;
            padding: 16px;
        }

        div[data-testid="stMetric"]:nth-child(even) {
            border-top-color: #f2c94c;
        }

        section[data-testid="stSidebar"] {
            background-color: #eef2f4;
        }

        hr {
            border: none;
            border-top: 1px solid #dbe3e8;
            margin: 1.8rem 0;
        }

        .intro {
            padding: 18px 20px;
            margin: 10px 0 24px;
            background-color: #eaf5fb;
            border-left: 5px solid #3b82b8;
            border-radius: 8px;
            color: #34424c;
        }

        .info {
            padding: 16px 18px;
            background-color: #fff8df;
            border-left: 5px solid #f2c94c;
            border-radius: 8px;
            color: #34424c;
        }
    </style>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv("simulacao_clima_brasil.csv")
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

st.title("☀️ Dashboard Climático no Brasil")

st.markdown(
    """
    <div class="intro">
        Explore as condições climáticas registradas no Brasil entre
        <strong>2015 e 2024</strong>. Use os filtros para comparar períodos
        e regiões e observar a ocorrência de eventos extremos.
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("Filtros")
st.sidebar.caption(
    "Selecione as opções abaixo para atualizar os resultados do dashboard."
)

anos_disponiveis = sorted(df["ano"].dropna().unique())
regioes_disponiveis = sorted(df["regiao"].dropna().unique())
alertas_disponiveis = df["nivel_alerta"].dropna().unique().tolist()

ano = st.sidebar.multiselect(
    "Ano",
    anos_disponiveis,
    default=anos_disponiveis
)

regiao = st.sidebar.multiselect(
    "Região",
    regioes_disponiveis,
    default=regioes_disponiveis
)

alerta = st.sidebar.multiselect(
    "Nível de alerta",
    alertas_disponiveis,
    default=alertas_disponiveis
)

df_filtrado = df[
    df["ano"].isin(ano)
    & df["regiao"].isin(regiao)
    & df["nivel_alerta"].isin(alerta)
]

if df_filtrado.empty:
    st.warning(
        "Nenhum registro foi encontrado com os filtros selecionados. "
        "Altere uma ou mais opções para continuar."
    )
    st.stop()

temperatura = df_filtrado["temperatura_media"].mean()
chuva = df_filtrado["chuva_mm"].mean()
eventos = df_filtrado["eventos_extremos"].sum()
percentual = (
    df_filtrado["teve_evento_extremo"].eq("Sim").mean() * 100
)

st.subheader("Visão geral")
st.caption(
    "Principais indicadores calculados de acordo com os filtros selecionados."
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Temperatura média",
    f"{temperatura:.2f} °C"
)

col2.metric(
    "Chuva média",
    f"{chuva:.2f} mm"
)

col3.metric(
    "Eventos extremos",
    int(eventos)
)

col4.metric(
    "Registros com eventos",
    f"{percentual:.2f}%"
)

st.divider()

st.subheader("Comparação entre regiões")
st.caption(
    "Resumo das médias de temperatura e chuva e do total de eventos "
    "extremos em cada região selecionada."
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

st.divider()

st.subheader("Eventos extremos ao longo dos anos")
st.caption(
    "O gráfico mostra como a quantidade de eventos extremos varia "
    "durante o período selecionado."
)

eventos_ano = (
    df_filtrado.groupby("ano")["eventos_extremos"]
    .sum()
)

fig, ax = plt.subplots(figsize=(9, 4))

ax.plot(
    eventos_ano.index,
    eventos_ano.values,
    marker="o",
    linewidth=2
)

ax.set_xlabel("Ano")
ax.set_ylabel("Quantidade de eventos")
ax.grid(alpha=0.25)

st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.divider()

st.subheader("Eventos extremos por região")
st.caption(
    "Compare o total de eventos extremos registrado nas regiões "
    "selecionadas."
)

eventos_regiao = (
    df_filtrado.groupby("regiao")["eventos_extremos"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(9, 4))

sns.barplot(
    x=eventos_regiao.index,
    y=eventos_regiao.values,
    ax=ax
)

ax.set_xlabel("Região")
ax.set_ylabel("Quantidade de eventos")
ax.tick_params(axis="x", rotation=20)

st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.divider()

st.subheader("Relação entre as variáveis")
st.caption(
    "A matriz de correlação ajuda a observar como as variáveis "
    "climáticas se relacionam nos dados selecionados. Valores próximos "
    "de 1 ou -1 indicam relações mais fortes."
)

colunas_correlacao = [
    "temperatura_media",
    "chuva_mm",
    "umidade",
    "velocidade_vento",
    "eventos_extremos"
]

correlacao = df_filtrado[colunas_correlacao].corr()

fig, ax = plt.subplots(figsize=(8, 5))

sns.heatmap(
    correlacao,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    vmin=-1,
    vmax=1,
    ax=ax
)

ax.set_xticklabels(
    ["Temperatura", "Chuva", "Umidade", "Vento", "Eventos"],
    rotation=25,
    ha="right"
)

ax.set_yticklabels(
    ["Temperatura", "Chuva", "Umidade", "Vento", "Eventos"],
    rotation=0
)

st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.divider()

st.subheader("Resumo dos resultados")

if not eventos_regiao.empty:
    regiao_destaque = eventos_regiao.idxmax()
    maior_total = int(eventos_regiao.max())

    st.markdown(
        f"""
        <div class="info">
            Nos dados selecionados, a região com mais eventos extremos foi
            <strong>{regiao_destaque}</strong>, com
            <strong>{maior_total}</strong> ocorrências.
            A temperatura média foi de <strong>{temperatura:.2f} °C</strong>
            e a chuva média de <strong>{chuva:.2f} mm</strong>.
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")
st.write(
    "Os filtros permitem observar diferentes recortes dos dados e comparar "
    "como as condições climáticas e os eventos extremos variam entre "
    "períodos e regiões."
)
