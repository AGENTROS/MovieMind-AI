import unittest

import pandas as pd

from content_based import ContentBasedRecommender
from collaborative import CollaborativeRecommender
from hybrid import HybridRecommender


class RecommenderTests(unittest.TestCase):
    def setUp(self):
        self.movies = pd.DataFrame(
            [
                {"movieId": 1, "title": "Space Story", "clean_title": "Space Story",
                 "content_soup": "space adventure galaxy", "genres_str": "Adventure"},
                {"movieId": 2, "title": "Space Journey", "clean_title": "Space Journey",
                 "content_soup": "space adventure stars", "genres_str": "Adventure"},
                {"movieId": 3, "title": "Quiet Garden", "clean_title": "Quiet Garden",
                 "content_soup": "garden flowers calm", "genres_str": "Drama"},
            ],
            index=[4, 8, 12],
        )
        self.ratings = pd.DataFrame([
            {"userId": 1, "movieId": 1, "rating": 5.0},
            {"userId": 1, "movieId": 2, "rating": 4.0},
            {"userId": 2, "movieId": 1, "rating": 4.5},
            {"userId": 2, "movieId": 3, "rating": 3.5},
            {"userId": 3, "movieId": 2, "rating": 4.5},
            {"userId": 3, "movieId": 3, "rating": 2.0},
        ])

    def test_content_similarity_threshold_is_enforced(self):
        recommender = ContentBasedRecommender(self.movies)
        results = recommender.recommend_by_movie_id(
            1, top_n=10, min_similarity=0.99
        )
        self.assertTrue(results.empty)

    def test_content_recommender_handles_non_contiguous_input_index(self):
        recommender = ContentBasedRecommender(self.movies)
        results = recommender.recommend_by_movie_id(1, top_n=2)
        self.assertTrue(set(results["movieId"]).issubset({2, 3}))

    def test_collaborative_predictions_only_include_unseen_movies(self):
        recommender = CollaborativeRecommender(self.movies, self.ratings)
        results = recommender.recommend_for_user(1, top_n=3)
        self.assertNotIn(1, results.get("movieId", pd.Series(dtype=int)).tolist())

    def test_hybrid_recommendations_exclude_movies_rated_by_existing_user(self):
        content = ContentBasedRecommender(self.movies)
        collaborative = CollaborativeRecommender(self.movies, self.ratings)
        recommender = HybridRecommender(content, collaborative)

        results = recommender.recommend(movie_id=1, user_id=1, top_n=3)

        self.assertTrue(set(results.get("movieId", [])) <= {3})


if __name__ == "__main__":
    unittest.main()
