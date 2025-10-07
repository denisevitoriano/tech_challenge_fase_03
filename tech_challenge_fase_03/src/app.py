import streamlit as st
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import tree
import plotly.express as px

# ======================================================
# 🔧 CONFIGURAÇÕES INICIAIS
# ======================================================
st.set_page_config(page_title="Análise de Vendedores e Clusters", layout="wide")

st.title("📊 Segmentação de Vendedores")
st.markdown("""
Explore o comportamento dos vendedores e a composição dos clusters de forma interativa.

Use o filtro lateral para selecionar o período analisado.
""")

st.caption("💡 Dica: passe o mouse sobre os gráficos para ver valores detalhados e use o zoom para explorar regiões específicas.")

# ======================================================
# 📥 LEITURA E TRATAMENTO DO DATAFRAME
# ======================================================
BASE_DIR = Path(__file__).resolve().parent.parent  # sobe 1 nível (do src para a raiz)
DATA_PATH = BASE_DIR / "data" / "03_model" / "clustering_output.csv"

df = pd.read_csv(DATA_PATH)

# Garantindo que a coluna data esteja no formato correto
df['data'] = pd.to_datetime(df['data'], errors='coerce')
df['data'] = df['data'].dt.date

cluster_col = 'cluster_id'
feature_cols = [c for c in df.columns if c.startswith('recbruta_') and c.endswith('_prop')]

cluster_colors = {
    '0': '#1F77B4',
    '1': '#FF7F0E',
    '2': '#2CA02C',
    '3': '#D62728',
    '4': '#9467BD',
    '5': '#8C564B',
    '6': '#E377C2',
    '7': '#7F7F7F',
    '8': '#BCBD22',
}

# ======================================================
# 🧭 SIDEBAR – FILTROS
# ======================================================
st.sidebar.header("⚙️ Filtros")

# Criando lista de datas únicas ordenadas
available_dates = sorted(df['data'].unique())

# Selecionador único de data (dropdown)
selected_date = st.sidebar.selectbox(
    "Selecione a data de referência:",
    options=available_dates,
    index=len(available_dates) - 1,  # seleciona a mais recente por padrão
)

# Aplicando filtros
df_filtrado = df[df['data'] == selected_date].copy()
df_filtrado[cluster_col] = df_filtrado[cluster_col].astype(str)

# ======================================================
# 📈 GRÁFICO 1 – Evolução de Vendedores por Categoria
# ======================================================
st.subheader("📆 Evolução de Vendedores por Categoria")

# Agrupando por data e cluster para contar quantos sellers ativos existem
df_vendedores_cluster = (
    df.groupby(['data', 'cluster_id'])
    .agg(num_vendedores = ('seller_id', 'nunique'))
    .reset_index()
)

# Criação do gráfico
fig_cluster = px.line(
    df_vendedores_cluster,
    x='data',
    y='num_vendedores',
    color='cluster_id',
    markers=True,
    title="Evolução da quantidade de vendedores por cluster",
    color_discrete_map=cluster_colors,
    category_orders={cluster_col: sorted(df_filtrado[cluster_col].unique(), key=lambda x: int(x))}
)

fig_cluster.update_layout(
    xaxis_title="",
    yaxis_title="# Vendedores",
    legend_title="Cluster",
    template="plotly_white",
    legend=dict(orientation="h", y=-0.25)
)

st.plotly_chart(fig_cluster, use_container_width=True)

st.divider()

# ======================================================
# 📊 GRÁFICO 2 – Distribuição de Vendedores por Cluster
# ======================================================
st.subheader("📊 Distribuição de Vendedores por Cluster")

cluster_counts = df_filtrado[cluster_col].value_counts().reset_index()
cluster_counts.columns = ['cluster_id', 'num_vendedores']

fig_bar = px.bar(
    cluster_counts,
    x='cluster_id',
    y='num_vendedores',
    color='cluster_id',
    text='num_vendedores',
    title='Distribuição de Vendedores por Cluster',
    color_discrete_map=cluster_colors,
    category_orders={cluster_col: sorted(df_filtrado[cluster_col].unique(), key=lambda x: int(x))}
)
fig_bar.update_traces(textposition='outside')
fig_bar.update_layout(
    xaxis_title="",
    yaxis_title="# Vendedores",
    template='plotly_white',
    legend_title_text='Cluster',
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ======================================================
# 🧩 GRÁFICO 3 – PCA dos Clusters
# ======================================================
st.subheader("🧬 Distribuição dos Vendedores (PCA)")

# Padroniza os dados para o PCA (média=0, desvio=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_filtrado[feature_cols].fillna(0))

# Aplica o PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(X_scaled)

# Adiciona os componentes principais ao dataframe
df_filtrado['pca1'] = pca_result[:, 0]
df_filtrado['pca2'] = pca_result[:, 1]

fig_pca = px.scatter(
    df_filtrado,
    x='pca1',
    y='pca2',
    color=cluster_col,
    hover_data=['seller_id'],
    title='Distribuição dos Vendedores por Cluster (PCA)',
    color_discrete_map=cluster_colors,
    category_orders={cluster_col: sorted(df_filtrado[cluster_col].unique(), key=lambda x: int(x))}
)

fig_pca.update_layout(
    xaxis_title="PCA1",
    yaxis_title="PCA2",
    template='plotly_white',
    legend_title_text='Cluster',
)

st.plotly_chart(fig_pca, use_container_width=True)

st.divider()

# ======================================================
# 🔥 GRÁFICO 4 – Heatmap Interativo dos Clusters
# ======================================================
st.subheader("🔥 Heatmap Interativo dos Clusters")

# Treina modelo de árvore de decisão para selecionar as features mais importantes
X = df_filtrado[feature_cols]
y = df_filtrado[cluster_col]

clf = tree.DecisionTreeClassifier(random_state=42)
clf.fit(X, y)

# Importância das variáveis
feature_importance = pd.Series(clf.feature_importances_, index=feature_cols).sort_values(ascending=False)

# Permite ao usuário escolher o número de features
n_features = st.slider(
    "Selecione o número de features mais importantes",
    min_value=3,
    max_value=min(20, len(feature_importance)),
    value=10
)

# Seleciona as top features
top_features = feature_importance.index[:n_features].tolist()

# f_filtrado.groupby(cluster_col)[feature_cols].mean().round(2)
mean_by_cluster = (
    df_filtrado
    .groupby(cluster_col)
    .agg({col: 'mean' for col in top_features})
    .reset_index()
)

fig_heatmap = px.imshow(
    mean_by_cluster.set_index(cluster_col)[top_features].T,
    color_continuous_scale='Viridis',
    labels=dict(x='Cluster', y="Features", color="Valor Médio"),
    title=f"Heatmap - Médias das {n_features} Features Mais Importantes por Cluster"
)
fig_heatmap.update_layout(
    template='plotly_white',
    height=550
)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.divider()

# ======================================================
# 📋 TABELA – Perfil Médio por Cluster
# ======================================================
st.subheader("📈 Receita Média por Cluster")

st.dataframe(mean_by_cluster.style.highlight_max(axis=0, color='lightgreen'))

st.divider()