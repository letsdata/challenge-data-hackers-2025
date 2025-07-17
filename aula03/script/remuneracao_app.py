
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import json
import requests

# --- Configuração da Página ---
st.set_page_config(page_title="Análise de Salários", layout="wide")

# --- Título e Descrição ---
st.title("Análise de Salários de Profissionais de Dados no Brasil")
st.markdown("Explore as remunerações por cargo, nível de experiência e outros filtros.")

# --- Carregamento de Dados ---
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/dataset_salarios_dados.csv')
    return df

df = load_data()

# --- Barra Lateral (Sidebar) com Filtros ---
st.sidebar.header("Filtros")
cargos = st.sidebar.multiselect(
    "Cargo", options=df.cargo_atual.unique(), default=df.cargo_atual.unique()
)

generos = st.sidebar.multiselect(
    "Gênero", options=df.genero.unique(), default=df.genero.unique()
)

# Definindo a ordem da experiência
ordem_experiencia = [
    'Não tenho experiência na área de dados',
    'Menos de 1 ano',
    'de 1 a 2 anos',
    'de 3 a 5 anos',
    'de 6 a 10 anos',
    'Mais de 10 anos'
]
df['tempo_experiencia_dados'] = pd.Categorical(df['tempo_experiencia_dados'], categories=ordem_experiencia, ordered=True)

experiencia = st.sidebar.multiselect(
    "Tempo de Experiência em Dados", 
    options=ordem_experiencia, 
    default=ordem_experiencia
)

df_filt = df[
    (df.cargo_atual.isin(cargos)) & 
    (df.genero.isin(generos)) & 
    (df.tempo_experiencia_dados.isin(experiencia))
]


# --- Ordem das faixas salariais ---
ordem_faixa_salarial = [
    'Menos de R$ 1.000/mês',
    'de R$ 1.001/mês a R$ 2.000/mês',
    'de R$ 2.001/mês a R$ 3.000/mês',
    'de R$ 3.001/mês a R$ 4.000/mês',
    'de R$ 4.001/mês a R$ 6.000/mês',
    'de R$ 6.001/mês a R$ 8.000/mês',
    'de R$ 8.001/mês a R$ 12.000/mês',
    'de R$ 12.001/mês a R$ 16.000/mês',
    'de R$ 16.001/mês a R$ 20.000/mês',
    'de R$ 20.001/mês a R$ 25.000/mês',
    'de R$ 25.001/mês a R$ 30.000/mês',
    'de R$ 30.001/mês a R$ 40.000/mês',
    'Acima de R$ 40.001/mês'
]

# --- Visualizações ---
st.header("Distribuição de Salários")

# Gráfico de barras da faixa salarial
s_faixa_salarial = pd.Series(df_filt['faixa_salarial'])
df_faixa_salarial = s_faixa_salarial.value_counts().reset_index()
df_faixa_salarial.columns = ['faixa_salarial', 'contagem']

# Convertendo a coluna para tipo Categoria com a ordem definida
df_faixa_salarial['faixa_salarial'] = pd.Categorical(df_faixa_salarial['faixa_salarial'], categories=ordem_faixa_salarial, ordered=True)
df_faixa_salarial = df_faixa_salarial.sort_values('faixa_salarial')

fig_faixa = px.bar(
    df_faixa_salarial,
    x='faixa_salarial',
    y='contagem',
    title='Distribuição de Faixas Salariais',
    labels={'faixa_salarial': 'Faixa Salarial', 'contagem': 'Número de Profissionais'},
    text_auto=True
)
st.plotly_chart(fig_faixa, use_container_width=True)

st.markdown("---")

st.header("Análise por Cargo")
# Gráfico de barras dos cargos
s_cargos = pd.Series(df_filt['cargo_atual'])
df_cargos = s_cargos.value_counts().reset_index()
df_cargos.columns = ['cargo_atual', 'contagem']

fig_cargos = px.bar(
    df_cargos,
    y='cargo_atual',
    x='contagem',
    orientation='h',
    title='Distribuição de Cargos',
    labels={'cargo_atual': 'Cargo Atual', 'contagem': 'Número de Profissionais'},
    text_auto=True
)
fig_cargos.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_cargos, use_container_width=True)

st.markdown("---")

# --- Gráficos Demográficos ---
st.header("Análises Demográficas")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribuição por Gênero")
    s_genero = pd.Series(df_filt['genero'])
    df_genero = s_genero.value_counts().reset_index()
    df_genero.columns = ['genero', 'contagem']
    fig_genero = px.treemap(
        df_genero,
        path=['genero'],
        values='contagem',
        title='Proporção de Gêneros'
    )
    st.plotly_chart(fig_genero, use_container_width=True)

with col2:
    st.subheader("Distribuição por Experiência")
    s_experiencia = pd.Series(df_filt['tempo_experiencia_dados'])
    df_experiencia = s_experiencia.value_counts().reset_index()
    df_experiencia.columns = ['experiencia', 'contagem']
    df_experiencia['experiencia'] = pd.Categorical(df_experiencia['experiencia'], categories=ordem_experiencia, ordered=True)
    df_experiencia = df_experiencia.sort_values('experiencia')
    fig_experiencia = px.bar(
        df_experiencia,
        x='experiencia',
        y='contagem',
        title='Níveis de Experiência na Área de Dados',
        labels={'experiencia': 'Tempo de Experiência', 'contagem': 'Número de Profissionais'},
        text_auto=True
    )
    st.plotly_chart(fig_experiencia, use_container_width=True)

st.markdown("---")

# --- Análises Cruzadas com Salário ---
st.header("Salário vs. Outras Variáveis")

st.subheader("Faixa Salarial por Gênero")
df_salario_genero = df_filt.groupby(['faixa_salarial', 'genero'], observed=True).size().reset_index(name='contagem')
df_salario_genero['faixa_salarial'] = pd.Categorical(df_salario_genero['faixa_salarial'], categories=ordem_faixa_salarial, ordered=True)
df_salario_genero = df_salario_genero.sort_values('faixa_salarial')

fig_sal_gen = px.bar(
    df_salario_genero,
    x='faixa_salarial',
    y='contagem',
    color='genero',
    barmode='group',
    title='Comparativo de Faixa Salarial por Gênero',
    labels={'faixa_salarial': 'Faixa Salarial', 'contagem': 'Número de Profissionais', 'genero': 'Gênero'},
)
st.plotly_chart(fig_sal_gen, use_container_width=True)

st.subheader("Hierarquia de Experiência e Salário")
df_treemap_exp_sal = df_filt.groupby(['tempo_experiencia_dados', 'faixa_salarial'], observed=True).size().reset_index(name='contagem')
fig_treemap = px.treemap(
    df_treemap_exp_sal,
    path=['tempo_experiencia_dados', 'faixa_salarial'],
    values='contagem',
    title='Distribuição de Salário por Nível de Experiência',
    color='tempo_experiencia_dados',
    color_discrete_map={'(?)':'black', 'Menos de 1 ano':'gold', 'de 1 a 2 anos':'darkorange', 'de 3 a 5 anos':'red', 'de 6 a 10 anos': 'darkred', 'Mais de 10 anos': 'maroon'}
)
st.plotly_chart(fig_treemap, use_container_width=True)

st.markdown("---")

# --- Análise Geográfica ---
st.header("Análise Geográfica de Salários")

# Função para converter faixa salarial para valor numérico
def converte_salario_para_numero(faixa):
    if isinstance(faixa, str):
        numeros = [int(s) for s in re.findall(r'\d+', faixa)]
        if 'Menos de' in faixa:
            return numeros[0] * 1000
        elif 'Acima de' in faixa:
            return numeros[0] * 1000
        elif len(numeros) == 2:
            return ((numeros[0] + numeros[1]) / 2) * 1000
        elif len(numeros) == 4: # Formato de 1.001 a 2.000
            return ((numeros[0] * 1000 + numeros[1]) + (numeros[2] * 1000 + numeros[3])) / 2
    return None

# Carregar GeoJSON do Brasil
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/giuliano-macedo/geodata-br-states/refs/heads/main/geojson/br_states.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança um erro para status HTTP ruins
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao carregar dados geográficos: {e}")
        return None
    except json.JSONDecodeError:
        st.error("Erro ao decodificar os dados geográficos. O formato pode ser inválido.")
        return None

geojson = load_geojson()

if geojson:
    # Get all state abbreviations from GeoJSON
    all_states = [feature['id'] for feature in geojson.get('features', [])]
    df_all_states = pd.DataFrame(data=all_states, columns=['uf_residencia'])

    df_mapa = df_filt.copy()
    df_mapa['salario_medio'] = pd.Series(df_mapa['faixa_salarial']).apply(converte_salario_para_numero)

    df_estado_salario = df_mapa.groupby('uf_residencia')['salario_medio'].mean().reset_index()

    # Merge with all states to include those with no data
    df_mapa_completo = pd.merge(df_all_states, df_estado_salario, on='uf_residencia', how='left')

    # Binning the salary data
    bins = [0, 4000, 8000, 12000, 16000, 20000, 100000]
    labels = [
        'Até R$4k', 
        'R$4k - R$8k', 
        'R$8k - R$12k',
        'R$12k - R$16k', 
        'R$16k - R$20k', 
        'Acima de R$20k'
    ]
    df_mapa_completo['faixa_salario_medio'] = pd.cut(df_mapa_completo['salario_medio'], bins=bins, labels=labels, right=False)

    # Fill NaN with "Sem Informação"
    # Usando .cat.add_categories antes de fillna para tratar como categoria
    df_mapa_completo['faixa_salario_medio'] = df_mapa_completo['faixa_salario_medio'].cat.add_categories(['Sem Informação'])
    df_mapa_completo['faixa_salario_medio'].fillna('Sem Informação', inplace=True)
    
    # Criar mapa coroplético
    fig_mapa = px.choropleth(
        df_mapa_completo,
        geojson=geojson,
        locations='uf_residencia',
        featureidkey="id",
        color='faixa_salario_medio',
        color_discrete_map={
            'Sem Informação': 'lightgrey',
            'Até R$4k': '#eff3ff',
            'R$4k - R$8k': '#c6dbef',
            'R$8k - R$12k': '#9ecae1',
            'R$12k - R$16k': '#6baed6',
            'R$16k - R$20k': '#3182bd',
            'Acima de R$20k': '#08519c'
        },
        category_orders={'faixa_salario_medio': labels + ['Sem Informação']},
        scope="south america",
        title="Média Salarial por Estado",
        labels={'uf_residencia':'Estado', 'faixa_salario_medio':'Faixa Salarial Média (R$)'}
    )
    fig_mapa.update_layout(height=800)
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_mapa, use_container_width=True)
else:
    st.warning("O mapa não pôde ser exibido pois os dados geográficos não foram carregados.") 