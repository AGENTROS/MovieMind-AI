import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from data_loader import get_processed_data

class CollaborativeRecommender:
    def __init__(self, movies_df=None, ratings_df=None):
        if movies_df is None or ratings_df is None:
            self.movies_df, self.ratings_df = get_processed_data()
        else:
            self.movies_df = movies_df.copy()
            self.ratings_df = ratings_df.copy()

        self._build_matrix()

    def _build_matrix(self):
        """Construct user-item rating matrix and user index maps."""
        # Pivot ratings table: rows=userId, cols=movieId
        self.user_item_matrix = self.ratings_df.pivot(
            index='userId', columns='movieId', values='rating'
        )
        
        # User mean ratings for mean-centering (handling user rating bias)
        self.user_means = self.user_item_matrix.mean(axis=1)
        
        # Mean-centered rating matrix (NaN filled with 0)
        self.matrix_centered = self.user_item_matrix.sub(self.user_means, axis=0).fillna(0)
        
        # Precompute user-user cosine similarity matrix
        self.user_sim_matrix = cosine_similarity(self.matrix_centered)
        self.user_ids = list(self.user_item_matrix.index)
        self.user_to_idx = {uid: i for i, uid in enumerate(self.user_ids)}
        self.movie_info = self.movies_df.set_index('movieId').to_dict('index')

    def recommend_for_user(self, user_id, top_n=10, k_neighbors=25):
        """
        User-based collaborative filtering for an existing dataset user.
        Predicts ratings for movies the user has not seen yet.
        """
        if user_id not in self.user_to_idx:
            return pd.DataFrame()

        u_idx = self.user_to_idx[user_id]
        user_mean = self.user_means.loc[user_id]
        
        # User's rated movie set
        user_ratings = self.user_item_matrix.loc[user_id]
        seen_movies = set(user_ratings.dropna().index)

        # Similarities with other users
        sim_scores = self.user_sim_matrix[u_idx].copy()
        sim_scores[u_idx] = -1.0 # Don't compare with self

        # Top-K neighbors with positive similarity
        neighbor_indices = np.argsort(-sim_scores)[:k_neighbors]
        valid_neighbors = [idx for idx in neighbor_indices if sim_scores[idx] > 0]

        if not valid_neighbors:
            return pd.DataFrame()

        neighbor_sims = sim_scores[valid_neighbors]
        neighbor_ratings = self.user_item_matrix.iloc[valid_neighbors]
        neighbor_means = self.user_means.iloc[valid_neighbors]

        # Candidates are movies seen by neighbors but unseen by target user
        candidate_movies = [m for m in neighbor_ratings.columns if m not in seen_movies]
        
        pred_scores = {}
        for m in candidate_movies:
            ratings_col = neighbor_ratings[m]
            rated_mask = ratings_col.notna()
            if rated_mask.sum() < 2: # Require at least 2 neighbors to have rated it
                continue
            
            sims = neighbor_sims[rated_mask]
            diffs = ratings_col[rated_mask] - neighbor_means[rated_mask]
            
            sim_sum = np.sum(np.abs(sims))
            if sim_sum > 0:
                pred = user_mean + (np.sum(sims * diffs) / sim_sum)
                pred = np.clip(pred, 0.5, 5.0)
                pred_scores[m] = round(float(pred), 2)

        if not pred_scores:
            return pd.DataFrame()

        # Sort candidate movies by predicted rating
        sorted_mids = sorted(pred_scores.keys(), key=lambda x: pred_scores[x], reverse=True)[:top_n]
        
        results = []
        for mid in sorted_mids:
            if mid in self.movie_info:
                info = self.movie_info[mid].copy()
                info['movieId'] = mid
                info['predicted_rating'] = pred_scores[mid]
                results.append(info)

        return pd.DataFrame(results)

    def recommend_for_custom_user(self, custom_ratings, top_n=10, k_neighbors=25):
        """
        Collaborative filtering for a real-time guest/custom user who rates movies in the UI.
        custom_ratings: dict of {movieId: rating (1-5)}
        """
        if not custom_ratings:
            return pd.DataFrame()

        # Build guest user vector aligned with matrix columns
        all_movie_ids = self.user_item_matrix.columns
        guest_series = pd.Series(index=all_movie_ids, dtype=float)
        
        for mid, r in custom_ratings.items():
            if mid in guest_series.index:
                guest_series[mid] = float(r)

        rated_mids = set(custom_ratings.keys())
        guest_mean = guest_series.dropna().mean()
        if pd.isna(guest_mean):
            guest_mean = 3.5

        guest_centered = (guest_series - guest_mean).fillna(0).values.reshape(1, -1)
        
        # Calculate similarity with all existing users
        sim_scores = cosine_similarity(guest_centered, self.matrix_centered.values).flatten()

        neighbor_indices = np.argsort(-sim_scores)[:k_neighbors]
        valid_neighbors = [idx for idx in neighbor_indices if sim_scores[idx] > 0]

        if not valid_neighbors:
            return pd.DataFrame()

        neighbor_sims = sim_scores[valid_neighbors]
        neighbor_ratings = self.user_item_matrix.iloc[valid_neighbors]
        neighbor_means = self.user_means.iloc[valid_neighbors]

        candidate_movies = [m for m in neighbor_ratings.columns if m not in rated_mids]
        
        pred_scores = {}
        for m in candidate_movies:
            ratings_col = neighbor_ratings[m]
            rated_mask = ratings_col.notna()
            if rated_mask.sum() < 2:
                continue
            
            sims = neighbor_sims[rated_mask]
            diffs = ratings_col[rated_mask] - neighbor_means[rated_mask]
            
            sim_sum = np.sum(np.abs(sims))
            if sim_sum > 0:
                pred = guest_mean + (np.sum(sims * diffs) / sim_sum)
                pred = np.clip(pred, 0.5, 5.0)
                pred_scores[m] = round(float(pred), 2)

        sorted_mids = sorted(pred_scores.keys(), key=lambda x: pred_scores[x], reverse=True)[:top_n]
        
        results = []
        for mid in sorted_mids:
            if mid in self.movie_info:
                info = self.movie_info[mid].copy()
                info['movieId'] = mid
                info['predicted_rating'] = pred_scores[mid]
                results.append(info)

        return pd.DataFrame(results)

if __name__ == '__main__':
    cf = CollaborativeRecommender()
    print("Testing Collaborative Filtering for User 1...")
    recs = cf.recommend_for_user(1, top_n=5)
    print(recs[['title', 'genres_str', 'predicted_rating']])
    
    print("\nTesting Custom User with ratings...")
    # Assume custom user rated Toy Story (1) as 5.0 and Jumanji (2) as 4.0
    custom_recs = cf.recommend_for_custom_user({1: 5.0, 2: 4.0}, top_n=5)
    print(custom_recs[['title', 'genres_str', 'predicted_rating']])
