import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_loader import get_processed_data

class ContentBasedRecommender:
    def __init__(self, movies_df=None):
        if movies_df is None:
            self.movies_df, _ = get_processed_data()
        else:
            self.movies_df = movies_df.copy()
        self.movies_df = self.movies_df.reset_index(drop=True)
            
        self._build_model()

    def _build_model(self):
        """Fit TF-IDF Vectorizer and create index mappings."""
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=10000)
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies_df['content_soup'].fillna(''))
        
        # Mapping index <-> movieId and title <-> index
        self.indices = pd.Series(self.movies_df.index, index=self.movies_df['movieId']).drop_duplicates()
        self.title_indices = pd.Series(self.movies_df.index, index=self.movies_df['clean_title'].str.lower()).drop_duplicates()

    def search_movies(self, query, limit=10):
        """Search movies by title query."""
        if not query or len(query.strip()) == 0:
            return self.movies_df.head(limit)
        
        q = query.lower().strip()
        mask = self.movies_df['title'].str.lower().str.contains(q, regex=False) | \
               self.movies_df['clean_title'].str.lower().str.contains(q, regex=False)
        return self.movies_df[mask].head(limit)

    def recommend_by_movie_id(self, movie_id, top_n=10, min_similarity=0.05):
        """
        Recommend movies similar to the given movieId using TF-IDF and Cosine Similarity.
        """
        if top_n <= 0 or movie_id not in self.indices:
            return pd.DataFrame()

        idx = self.indices[movie_id]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]

        # Calculate cosine similarity with all movies
        target_vec = self.tfidf_matrix[idx]
        sim_scores = cosine_similarity(target_vec, self.tfidf_matrix).flatten()

        # Sort indices by similarity descending
        sim_indices = np.argsort(-sim_scores)

        # Exclude the query movie itself
        sim_indices = [i for i in sim_indices if i != idx]

        results = []
        for i in sim_indices:
            score = float(sim_scores[i])
            if score < min_similarity:
                break
            movie_row = self.movies_df.iloc[i].to_dict()
            movie_row['similarity_score'] = round(score, 4)
            movie_row['match_percentage'] = round(score * 100, 1)
            results.append(movie_row)
            if len(results) >= top_n:
                break

        return pd.DataFrame(results)

    def recommend_by_title(self, title, top_n=10):
        """Recommend movies by title string."""
        matches = self.search_movies(title, limit=1)
        if matches.empty:
            return pd.DataFrame()
        movie_id = matches.iloc[0]['movieId']
        return self.recommend_by_movie_id(movie_id, top_n=top_n)

if __name__ == '__main__':
    recommender = ContentBasedRecommender()
    print("Testing Content-Based Recommendation for 'Interstellar'...")
    matches = recommender.search_movies('Interstellar')
    if not matches.empty:
        mid = matches.iloc[0]['movieId']
        recs = recommender.recommend_by_movie_id(mid, top_n=5)
        print(recs[['title', 'genres_str', 'similarity_score', 'match_percentage']])
