import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# ================= CONFIGURAÇÕES BÁSICAS =================
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")
st.title("📊 Dashboard COVID-19 Interativo")

# ================= CARREGAR CSVs DISPONÍVEIS =================
csv_files = [f for f in os.listdir("output") if f.endswith(".csv")]
pais_selecionados = st.multiselect("🌍 Escolha os países:", csv_files, default=[csv_files[0]])

if not pais_selecionados:
    st.warning("⚠️ Selecione pelo menos um país!")
    st.stop()

# ================= INDICADORES DISPONÍVEIS =================
indicadores_disponiveis = {
    "casos_diarios": "Casos Diários",
    "mortes_diarias": "Mortes Diárias",
    "recuperados_diarios": "Recuperados Diários",
    "casos_7d_ma": "Casos (Média 7d)",
    "mortes_7d_ma": "Mortes (Média 7d)",
    "recuperados_7d_ma": "Recuperados (Média 7d)",
    "letalidade_pct": "Letalidade (%)",
    "recuperacao_pct": "Recuperação (%)",
    "casos_por_100k": "Casos por 100k habitantes"
}
metricas = st.multiselect("📌 Escolha as métricas:", list(indicadores_disponiveis.keys()), default=["casos_diarios"])


dfs = []
for arquivo in pais_selecionados:
    df = pd.read_csv(os.path.join("output", arquivo), parse_dates=['date'])
    df['pais'] = arquivo.replace("covid_", "").replace(".csv", "")
    dfs.append(df)

df_all = pd.concat(dfs)


min_date = df_all['date'].min()
max_date = df_all['date'].max()
start_date, end_date = st.slider(
    "⏳ Escolha o período:",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime())
)
df_filtered = df_all[(df_all['date'] >= start_date) & (df_all['date'] <= end_date)]

st.subheader("Indicadores-Chave")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Casos", f"{df_filtered['casos_diarios'].sum():,.0f}")
with col2:
    st.metric("Total de Mortes", f"{df_filtered['mortes_diarias'].sum():,.0f}")
with col3:
    st.metric("Taxa de Letalidade (%)", f"{df_filtered['letalidade_pct'].mean():.2f}")


aba1, aba2, aba3, aba4 = st.tabs(["📈 Séries Temporais", "🗺️ Mapas", "📋 Tabela", "📊 Comparações"])


with aba1:
    for metrica in metricas:
        st.subheader(f"{indicadores_disponiveis[metrica]} por País")
        fig = px.line(
            df_filtered,
            x='date',
            y=metrica,
            color='pais',
            title=f"{indicadores_disponiveis[metrica]} de COVID-19",
            labels={'date': 'Data', metrica: indicadores_disponiveis[metrica], 'pais': 'País'}
        )
        st.plotly_chart(fig, use_container_width=True)

with aba2:
    st.subheader("Distribuição Geográfica")
    if "casos_por_100k" in df_filtered.columns:
        df_last = df_filtered[df_filtered['date'] == df_filtered['date'].max()]
        fig_map = px.choropleth(
            df_last,
            locations="pais",
            locationmode="country names",
            color="casos_por_100k",
            hover_name="pais",
            title="Casos por 100k habitantes (última data)"
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("⚠️ Coluna 'casos_por_100k' não encontrada nos dados.")


with aba3:
    st.subheader("Tabela de Dados Filtrados")
    st.dataframe(df_filtered)


with aba4:
    if len(metricas) >= 2:
        st.subheader("Comparação de Métricas")
        fig_comp = go.Figure()
        for metrica in metricas:
            fig_comp.add_trace(go.Bar(
                x=df_filtered.groupby("pais")[metrica].sum().index,
                y=df_filtered.groupby("pais")[metrica].sum().values,
                name=indicadores_disponiveis[metrica]
            ))
        fig_comp.update_layout(barmode='group', title="Comparação de Indicadores por País")
        st.plotly_chart(fig_comp, use_container_width=True)
    else:
        st.info("Selecione ao menos 2 métricas para comparação.")
