import os
import re
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def load_raw_data():
    """Load raw CSV files from data directory."""
    movies_path = os.path.join(DATA_DIR, 'movies.csv')
    ratings_path = os.path.join(DATA_DIR, 'ratings.csv')
    tags_path = os.path.join(DATA_DIR, 'tags.csv')
    links_path = os.path.join(DATA_DIR, 'links.csv')

    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    
    tags_df = pd.read_csv(tags_path) if os.path.exists(tags_path) else pd.DataFrame(columns=['userId', 'movieId', 'tag'])
    links_df = pd.read_csv(links_path) if os.path.exists(links_path) else pd.DataFrame(columns=['movieId', 'imdbId', 'tmdbId'])

    return movies_df, ratings_df, tags_df, links_df

def extract_year(title):
    """Extract release year from movie title e.g. Toy Story (1995) -> 1995."""
    match = re.search(r'\((\d{4})\)', title)
    return int(match.group(1)) if match else None

def clean_title(title):
    """Clean movie title by removing year and trailing punctuation."""
    cleaned = re.sub(r'\s*\(\d{4}\)', '', title).strip()
    return cleaned

def get_processed_data():
    """
    Process movies, ratings, tags and links into an enriched dataframe.
    Calculates average ratings, vote counts, formatted genres, and aggregated tags.
    """
    movies_df, ratings_df, tags_df, links_df = load_raw_data()

    # Extract year and clean title
    movies_df['year'] = movies_df['title'].apply(extract_year)
    movies_df['clean_title'] = movies_df['title'].apply(clean_title)

    # Process genres list
    movies_df['genres_list'] = movies_df['genres'].apply(
        lambda x: [g.strip() for g in x.split('|')] if isinstance(x, str) and x != '(no genres listed)' else ['Unknown']
    )
    movies_df['genres_str'] = movies_df['genres_list'].apply(lambda x: ", ".join(x))

    # Aggregate tags per movie
    if not tags_df.empty:
        tags_df['tag'] = tags_df['tag'].astype(str).str.lower().str.strip()
        movie_tags = tags_df.groupby('movieId')['tag'].apply(lambda tags: " ".join(set(tags))).reset_index()
        movies_df = pd.merge(movies_df, movie_tags, on='movieId', how='left')
        movies_df['tag'] = movies_df['tag'].fillna('')
    else:
        movies_df['tag'] = ''

    # Compute rating statistics per movie
    rating_stats = ratings_df.groupby('movieId').agg(
        avg_rating=('rating', 'mean'),
        rating_count=('rating', 'count')
    ).reset_index()
    rating_stats['avg_rating'] = rating_stats['avg_rating'].round(1)

    movies_df = pd.merge(movies_df, rating_stats, on='movieId', how='left')
    movies_df['avg_rating'] = movies_df['avg_rating'].fillna(0.0)
    movies_df['rating_count'] = movies_df['rating_count'].fillna(0).astype(int)

    # Merge links for TMDB integration
    if not links_df.empty:
        movies_df = pd.merge(movies_df, links_df[['movieId', 'tmdbId', 'imdbId']], on='movieId', how='left')
        movies_df['tmdbId'] = movies_df['tmdbId'].fillna(0).astype(int)

    # Combined content metadata for TF-IDF
    movies_df['content_soup'] = (
        movies_df['genres'].str.replace('|', ' ', regex=False).str.lower() + " " +
        movies_df['tag'] + " " +
        movies_df['clean_title'].str.lower()
    ).str.strip()

    return movies_df, ratings_df

if __name__ == '__main__':
    movies, ratings = get_processed_data()
    print("Movies processed:", len(movies))
    print("Ratings processed:", len(ratings))
    print(movies[['movieId', 'title', 'clean_title', 'year', 'avg_rating', 'rating_count', 'tmdbId']].head())
