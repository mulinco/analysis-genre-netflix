# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import KNNImputer
import os
import re
from collections import defaultdict


st.set_page_config(layout="wide", page_title="Análise de Gêneros Netflix", page_icon="🎬")


st.title("📊 Análise de Gêneros de Filmes/Séries")

@st.cache_data
def load_data():
    try:
        file_path = os.path.abspath('C:/Users/mulin/OneDrive/Documentos/analysis-genre-netflix/data/processed/data_tratada.csv')
        st.write(f"Carregando dados de: {file_path}")
        
        if not os.path.exists(file_path):
            st.error("Arquivo não encontrado no caminho especificado!")
            return None
            
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        
        
        required_columns = {'imdbAverageRating', 'imdbNumVotes', 'genres', 'releaseYear', 'type'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            st.error(f"Colunas faltantes: {missing}")
            return None
        
        
        df['genres'] = df['genres'].apply(clean_and_standardize_genres)
            
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

def clean_and_standardize_genres(genres_str):
    """Padroniza os gêneros e consolida duplicados"""
    if pd.isna(genres_str):
        return ''
    
    
    genre_mapping = {
        'reality-tv': 'reality',
        'sci-fi': 'science fiction',
        'sci-fi fantasy': 'science fiction',
        'action adventure': 'action',
        'action-adventure': 'action',
        'tv movie': 'movie',
        'science-fiction': 'science fiction',
        'sci fi': 'science fiction',
        'sci fi fantasy': 'science fiction',
        'talk-show': 'talk show',
        'game-show': 'game show'
    }
    
    genres = [g.strip().lower() for g in str(genres_str).split(',')]
    cleaned_genres = []
    
    for genre in genres:
        standardized = genre_mapping.get(genre, genre)
        cleaned = re.sub(r'[^\w\s-]', '', standardized).strip()
        if cleaned and cleaned not in cleaned_genres:
            cleaned_genres.append(cleaned)
    
    return ','.join(sorted([g.title() for g in cleaned_genres]))

def get_unique_genres(df):
    """Obtém gêneros únicos após padronização"""
    all_genres = set()
    for genres in df['genres'].str.split(','):
        if isinstance(genres, list):
            all_genres.update([g.strip() for g in genres if g.strip()])
    return sorted(all_genres)


df = load_data()

if df is not None:
    with st.sidebar:
        st.header("🔍 Filtros Interativos")
        
        available_types = sorted(df['type'].unique())
        selected_type = st.selectbox("Selecione o tipo:", options=['Todos'] + available_types, index=0)
        
        min_year, max_year = int(df['releaseYear'].min()), int(df['releaseYear'].max())
        selected_years = st.slider("Selecione o intervalo de anos:", min_year, max_year, (min_year, max_year))
        
        unique_genres = get_unique_genres(df)
        selected_genres = st.multiselect("Selecione gêneros:", options=unique_genres, default=['Action', 'Comedy', 'Drama'])
        
        min_rating, max_rating = float(df['imdbAverageRating'].min()), float(df['imdbAverageRating'].max())
        rating_range = st.slider("Filtrar por avaliação IMDb:", min_rating, max_rating, (6.0, 9.0))

    
    filtered_df = df[
        (df['releaseYear'].between(*selected_years)) &
        (df['imdbAverageRating'].between(*rating_range))
    ]
    
    if selected_type != 'Todos':
        filtered_df = filtered_df[filtered_df['type'] == selected_type]
    
    if selected_genres:
        genre_pattern = '|'.join([re.escape(g) for g in selected_genres])
        filtered_df = filtered_df[filtered_df['genres'].str.contains(genre_pattern, na=False, regex=True)]

    
    st.subheader("📈 Métricas Gerais")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Total de Títulos", len(filtered_df))
    with col2:
        st.metric("Nota Média", f"{filtered_df['imdbAverageRating'].mean():.2f}")
    with col3:
        st.metric("Total de Votos", f"{filtered_df['imdbNumVotes'].sum():,}")
    with col4:
        st.metric("Ano Médio", int(filtered_df['releaseYear'].mean()))
    with col5:
        st.metric("Média de Votos/Título", f"{filtered_df['imdbNumVotes'].mean():.0f}")
    with col6:
        st.metric("Desvio das Notas", f"{filtered_df['imdbAverageRating'].std():.2f}")

    
    tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(["📚Introdução", "📊 Popularidade", "🎭 Distribuição", "📅 Evolução Temporal", "📎Dados Filtrados", "👩‍💻Sobre Mim"])
    
    with tab0:
        st.header("Oi! Vem cá...")
        st.write("""

Você já se perguntou por que a Netflix parece estar cheia de dramas e documentários nos últimos anos? Ou por que alguns gêneros sempre têm as notas mais altas? Eu também. Foi daí que surgiu a ideia de investigar os gêneros mais populares e bem avaliados da plataforma. 
 
---

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
- Houve um **aumento expressivo** de lançamentos em 2019.

---


""")


    with tab1:
        st.subheader("Top Gêneros por Popularidade")
        
        genre_counts = (filtered_df['genres'].str.split(',')
                       .explode()
                       .str.strip()
                       .value_counts()
                       .reset_index())
        genre_counts.columns = ['Gênero', 'Contagem']
        genre_counts = genre_counts.sort_values('Contagem', ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=genre_counts, x='Contagem', y='Gênero', palette="viridis", ax=ax)
        plt.title("Gêneros Mais Frequentes")
        plt.xlabel("Contagem")
        plt.ylabel("Gênero")
        st.pyplot(fig)

        st.markdown("### 📋 Tabela: Gêneros Mais Frequentes")
        st.dataframe(genre_counts, use_container_width=True)

    with tab2:
        st.subheader("Distribuição de Avaliações")
        
        current_genres = sorted(set(filtered_df['genres'].str.split(',').explode().str.strip().unique()))
        genre_to_analyze = st.selectbox("Selecione um gênero para detalhar:", options=current_genres)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(
            data=filtered_df[filtered_df['genres'].str.contains(re.escape(genre_to_analyze))],
            x='imdbAverageRating',
            bins=20,
            kde=True,
            color='skyblue'
        )
        plt.title(f"Distribuição de Avaliações - {genre_to_analyze}")
        plt.xlabel("Avaliação IMDb")
        st.pyplot(fig)

        selected_df = filtered_df[filtered_df['genres'].str.contains(re.escape(genre_to_analyze))]
        st.markdown(f"### 📋 Exemplos de títulos do gênero {genre_to_analyze}")
        st.dataframe(
            selected_df[['title', 'imdbAverageRating', 'imdbNumVotes', 'releaseYear']]
            .sort_values('imdbAverageRating', ascending=False)
            .head(10)
        )

        st.subheader("Comparação: Nota Média por Gênero e Tipo")

        
        exploded_df = filtered_df.copy()
        exploded_df = exploded_df.assign(genero=exploded_df['genres'].str.split(',')).explode('genero')
        exploded_df['genero'] = exploded_df['genero'].str.strip()

        
        generos_disponiveis = sorted(exploded_df['genero'].unique())

        
        generos_selecionados = st.multiselect(
            "Escolha os gêneros para comparar:",
            options=generos_disponiveis,
            default=['Drama', 'Comedy']
        )

       
        df_filtrado_generos = exploded_df[exploded_df['genero'].isin(generos_selecionados)]

        
        if not df_filtrado_generos.empty:
            media_genero_tipo = df_filtrado_generos.groupby(['genero', 'type'])['imdbAverageRating'].mean().reset_index()

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=media_genero_tipo, x='imdbAverageRating', y='genero', hue='type', palette='Set2', ax=ax)
            plt.xlabel("Nota Média IMDb")
            plt.ylabel("Gênero")
            plt.title("Nota Média por Gênero e Tipo (Selecionados)")
            st.pyplot(fig)
        else:
            st.info("Selecione ao menos um gênero para visualizar a comparação.")

    

    with tab3:
        st.subheader("Evolução Temporal das Avaliações")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(
            data=filtered_df,
            x='releaseYear',
            y='imdbAverageRating',
            estimator='mean',
            errorbar=None,
            color='royalblue',
            linewidth=2
        )
        plt.title("Média de Avaliações por Ano")
        plt.xlabel("Ano de Lançamento")
        plt.ylabel("Avaliação Média IMDb")
        st.pyplot(fig)
        st.subheader("Evolução Temporal das Avaliações")

         
        min_year, max_year = int(filtered_df['releaseYear'].min()), int(filtered_df['releaseYear'].max())
    
    
        selected_years = st.slider("Selecione o intervalo de anos:", 
                               min_year, max_year, 
                               (min_year, max_year),
                               key="year_slider")  # A chave "year_slider" é única

    
        filtered_by_year = filtered_df[filtered_df['releaseYear'].between(*selected_years)]

    
        st.subheader("Quantidade de Lançamentos por Ano")
        year_counts = filtered_by_year['releaseYear'].value_counts().sort_index()

   
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.histplot(
        year_counts,
        bins=len(year_counts),
        kde=False,
        color='lightblue',
        ax=ax
    )
        ax.set_xlabel("Ano de Lançamento")
        ax.set_ylabel("Quantidade de Títulos")
        ax.set_title("Número de Lançamentos por Ano")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with tab4:
    
        st.subheader("📋 Dados Filtrados")
        st.dataframe(
        filtered_df.sort_values('imdbAverageRating', ascending=False),
        height=400,
        use_container_width=True
    )
    
    
        st.download_button(
        label="📥 Baixar Dados Filtrados (CSV)",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='dados_filtrados.csv',
        mime='text/csv'
    )

    with tab5:
        #### 👩‍💻 Sobre o Projeto
        st.write(### Sobre mim

"""Desenvolvido por mim, **Maria Rodrigues** 🙂  \n
Sou estudante de Ciências Biológicas na UFRJ, com foco em Genética, e atuo como bolsista de Iniciação Científica em Bioinformática. Curto muito tudo que envolve dados, tecnologia e ciência, e esse projeto faz parte do meu portfólio na área de **Data Science**, uma área que venho explorando com bastante dedicação.

Se quiser trocar ideia ou acompanhar meus projetos, tô por aqui:  
🐙 [GitHub](https://github.com/mulinco)  
💼 [LinkedIn](https://www.linkedin.com/in/mariaclararodrigues3113)"""
)
   



    

else:
    st.warning("Não foi possível carregar os dados. Verifique o caminho do arquivo e tente novamente.") 