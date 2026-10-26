"""Clients and normalization helpers for live TMDB and OMDb movie data."""

import os
import re
from pathlib import Path

import requests


def _read_env_value(name):
    value = os.environ.get(name)
    if value:
        return value

    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return ""

    for line in env_path.read_text(encoding="utf-8").splitlines():
        key, separator, candidate = line.partition("=")
        if separator and key.strip() == name:
            return candidate.strip().strip("\"'")
    return ""


def save_env_value(name, value):
    """Update one .env variable while preserving all other local credentials."""
    env_path = Path(__file__).resolve().parent / ".env"
    lines = (
        env_path.read_text(encoding="utf-8").splitlines()
        if env_path.exists()
        else []
    )
    updated = []
    found = False
    for line in lines:
        key, separator, _ = line.partition("=")
        if separator and key.strip() == name:
            updated.append(f"{name}={value}")
            found = True
        else:
            updated.append(line)
    if not found:
        updated.append(f"{name}={value}")
    env_path.write_text("\n".join(updated) + "\n", encoding="utf-8")
    os.environ[name] = value


def parse_runtime(value):
    """Parse OMDb runtime text such as '136 min' into an integer number of minutes."""
    match = re.search(r"\b(\d+)\s*min\b", str(value or ""), re.IGNORECASE)
    return int(match.group(1)) if match else None


class OMDbClient:
    def __init__(self, api_key=None, session=None):
        self.api_key = api_key or _read_env_value("OMDB_API_KEY")
        self.session = session or requests.Session()
        self._cache = {}

    def set_api_key(self, api_key):
        self.api_key = api_key.strip() if api_key else ""

    def get_movie_details(self, imdb_id=None, title=None, year=None):
        """Fetch OMDb details by IMDb ID, falling back to a title/year lookup."""
        if not self.api_key:
            return None
        if not imdb_id and not title:
            return None
        cache_key = imdb_id or f"{title}:{year or ''}".casefold()
        if cache_key in self._cache:
            return self._cache[cache_key]

        params = {"apikey": self.api_key, "plot": "full"}
        if imdb_id:
            params["i"] = imdb_id
        else:
            params["t"] = title
            if year:
                params["y"] = int(year)

        response = self.session.get(
            "https://www.omdbapi.com/", params=params, timeout=5
        )
        response.raise_for_status()
        data = response.json()
        if data.get("Response") != "True":
            return None

        data["runtime_minutes"] = parse_runtime(data.get("Runtime"))
        self._cache[cache_key] = data
        return data


omdb_client = OMDbClient()
