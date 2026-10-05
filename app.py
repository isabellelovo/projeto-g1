import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Análise Climática",
    layout="wide"
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

df["data"] = pd.to_datetime(df["data"])
df["trimestre"] = df["data"].dt.quarter
df["nome_mes"] = df["data"].dt.month_name()

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

df["nome_mes"] = df["mes"].map(meses)

df["amplitude_termica"] = (
    df["temperatura_maxima"] - df["temperatura_minima"]
)

df["teve_evento_extremo"] = np.where(
    df["eventos_extremos"] > 0,
    "Sim",
    "Não"
)

eventos_regiao = df.groupby("regiao")["eventos_extremos"].sum()
eventos_ano = df.groupby("ano")["eventos_extremos"].sum()

colunas = [
    "temperatura_media",
    "chuva_mm",
    "umidade",
    "velocidade_vento",
    "eventos_extremos"
]

correlacao = df[colunas].corr()

st.title("Análise Climática e Eventos Extremos no Brasil")

st.write(
    "Análise das condições climáticas registradas entre 2015 e 2024, "
    "com foco na ocorrência de eventos extremos e nas diferenças "
    "entre regiões e períodos."
)

st.sidebar.header("Filtros")

ano = st.sidebar.multiselect(
    "Ano",
    sorted(df["ano"].unique()),
    default=sorted(df["ano"].unique())
)

regiao = st.sidebar.multiselect(
    "Região",
    sorted(df["regiao"].unique()),
    default=sorted(df["regiao"].unique())
)

alerta = st.sidebar.multiselect(
    "Nível de alerta",
    df["nivel_alerta"].dropna().unique().tolist(),
    default=df["nivel_alerta"].dropna().unique().tolist()
)

df_filtrado = df[
    df["ano"].isin(ano)
    & df["regiao"].isin(regiao)
    & df["nivel_alerta"].isin(alerta)
]

if df_filtrado.empty:
    st.warning("Não há dados para os filtros selecionados.")
    st.stop()

temperatura = df_filtrado["temperatura_media"].mean()
chuva = df_filtrado["chuva_mm"].mean()
eventos = df_filtrado["eventos_extremos"].sum()
percentual = (
    df_filtrado["teve_evento_extremo"].eq("Sim").mean() * 100
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Temperatura média", f"{temperatura:.2f} °C")
col2.metric("Chuva média", f"{chuva:.2f} mm")
col3.metric("Eventos extremos", int(eventos))
col4.metric("Registros com eventos", f"{percentual:.2f}%")

st.subheader("Dados por Região")

tabela = df_filtrado.groupby("regiao").agg(
    temperatura_media=("temperatura_media", "mean"),
    chuva_media=("chuva_mm", "mean"),
    eventos_extremos=("eventos_extremos", "sum")
).reset_index()

st.dataframe(tabela.round(2), use_container_width=True)

st.subheader("Eventos Extremos por Ano")

eventos_ano_filtrado = (
    df_filtrado.groupby("ano")["eventos_extremos"].sum()
)

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(
    eventos_ano_filtrado.index,
    eventos_ano_filtrado.values,
    marker="o"
)

ax.set_xlabel("Ano")
ax.set_ylabel("Eventos extremos")
ax.set_title("Eventos Extremos por Ano")
ax.grid(True)

st.pyplot(fig)

plt.close(fig)

st.subheader("Eventos Extremos por Região")

eventos_regiao_filtrado = (
    df_filtrado.groupby("regiao")["eventos_extremos"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 4))

sns.barplot(
    x=eventos_regiao_filtrado.index,
    y=eventos_regiao_filtrado.values,
    ax=ax
)

ax.set_xlabel("Região")
ax.set_ylabel("Eventos extremos")
ax.set_title("Eventos Extremos por Região")
ax.tick_params(axis="x", rotation=30)

st.pyplot(fig)

plt.close(fig)

st.subheader("Correlação entre Variáveis")

correlacao_filtrada = df_filtrado[colunas].corr()

fig, ax = plt.subplots(figsize=(8, 5))

sns.heatmap(
    correlacao_filtrada,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    ax=ax
)

ax.set_title("Correlação entre Variáveis")

st.pyplot(fig)

plt.close(fig)

st.subheader("Interpretação")

eventos_regiao_filtrado = (
    df_filtrado.groupby("regiao")["eventos_extremos"]
    .sum()
    .sort_values(ascending=False)
)

if not eventos_regiao_filtrado.empty:
    regiao_destaque = eventos_regiao_filtrado.idxmax()

    st.write(
        f"A região com maior quantidade de eventos extremos no período "
        f"selecionado foi {regiao_destaque}."
    )

    st.write(
        f"A temperatura média foi de {temperatura:.2f} °C e a chuva média "
        f"foi de {chuva:.2f} mm."
    )

st.subheader("Conclusão Executiva")

st.write(
    "Os resultados permitem comparar as condições climáticas e a "
    "ocorrência de eventos extremos entre diferentes períodos e regiões. "
    "Os indicadores são atualizados conforme os filtros selecionados."
)

st.write(
    "Por se tratar de uma base simulada, os resultados representam "
    "os padrões encontrados nos dados analisados."
)
