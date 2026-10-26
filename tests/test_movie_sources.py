import unittest
from unittest.mock import Mock

from movie_sources import OMDbClient, parse_runtime
from tmdb_api import TMDBClient


class MovieSourceTests(unittest.TestCase):
    def test_runtime_parser_requires_a_known_minutes_value(self):
        self.assertEqual(parse_runtime("136 min"), 136)
        self.assertEqual(parse_runtime("N/A"), None)
        self.assertEqual(parse_runtime(None), None)

    def test_omdb_uses_imdb_id_and_normalizes_runtime(self):
        response = Mock()
        response.json.return_value = {
            "Response": "True", "imdbID": "tt3896198", "Runtime": "136 min"
        }
        session = Mock()
        session.get.return_value = response
        client = OMDbClient(api_key="test-key", session=session)

        details = client.get_movie_details(imdb_id="tt3896198")

        self.assertEqual(details["runtime_minutes"], 136)
        self.assertEqual(session.get.call_args.kwargs["params"]["i"], "tt3896198")
        self.assertNotIn("t", session.get.call_args.kwargs["params"])

    def test_missing_omdb_key_does_not_make_a_request(self):
        session = Mock()
        client = OMDbClient(api_key="", session=session)
        self.assertIsNone(client.get_movie_details(imdb_id="tt3896198"))
        session.get.assert_not_called()

    def test_tmdb_discovery_passes_runtime_filter_and_bearer_token(self):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"results": [], "total_pages": 1}
        session = Mock()
        session.get.return_value = response
        client = TMDBClient(api_key="test-key", read_token="test-token")
        client.session = session

        client.discover_movies(filters={"with_runtime.lte": 89})

        request = session.get.call_args
        self.assertEqual(
            request.kwargs["headers"]["Authorization"], "Bearer test-token"
        )
        self.assertEqual(request.kwargs["params"]["with_runtime.lte"], 89)


if __name__ == "__main__":
    unittest.main()
