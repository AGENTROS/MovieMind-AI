import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from data_loader import get_processed_data
from content_based import ContentBasedRecommender
from collaborative import CollaborativeRecommender
from hybrid import HybridRecommender

EVAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'evaluation_metrics.json')

def run_evaluation(sample_users=50, k=5, threshold=3.5):
    """
    Evaluate recommendation systems on held-out test data.
    - sample_users: number of active users to evaluate for fast benchmarking
    - k: top-k items recommended
    - threshold: minimum rating in test set to count as 'relevant'
    """
    print("Loading data for evaluation...")
    movies_df, ratings_df = get_processed_data()

    # Split ratings 80/20 into train and test
    train_ratings, test_ratings = train_test_split(ratings_df, test_size=0.2, random_state=42)

    # Initialize models on training data
    cb = ContentBasedRecommender(movies_df)
    cf = CollaborativeRecommender(movies_df, train_ratings)
    hybrid = HybridRecommender(cb, cf)

    # Select test users who have at least 10 ratings in test set
    test_user_counts = test_ratings.groupby('userId').size()
    eval_users = (
        test_user_counts[test_user_counts >= 10]
        .sort_values(ascending=False)
        .head(sample_users)
        .index.tolist()
    )

    print(f"Evaluating {len(eval_users)} users at K={k}...")

    cb_precisions, cb_recalls, cb_hits = [], [], []
    cf_precisions, cf_recalls, cf_hits = [], [], []
    hybrid_precisions, hybrid_recalls, hybrid_hits = [], [], []
    
    cf_errors = []
    evaluated_users = 0

    for uid in eval_users:
        user_test = test_ratings[test_ratings['userId'] == uid]
        user_train = train_ratings[train_ratings['userId'] == uid]
        
        # Ground truth relevant movies in test set
        relevant_test_movies = set(user_test[user_test['rating'] >= threshold]['movieId'])
        if not relevant_test_movies:
            continue
        evaluated_users += 1

        # Target user's favorite training movie for content-based seed
        fav_train_movie = user_train.sort_values(by='rating', ascending=False)
        seed_mid = fav_train_movie.iloc[0]['movieId'] if not fav_train_movie.empty else None

        # 1. Content-Based Recs
        if seed_mid:
            cb_recs = cb.recommend_by_movie_id(seed_mid, top_n=k)
            cb_mids = set(cb_recs['movieId']) if not cb_recs.empty else set()
        else:
            cb_mids = set()

        # 2. Collaborative Recs
        cf_recs = cf.recommend_for_user(uid, top_n=k)
        cf_mids = set(cf_recs['movieId']) if not cf_recs.empty else set()

        # 3. Hybrid Recs
        # Top from both
        hybrid_recs = hybrid.recommend(
            movie_id=seed_mid, user_id=uid, alpha=0.5, top_n=k
        )
        hybrid_mids = set(hybrid_recs['movieId']) if not hybrid_recs.empty else set()

        # Evaluate Hit, Precision, Recall
        def calc_metrics(recs, relevant):
            if not recs:
                return 0.0, 0.0, 0.0
            hits = len(recs & relevant)
            prec = hits / k
            rec = hits / len(relevant)
            hit = 1.0 if hits > 0 else 0.0
            return prec, rec, hit

        p_cb, r_cb, h_cb = calc_metrics(cb_mids, relevant_test_movies)
        p_cf, r_cf, h_cf = calc_metrics(cf_mids, relevant_test_movies)
        p_hy, r_hy, h_hy = calc_metrics(hybrid_mids, relevant_test_movies)

        cb_precisions.append(p_cb)
        cb_recalls.append(r_cb)
        cb_hits.append(h_cb)

        cf_precisions.append(p_cf)
        cf_recalls.append(r_cf)
        cf_hits.append(h_cf)

        hybrid_precisions.append(p_hy)
        hybrid_recalls.append(r_hy)
        hybrid_hits.append(h_hy)

        # Rating error calculation for CF
        if not cf_recs.empty and 'predicted_rating' in cf_recs.columns:
            pred_dict = dict(zip(cf_recs['movieId'], cf_recs['predicted_rating']))
            for _, test_row in user_test.iterrows():
                mid = test_row['movieId']
                if mid in pred_dict:
                    actual = test_row['rating']
                    pred = pred_dict[mid]
                    cf_errors.append((actual - pred) ** 2)

    rmse = float(np.sqrt(np.mean(cf_errors))) if cf_errors else None
    mae = float(np.mean(np.sqrt(cf_errors))) if cf_errors else None

    def mean_percentage(values):
        return round(float(np.mean(values)) * 100, 2) if values else 0.0

    results = {
        "evaluation_version": 3,
        "k": k,
        "sample_users_evaluated": evaluated_users,
        "content_based": {
            "precision": mean_percentage(cb_precisions),
            "recall": mean_percentage(cb_recalls),
            "hit_rate": mean_percentage(cb_hits),
            "algorithm": "TF-IDF + Cosine Similarity",
            "primary_strength": "Solves item cold start, domain specific similarity",
            "limitation": "Overspecialization, cannot recommend across different genres"
        },
        "collaborative": {
            "precision": mean_percentage(cf_precisions),
            "recall": mean_percentage(cf_recalls),
            "hit_rate": mean_percentage(cf_hits),
            "rmse": round(rmse, 3) if rmse is not None else None,
            "mae": round(mae, 3) if mae is not None else None,
            "algorithm": "User-Based Collaborative Filtering (Cosine Similarity)",
            "primary_strength": "Discovers cross-genre unexpected favorites, leverages community taste",
            "limitation": "Suffers from cold start problem on new users/items"
        },
        "hybrid": {
            "precision": mean_percentage(hybrid_precisions),
            "recall": mean_percentage(hybrid_recalls),
            "hit_rate": mean_percentage(hybrid_hits),
            "algorithm": "Weighted Linear Hybrid (Content + Collaborative)",
            "primary_strength": "Combines item metadata with collaborative user ratings",
            "limitation": "Higher computational overhead than single models"
        },
        "dataset_stats": {
            "total_movies": len(movies_df),
            "total_ratings": len(ratings_df),
            "total_users": ratings_df['userId'].nunique(),
            "rating_scale": "0.5 to 5.0",
            "matrix_sparsity": f"{round((1 - (len(ratings_df) / (len(movies_df) * ratings_df['userId'].nunique()))) * 100, 2)}%"
        }
    }

    os.makedirs(os.path.dirname(EVAL_FILE), exist_ok=True)
    with open(EVAL_FILE, 'w') as f:
        json.dump(results, f, indent=4)

    print("Evaluation completed and saved to", EVAL_FILE)
    return results

def get_cached_or_default_metrics():
    """Load cached metrics or run fast evaluation if not found."""
    if os.path.exists(EVAL_FILE):
        with open(EVAL_FILE, 'r') as f:
            cached = json.load(f)
        if cached.get("evaluation_version") == 3:
            return cached
    return run_evaluation(sample_users=30, k=5)

if __name__ == '__main__':
    res = run_evaluation(sample_users=40, k=5)
    print(json.dumps(res, indent=2))
