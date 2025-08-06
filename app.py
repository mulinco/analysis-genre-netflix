# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  # SUGESTÃO: Importar Plotly para gráficos interativos
import os
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    layout="wide",
    page_title="Análise de Gêneros de Filmes/Séries",
    page_icon="🎬"
)

# --- FUNÇÕES DE PROCESSAMENTO DE DADOS ---

@st.cache_data # Cache para carregar os dados apenas uma vez
def load_data():
    """Carrega os dados já pré-processados."""
    try:
        df = pd.read_csv('data/processed/data_tratada.csv', encoding='utf-8-sig')
        # Não precisa mais de aplicar a limpeza aqui!
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar ou processar os dados: {str(e)}")
        return None

def clean_and_standardize_genres(genres_str):
    """
    Padroniza os gêneros, consolida subgêneros e remove inconsistências,
    lidando com múltiplos separadores e combinações específicas.
    """
    if pd.isna(genres_str) or not isinstance(genres_str, str):
        return ''

    # Dicionário de mapeamento para padronizar nomes de gêneros
    genre_mapping = {
        'action adventure': 'action',
        'action-adventure': 'action',
        'sci-fi fantasy': 'science fiction',
        'war politics': 'war',
        'film-noir': 'noir',
        'tv movie': 'movie',
        'sci-fi': 'science fiction',
        'science-fiction': 'science fiction',
        'sci fi': 'science fiction',
        'reality-tv': 'reality',
        'talk-show': 'talk show',
        'game-show': 'game show',
        'musical': 'music'
    }

    # 1. Limpa caracteres de lista e converte para minúsculas
    processed_str = str(genres_str).lower().replace('[','').replace(']','').replace("'",'').replace('"','')
    
    # 2. Aplica mapeamentos de frases completas primeiro
    for key, value in genre_mapping.items():
        processed_str = processed_str.replace(key, value)

    # 3. Divide a string em uma lista de gêneros usando múltiplos separadores
    genres_list = re.split(r'[,/&;]', processed_str)
    
    # 4. Limpa espaços em branco e remove strings vazias, criando um conjunto para valores únicos
    mapped_genres = {g.strip() for g in genres_list if g.strip()}

    # 5. Lógica de consolidação para combinações específicas
    # Se um filme é 'Action' e 'Adventure', consideramos apenas 'Action'.
    if 'action' in mapped_genres and 'adventure' in mapped_genres:
        mapped_genres.remove('adventure')
    
    # Se um filme é 'Science Fiction' e 'Fantasy', consideramos apenas 'Science Fiction'.
    if 'science fiction' in mapped_genres and 'fantasy' in mapped_genres:
        mapped_genres.remove('fantasy')

    # 6. Retorna a string final, ordenada e com letras maiúsculas
    if not mapped_genres:
        return ''
    return ','.join(sorted([g.title() for g in mapped_genres]))

    # Primeiro, aplicamos o mapeamento para frases completas
    genres_str_lower = str(genres_str).lower()
    for key, value in genre_mapping.items():
        if key in genres_str_lower:
            genres_str_lower = genres_str_lower.replace(key, value)

    # Agora, separamos e limpamos os gêneros individuais
    genres = [g.strip() for g in genres_str_lower.split(',')]
    
    # Usamos um set para garantir que os gêneros sejam únicos após a limpeza
    cleaned_genres = set()

    for genre in genres:
        # Remove caracteres especiais e espaços extras
        cleaned = re.sub(r'[^\w\s-]', '', genre).strip()
        if cleaned:
            cleaned_genres.add(cleaned)

    # Retorna os gêneros em ordem alfabética e com a primeira letra maiúscula
    return ','.join(sorted([g.title() for g in cleaned_genres]))


def get_unique_genres(df):
    """Extrai uma lista de todos os gêneros únicos do DataFrame."""
    all_genres = set()
    # O método explode é mais eficiente para "desaninhar" listas
    df_exploded = df['genres'].str.split(',').explode()
    all_genres.update([g.strip() for g in df_exploded.dropna() if g.strip()])
    return sorted(list(all_genres))

# --- FUNÇÕES DE RENDERIZAÇÃO DAS ABAS (SUGESTÃO: Refatoração) ---
# Mover a lógica de cada aba para sua própria função deixa o código principal mais limpo.

def render_introduction_tab():
    """Renderiza o conteúdo da aba de Introdução."""
    st.header("Oi! Vem cá...")
    st.write("""
    Você já se perguntou por que a Netflix parece estar cheia de dramas e documentários nos últimos anos? Ou por que alguns gêneros sempre têm as notas mais altas? Eu também. Foi daí que surgiu a ideia de investigar os gêneros mais populares e bem avaliados da plataforma. 
    
#### Objetivo
Neste projeto, meu objetivo foi analisar padrões de popularidade, qualidade e evolução temporal dos títulos da Netflix, a partir de dados abertos disponíveis no Kaggle.
- **Dataset:** [Netflix Movies and TV Shows – Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)

---

#### O que eu fiz?

**Limpeza e pré-processamento**:
Comecei tratando valores ausentes e padronizando os gêneros que apareciam com muitas variações como 'Sci-Fi', 'Science Fiction' e 'Sci fi', e foram agrupados sob uma única categoria unificada.

**Análise exploratória**:
Depois, explorei os dados para entender padrões iniciais, como distribuições de nota e quantidade de títulos por gênero, duração média, entre outros.

**Criação de visualizações**:
Utilizei gráficos de barras, boxplots e contagens para revelar relações relevantes, por exemplo, a predominância de certos gêneros ou a variação das avaliações ao longo do tempo.

Desenvolvimento do dashboard com Streamlit:
Por fim, integrei as análises em um dashboard interativo usando o Streamlit. Ele permite ao usuário filtrar os dados por ano, tipo de produção (filme ou série), nota mínima e gêneros, facilitando a exploração personalizada dos resultados.



---

#### 🧭 Como Navegar
- **Popularidade:** Gêneros com mais lançamentos.
- **Distribuição:** Notas do IMDb por tipo/gênero.
- **Evolução Temporal:** Lançamentos por ano e gênero.
- **Dados Filtrados:** Tabela com os dados filtrados conforme os critérios selecionados na barra lateral.

---

#### 💡 Principais Insights
- O gênero **Drama** é o mais comum.
- Documentários tendem a ter notas **IMDb mais altas**.


---
""")

def render_popularity_tab(df):
    """Renderiza a aba de Popularidade com gráficos interativos."""
    st.subheader("Top Gêneros por Popularidade")
    
    if df.empty:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        return

    genre_counts = df['genres'].str.split(',').explode().str.strip().value_counts().reset_index()
    genre_counts.columns = ['Gênero', 'Contagem']
    genre_counts = genre_counts.sort_values('Contagem', ascending=False).head(10)
    
    # Começo do Plotly
    fig = px.bar(
        genre_counts,
        x='Contagem',
        y='Gênero',
        orientation='h',
        title="Gêneros Mais Frequentes",
        color='Contagem',
        color_continuous_scale=px.colors.sequential.Viridis,
        labels={'Contagem': 'Número de Títulos', 'Gênero': 'Gênero'}
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}) # Ordena o eixo Y
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Tabela: Gêneros Mais Frequentes")
    st.dataframe(genre_counts, use_container_width=True)

def render_distribution_tab(df):
    """Renderiza a aba de Distribuição de Avaliações."""
    st.subheader("Distribuição de Avaliações por Gênero")
    
    if df.empty:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        return
        
    current_genres = get_unique_genres(df)
    if not current_genres:
        st.info("Nenhum gênero para analisar com os filtros atuais.")
        return
        
    genre_to_analyze = st.selectbox("Selecione um gênero para detalhar:", options=current_genres)
    
    # SUGESTÃO: Usar Plotly também para o histograma
    genre_df = df[df['genres'].str.contains(re.escape(genre_to_analyze), na=False)]
    fig = px.histogram(
        genre_df,
        x='imdbAverageRating',
        nbins=30,
        title=f"Distribuição de Avaliações - {genre_to_analyze}",
        labels={'imdbAverageRating': 'Avaliação IMDb'},
        marginal="box" # Adiciona um boxplot para ver a distribuição
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # ... (resto da sua lógica da aba de distribuição)

def render_temporal_evolution_tab(df):
    """Renderiza a aba de Evolução Temporal."""
    st.subheader("Evolução Temporal das Análises")

    if df.empty:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        return

    # Gráfico de linha - Média de avaliações por ano
    st.markdown("#### Média de Avaliações por Ano")
    avg_rating_by_year = df.groupby('releaseYear')['imdbAverageRating'].mean().reset_index()
    fig1 = px.line(
        avg_rating_by_year,
        x='releaseYear',
        y='imdbAverageRating',
        title="Média de Avaliações IMDb ao Longo dos Anos",
        labels={'releaseYear': 'Ano de Lançamento', 'imdbAverageRating': 'Avaliação Média'}
    )
    fig1.update_traces(line_color='royalblue', line_width=2)
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico de barras - Quantidade de lançamentos por ano
    st.markdown("#### Quantidade de Lançamentos por Ano")
    year_counts = df['releaseYear'].value_counts().sort_index().reset_index()
    year_counts.columns = ['releaseYear', 'count']
    
    # SUGESTÃO: Usar um gráfico de área para esta visualização, fica ótimo!
    fig2 = px.area(
        year_counts,
        x='releaseYear',
        y='count',
        title="Número de Lançamentos por Ano",
        labels={'releaseYear': 'Ano de Lançamento', 'count': 'Quantidade de Títulos'}
    )
    st.plotly_chart(fig2, use_container_width=True)

def render_correlation_tab(df):
    """SUGESTÃO: Nova aba para análise de correlação."""
    st.subheader("Análise de Correlação entre Métricas")
    st.markdown("""
    Esta análise nos ajuda a entender como as variáveis numéricas se relacionam. 
    Por exemplo, uma correlação positiva entre `imdbNumVotes` e `imdbAverageRating` 
    sugere que títulos com mais votos tendem a ter notas maiores.
    """)

    if df.empty:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        return

    # Selecionar apenas colunas numéricas para a correlação
    corr_df = df[['releaseYear', 'imdbAverageRating', 'imdbNumVotes']].copy()
    corr_matrix = corr_df.corr()

    # Criar o heatmap com Matplotlib e Seaborn
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr_matrix,
        annot=True,       # Mostra os valores de correlação
        cmap='coolwarm',  # Paleta de cores
        fmt=".2f",        # Formata os números para 2 casas decimais
        linewidths=.5,
        ax=ax
    )
    ax.set_title("Matriz de Correlação")
    st.pyplot(fig)

def render_filtered_data_tab(df):
    """Renderiza a aba com a tabela de dados filtrados."""
    st.subheader("📋 Dados Filtrados")
    st.dataframe(
        df.sort_values('imdbAverageRating', ascending=False),
        height=400,
        use_container_width=True
    )
    
    # Converter para CSV para o botão de download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados Filtrados (CSV)",
        data=csv,
        file_name='dados_filtrados.csv',
        mime='text/csv'
    )

def render_about_tab():
    """Renderiza a aba Sobre Mim."""
    st.markdown("#### 👩‍💻 Sobre o Projeto e Sobre Mim")
    st.write("""
    Desenvolvido por mim, **Maria Rodrigues** 🙂 \n
    Sou estudante de Ciências Biológicas na UFRJ, com foco em Genética, e atuo como bolsista de Iniciação Científica em Bioinformática. Curto muito tudo que envolve dados, tecnologia e ciência, e esse projeto faz parte do meu portfólio na área de **Data Science**, uma área que venho explorando com bastante dedicação.

    Se quiser trocar ideia ou acompanhar meus projetos, tô por aqui:  
    🐙 [GitHub](https://github.com/mulinco)  
    💼 [LinkedIn](https://www.linkedin.com/in/mariaclararodrigues3113)
    """)


# --- LAYOUT PRINCIPAL DO APP ---

st.title("📊 Análise de Gêneros de Filmes/Séries")

df = load_data()

if df is not None:
    # --- BARRA LATERAL DE FILTROS ---
    with st.sidebar:
        st.header("🔍 Filtros Interativos")
        
        available_types = sorted(df['type'].unique())
        selected_type = st.selectbox("Selecione o tipo:", options=['Todos'] + available_types, index=0)
        
        min_year, max_year = int(df['releaseYear'].min()), int(df['releaseYear'].max())
        selected_years = st.slider("Selecione o intervalo de anos:", min_year, max_year, (min_year, max_year))
        
        unique_genres = get_unique_genres(df)
        selected_genres = st.multiselect("Selecione gêneros:", options=unique_genres, default=['Action', 'Comedy', 'Drama'])
        
        min_rating, max_rating = float(df['imdbAverageRating'].min()), float(df['imdbAverageRating'].max())
        rating_range = st.slider("Filtrar por avaliação IMDb:", min_rating, max_rating, (6.0, 9.0), step=0.1)

    # --- LÓGICA DE FILTRAGEM ---
    # Começa com uma cópia do dataframe original
    filtered_df = df.copy()
    
    # Aplica os filtros sequencialmente
    filtered_df = filtered_df[
        (filtered_df['releaseYear'].between(*selected_years)) &
        (filtered_df['imdbAverageRating'].between(*rating_range))
    ]
    
    if selected_type != 'Todos':
        filtered_df = filtered_df[filtered_df['type'] == selected_type]
    
    if selected_genres:
        # Lógica de filtro "OU" para gêneros: um título precisa ter pelo menos um dos gêneros selecionados
        genre_pattern = '|'.join([re.escape(g) for g in selected_genres])
        filtered_df = filtered_df[filtered_df['genres'].str.contains(genre_pattern, na=False, regex=True)]

    # --- EXIBIÇÃO DAS MÉTRICAS GERAIS ---
    st.subheader("📈 Métricas Gerais (com base nos filtros)")
    if not filtered_df.empty:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total de Títulos", f"{len(filtered_df):,}")
        with col2:
            st.metric("Nota Média", f"{filtered_df['imdbAverageRating'].mean():.2f}")
        with col3:
            st.metric("Total de Votos", f"{filtered_df['imdbNumVotes'].sum():,}")
        with col4:
            st.metric("Média de Votos/Título", f"{filtered_df['imdbNumVotes'].mean():.0f}")
        with col5:
            st.metric("Desvio das Notas", f"{filtered_df['imdbAverageRating'].std():.2f}")
    else:
        st.info("Nenhum título encontrado com os filtros selecionados. Tente ampliar suas escolhas.")

    # --- ABAS DE NAVEGAÇÃO ---
    tab_intro, tab_pop, tab_dist, tab_evo, tab_corr, tab_data, tab_about = st.tabs([
        "📚 Introdução", "📊 Popularidade", "🎭 Distribuição", 
        "📅 Evolução Temporal", "🔗 Correlações", "📎 Dados Filtrados", "👩‍💻 Sobre Mim"
    ])
    
    with tab_intro:
        render_introduction_tab()
    with tab_pop:
        render_popularity_tab(filtered_df)
    with tab_dist:
        render_distribution_tab(filtered_df) 
    with tab_evo:
        render_temporal_evolution_tab(filtered_df)
    with tab_corr:
        render_correlation_tab(filtered_df)
    with tab_data:
        render_filtered_data_tab(filtered_df)
    with tab_about:
        render_about_tab()
        
else:
    st.warning("Não foi possível carregar os dados. O aplicativo não pode ser exibido.")

