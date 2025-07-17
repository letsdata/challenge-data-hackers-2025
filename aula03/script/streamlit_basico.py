# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout.
# "wide" faz com que o conteúdo ocupe toda a largura da tela.
st.set_page_config(page_title="Explorador de Expectativa de Vida", layout="wide")

# --- Título e Descrição ---
# Exibe o título principal da aplicação.
st.title("🌍 Gapminder Explorer")
# Fornece uma breve instrução sobre como usar a aplicação.
st.markdown("Filtre por ano e continente para explorar dados de população e expectativa de vida.")

# --- Carregamento de Dados ---
# A anotação @st.cache_data garante que os dados sejam carregados apenas uma vez,
# melhorando a performance da aplicação. O resultado da função é armazenado em cache.
@st.cache_data
def load_data():
    # Carrega o conjunto de dados 'gapminder' que vem com a biblioteca Plotly Express.
    return px.data.gapminder()

# Chama a função para carregar os dados.
df = load_data()

# --- Barra Lateral (Sidebar) com Filtros ---
# Cria um cabeçalho para a seção de filtros na barra lateral.
st.sidebar.header("Filtros")
# Cria um slider para selecionar o ano.
# Os valores mínimo e máximo são definidos dinamicamente a partir dos dados.
# O valor padrão é 2007.
year = st.sidebar.slider("Ano", int(df.year.min()), int(df.year.max()), 2007)
# Cria uma caixa de seleção múltipla para os continentes.
# As opções são os continentes únicos presentes no DataFrame.
# Por padrão, todos os continentes vêm selecionados.
continents = st.sidebar.multiselect(
    "Continente", options=df.continent.unique(), default=df.continent.unique()
)

# --- Filtragem dos Dados ---
# Filtra o DataFrame com base no ano e nos continentes selecionados pelo usuário.
df_filt = df[(df.year == year) & (df.continent.isin(continents))]

# --- Métricas Resumidas ---
# Cria três colunas para exibir métricas lado a lado.
col1, col2, col3 = st.columns(3)
# Exibe o número de registros (linhas) no DataFrame filtrado.
col1.metric("Registros", len(df_filt))
# Exibe a expectativa de vida mínima, formatada com uma casa decimal.
col2.metric("Mín. Vida", f"{df_filt.lifeExp.min():.1f}")
# Exibe a expectativa de vida máxima, formatada com uma casa decimal.
col3.metric("Máx. Vida", f"{df_filt.lifeExp.max():.1f}")

# Adiciona uma linha horizontal para separar seções.
st.markdown("---")

# --- Layout Principal: Tabela e Gráfico ---
# Cria duas colunas para organizar o conteúdo principal.
# A coluna da direita (right) será duas vezes mais larga que a da esquerda (left).
left, right = st.columns((1, 2))

# --- Coluna da Esquerda: Tabela de Dados ---
with left:
    # Adiciona um subtítulo para a seção de dados.
    st.subheader("Dados")
    # Exibe o DataFrame filtrado em uma tabela interativa.
    # 'reset_index(drop=True)' reinicia o índice para uma melhor visualização.
    # 'use_container_width=True' faz a tabela ocupar toda a largura da coluna.
    st.dataframe(df_filt.reset_index(drop=True), use_container_width=True)

# --- Coluna da Direita: Gráfico de Dispersão ---
with right:
    # Adiciona um subtítulo para a seção do gráfico.
    st.subheader("Expectativa vs PIB per capita")
    # Cria um gráfico de dispersão (scatter plot) com Plotly Express.
    fig = px.scatter(
        df_filt,
        x="gdpPercap",          # Eixo X: PIB per capita
        y="lifeExp",            # Eixo Y: Expectativa de vida
        size="pop",             # Tamanho da bolha: População
        color="continent",      # Cor da bolha: Continente
        hover_name="country",   # Texto ao passar o mouse: Nome do país
        log_x=True,             # Eixo X em escala logarítmica para melhor visualização
        size_max=60,            # Tamanho máximo das bolhas
        title=f"{year} – Vida vs PIB", # Título do gráfico dinâmico com o ano
    )
    # Exibe o gráfico Plotly na aplicação.
    # 'use_container_width=True' faz o gráfico ocupar toda a largura da coluna.
    st.plotly_chart(fig, use_container_width=True)
