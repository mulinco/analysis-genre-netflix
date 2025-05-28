# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import re
from sklearn.impute import KNNImputer

# Configurações de visualização
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

def load_data(file_path):
    """Carrega os dados com tratamento"""
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        print(f"\nDados carregados: {len(df):,} registros")
        
        
        required_cols = {'title', 'type', 'genres', 'releaseYear', 'imdbAverageRating', 'imdbNumVotes'}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            raise ValueError(f"Colunas faltantes: {missing_cols}")
        
        return df
    
    except Exception as e:
        print(f"\nERRO ao carregar dados: {str(e)}")
        return None

def clean_genres(genres_str):
    """Limpa e padroniza os gêneros"""
    if pd.isna(genres_str):
        return ''
    genres = [g.strip() for g in str(genres_str).split(',')]
    # Remove caracteres especiais e duplicados
    cleaned = [re.sub(r'[^\w\s-]', '', g) for g in genres if g.strip()]
    return ','.join(sorted(list(set(cleaned))))

def preprocess_data(df):
    # Converter tipos
    df['releaseYear'] = pd.to_numeric(df['releaseYear'], errors='coerce')
    df['imdbAverageRating'] = pd.to_numeric(df['imdbAverageRating'], errors='coerce')
    df['imdbNumVotes'] = pd.to_numeric(df['imdbNumVotes'], errors='coerce')
    
    
    df['releaseYear'] = df['releaseYear'].fillna(df['releaseYear'].median()).astype(int)
    df['genres'] = df['genres'].fillna('Unknown')
    
   
    df['genres'] = df['genres'].apply(clean_genres)
    
    # Aplicar KNN para avaliações
    if df[['imdbAverageRating', 'imdbNumVotes']].isnull().any().any():
        imputer = KNNImputer(n_neighbors=3)
        df[['imdbAverageRating', 'imdbNumVotes']] = imputer.fit_transform(
            df[['imdbAverageRating', 'imdbNumVotes']])
    
    return df

def apply_filters(df, filters):
    """Aplica filtros com diagnóstico"""
    filtered_df = df.copy()
    
    print("\n=== DIAGNÓSTICO DOS FILTROS ===")
    print(f"Registros iniciais: {len(filtered_df):,}")
    
    
    if 'years' in filters:
        year_min, year_max = filters['years']
        filtered_df = filtered_df[filtered_df['releaseYear'].between(year_min, year_max)]
        print(f"Após filtrar anos ({year_min}-{year_max}): {len(filtered_df):,}")
    
    
    if 'rating_range' in filters:
        rating_min, rating_max = filters['rating_range']
        filtered_df = filtered_df[filtered_df['imdbAverageRating'].between(rating_min, rating_max)]
        print(f"Após filtrar avaliações ({rating_min}-{rating_max}): {len(filtered_df):,}")
    
    
    if 'type' in filters:
        if filters['type'] != 'Todos':
            before = len(filtered_df)
            filtered_df = filtered_df[filtered_df['type'] == filters['type']]
            print(f"Após filtrar tipo ({filters['type']}): {len(filtered_df):,} (removidos {before - len(filtered_df):,})")
        else:
            print("Nenhum filtro de tipo aplicado ('Todos' selecionado)")
    
    
    if 'genres' in filters and filters['genres']:
        genre_pattern = '|'.join([re.escape(g) for g in filters['genres']])
        filtered_df = filtered_df[filtered_df['genres'].str.contains(genre_pattern, na=False, regex=True)]
        print(f"Após filtrar gêneros ({filters['genres']}): {len(filtered_df):,}")
    
    return filtered_df

def generate_visualizations(filtered_df, output_dir='output'):
    """Gera visualizações e salva em arquivos"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if filtered_df.empty:
        print("\nAVISO: Nenhum dado para visualizações")
        return
    
    try:
        # Gráfico 1: Top gêneros 
        plt.figure()
        genre_counts = (filtered_df['genres'].str.split(',')
                       .explode()
                       .str.strip()
                       .value_counts()
                       .reset_index())
        genre_counts.columns = ['Gênero', 'Contagem']
        genre_counts['Gênero'] = genre_counts['Gênero'].apply(lambda x: re.sub(r'[^\w\s-]', '', x))
        genre_counts = genre_counts.groupby('Gênero').sum().reset_index().sort_values('Contagem', ascending=False).head(10)
        
        sns.barplot(data=genre_counts, x='Contagem', y='Gênero', palette="viridis")
        plt.title(f"Top Gêneros (n={len(filtered_df):,})")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/top_generos.png", dpi=300)
        plt.close()
        
        # Distribuição de avaliações para o gênero mais popular
        plt.figure()
        most_popular_genre = genre_counts.iloc[0]['Gênero']
        sns.histplot(
            filtered_df[filtered_df['genres'].str.contains(re.escape(most_popular_genre))],
            x='imdbAverageRating',
            bins=20,
            kde=True,
            color='skyblue'
        )
        plt.title(f"Distribuição de Avaliações - {most_popular_genre} (n={len(filtered_df):,})")
        plt.savefig(f"{output_dir}/distribuicao_avaliacoes.png", dpi=300)
        plt.close()
        
        #  Evolução temporal
        if filtered_df['releaseYear'].nunique() > 1:
            plt.figure()
            sns.lineplot(
                data=filtered_df,
                x='releaseYear',
                y='imdbAverageRating',
                estimator='mean',
                errorbar=None,
                color='royalblue',
                linewidth=2
            )
            plt.title(f"Evolução Temporal (n={len(filtered_df):,})")
            plt.savefig(f"{output_dir}/evolucao_temporal.png", dpi=300)
            plt.close()
        
        print(f"\nVisualizações salvas em: {os.path.abspath(output_dir)}")
    
    except Exception as e:
        print(f"\nERRO ao gerar gráficos: {str(e)}")

def analyze_data(df, filters=None):
    """Executa análise completa"""
    if filters is None:
        filters = {
            'years': (2000, 2023),
            'rating_range': (6.0, 10.0),
            'type': 'movie',
            'genres': ['Action', 'Adventure', 'Comedy']
        }
    
   
    filtered_df = apply_filters(df, filters)
    
    if filtered_df.empty:
        print("\nAVISO: Nenhum dado após filtragem!")
        print("\nSugestões:")
        print("- Verifique os intervalos de ano/avaliação")
        print("- Confira os gêneros/tipos digitados")
        print("\nDistribuições originais:")
        print(f"- Anos: {df['releaseYear'].min()} a {df['releaseYear'].max()}")
        print(f"- Avaliações: {df['imdbAverageRating'].min():.1f} a {df['imdbAverageRating'].max():.1f}")
        print(f"- Tipos: {df['type'].unique().tolist()}")
        print("\nExemplo de gêneros:", df['genres'].str.split(',').explode().value_counts().head(10).to_dict())
        return
    
    
    metrics = {
        'total': len(filtered_df),
        'avg_rating': filtered_df['imdbAverageRating'].mean(),
        'total_votes': filtered_df['imdbNumVotes'].sum(),
        'avg_year': filtered_df['releaseYear'].mean()
    }
    
    print("\n=== RESULTADOS ===")
    print(f"Total de títulos: {metrics['total']:,}")
    print(f"Avaliação média: {metrics['avg_rating']:.2f}")
    print(f"Votos totais: {metrics['total_votes']:,.0f}")
    print(f"Ano médio: {int(metrics['avg_year'])}")
    
    
    generate_visualizations(filtered_df)

def main():
    print("=== ANÁLISE DE CATÁLOGO NETFLIX ===")
    
    
    DATA_PATH = 'C:/Users/mulin/OneDrive/Documentos/analysis-genre-netflix/data/processed/data_tratada.csv'  # Caminho relativo para GitHub
    OUTPUT_DIR = 'output'
    
    
    df = load_data(DATA_PATH)
    if df is None:
        return
    
    # Pré-processamento
    df = preprocess_data(df)
    
    # Filtros padrão 
    my_filters = {
        'years': (2000, 2023),      # Intervalo de anos
        'rating_range': (6.0, 10.0), # Avaliação mínima e máxima
        'type': 'movie',             # 'Todos' para incluir tudo
        'genres': ['Action', 'Adventure', 'Comedy']  # Lista vazia [] para todos
    }
    
    # Análise
    analyze_data(df, my_filters)

if __name__ == "__main__":
    main()