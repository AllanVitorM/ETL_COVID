import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")
st.title("Dashboard COVID-19 Interativo")

# --- Lista de CSVs disponíveis ---
csv_files = [f for f in os.listdir("output") if f.endswith(".csv")]
pais_selecionados = st.multiselect("Escolha os países:", csv_files, default=[csv_files[0]])

if not pais_selecionados:
    st.warning("Selecione pelo menos um país!")
    st.stop()

# --- Indicadores disponíveis ---
indicadores_disponiveis = [
    "casos_diarios", "mortes_diarias", "recuperados_diarios",
    "casos_7d_ma", "mortes_7d_ma", "recuperados_7d_ma",
    "letalidade_pct", "recuperacao_pct", "casos_por_100k"
]
indicador = st.selectbox("Escolha o indicador/métrica:", indicadores_disponiveis)

# --- Carregar CSVs selecionados ---
dfs = []
for arquivo in pais_selecionados:
    df = pd.read_csv(os.path.join("output", arquivo), parse_dates=['date'])
    df['pais'] = arquivo.replace("covid_", "").replace(".csv","")
    dfs.append(df)

df_all = pd.concat(dfs)

# --- Filtro por período ---
min_date = df_all['date'].min()
max_date = df_all['date'].max()
start_date, end_date = st.slider(
    "Escolha o período:",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime())
)

df_filtered = df_all[(df_all['date'] >= start_date) & (df_all['date'] <= end_date)]

# --- Mostrar tabela filtrada ---
st.subheader("Tabela de dados filtrada")
st.dataframe(df_filtered)

# --- Gráfico interativo ---
st.subheader(f"{indicador} por país")
fig = px.line(
    df_filtered,
    x='date',
    y=indicador,
    color='pais',
    title=f"{indicador} de COVID-19",
    labels={'date':'Data', indicador: indicador, 'pais':'País'}
)
st.plotly_chart(fig, use_container_width=True)
