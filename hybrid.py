import pandas as pd
import numpy as np

class HybridRecommender:
    def __init__(self, content_recommender, collaborative_recommender):
        self.cb = content_recommender
        self.cf = collaborative_recommender
        self.movie_info = self.cb.movies_df.set_index('movieId').to_dict('index')

    def recommend(self, movie_id=None, user_id=None, custom_ratings=None, alpha=0.5, top_n=10):
        """
        Hybrid recommendation engine blending Content-Based and Collaborative Filtering.
        - alpha: Weight given to Content-Based (0.0 = pure collaborative, 1.0 = pure content)
        - movie_id: Seed movie for content similarity (e.g. user selected favorite movie)
        - user_id: Existing MovieLens user ID
        - custom_ratings: Dict of {movieId: rating} for custom guest user
        """
        content_scores = {}
        collab_scores = {}
        alpha = float(np.clip(alpha, 0.0, 1.0))
        if top_n <= 0:
            return pd.DataFrame()

        # 1. Gather Content-Based Scores
        if movie_id is not None:
            cb_df = self.cb.recommend_by_movie_id(movie_id, top_n=50)
            if not cb_df.empty:
                for _, row in cb_df.iterrows():
                    # Cosine similarity is already in [0, 1]
                    content_scores[row['movieId']] = float(row.get('similarity_score', 0.0))

        # 2. Gather Collaborative Filtering Scores
        if user_id is not None:
            cf_df = self.cf.recommend_for_user(user_id, top_n=50)
            if not cf_df.empty:
                for _, row in cf_df.iterrows():
                    # Normalize predicted rating from [0.5, 5.0] to [0.0, 1.0]
                    raw_rating = float(row.get('predicted_rating', 3.0))
                    norm_score = max(0.0, min(1.0, (raw_rating - 0.5) / 4.5))
                    collab_scores[row['movieId']] = norm_score
        elif custom_ratings:
            cf_df = self.cf.recommend_for_custom_user(custom_ratings, top_n=50)
            if not cf_df.empty:
                for _, row in cf_df.iterrows():
                    raw_rating = float(row.get('predicted_rating', 3.0))
                    norm_score = max(0.0, min(1.0, (raw_rating - 0.5) / 4.5))
                    collab_scores[row['movieId']] = norm_score

        # Fallback scenarios:
        # If no CF signals available, pure CB
        if not collab_scores and content_scores:
            alpha = 1.0
        # If no CB seed movie provided, pure CF
        elif not content_scores and collab_scores:
            alpha = 0.0
        elif not content_scores and not collab_scores:
            # Fallback to popular high-rated movies
            popular = self.cb.movies_df.sort_values(by=['rating_count', 'avg_rating'], ascending=False).head(top_n)
            return popular

        all_candidates = set(content_scores.keys()) | set(collab_scores.keys())
        
        # Exclude seed movie if specified
        if movie_id in all_candidates:
            all_candidates.remove(movie_id)

        # Exclude movies custom user already rated
        if custom_ratings:
            for mid in custom_ratings:
                all_candidates.discard(mid)
        elif user_id in self.cf.user_to_idx:
            seen_movies = self.cf.user_item_matrix.loc[user_id].dropna().index
            all_candidates.difference_update(seen_movies)

        hybrid_results = []
        for mid in all_candidates:
            c_score = content_scores.get(mid, 0.0)
            cf_score = collab_scores.get(mid, 0.0)
            
            # Weighted hybrid score
            h_score = (alpha * c_score) + ((1.0 - alpha) * cf_score)
            
            if mid in self.movie_info:
                info = self.movie_info[mid].copy()
                info['movieId'] = mid
                info['hybrid_score'] = round(float(h_score), 4)
                info['content_score'] = round(float(c_score), 4)
                info['collab_score'] = round(float(cf_score), 4)
                info['match_percentage'] = round(float(h_score) * 100, 1)
                hybrid_results.append(info)

        sorted_recs = sorted(hybrid_results, key=lambda x: x['hybrid_score'], reverse=True)[:top_n]
        return pd.DataFrame(sorted_recs)

if __name__ == '__main__':
    from content_based import ContentBasedRecommender
    from collaborative import CollaborativeRecommender
    
    cb = ContentBasedRecommender()
    cf = CollaborativeRecommender()
    hybrid = HybridRecommender(cb, cf)
    
    print("Testing Hybrid Recommender for movie Toy Story (1) and user 1...")
    recs = hybrid.recommend(movie_id=1, user_id=1, alpha=0.5, top_n=5)
    print(recs[['title', 'genres_str', 'hybrid_score', 'content_score', 'collab_score']])
