import unittest

import pandas as pd

from movie_filters import filter_movies


class MovieFilterTests(unittest.TestCase):
    def setUp(self):
        self.movies = pd.DataFrame([
            {
                "movieId": 1, "genres": "Comedy|Drama", "year": 1995,
                "avg_rating": 4.0, "rating_count": 20, "runtime": 89,
            },
            {
                "movieId": 2, "genres": "Comedy", "year": 1995,
                "avg_rating": 4.5, "rating_count": 20, "runtime": 90,
            },
            {
                "movieId": 3, "genres": "Horror", "year": 2005,
                "avg_rating": 4.8, "rating_count": 20, "runtime": 80,
            },
            {
                "movieId": 4, "genres": "Comedy", "year": 1996,
                "avg_rating": 4.0, "rating_count": 20, "runtime": None,
            },
        ])

    def test_under_90_is_strict_and_drops_unknown_runtime(self):
        result = filter_movies(self.movies, preset="under_90")
        self.assertEqual(result["movieId"].tolist(), [1, 3])

    def test_empty_filter_does_not_return_original_catalog(self):
        result = filter_movies(self.movies, mood="Western")
        self.assertTrue(result.empty)

    def test_genre_era_rating_and_preset_filters_are_combined(self):
        result = filter_movies(
            self.movies, mood="Comedy", era="90s", min_rating=8.0,
            preset="under_90",
        )
        self.assertEqual(result["movieId"].tolist(), [1])

    def test_under_90_without_runtime_metadata_returns_no_candidates(self):
        result = filter_movies(
            self.movies.drop(columns=["runtime"]), preset="under_90"
        )
        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
