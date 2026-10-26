"""Strict filtering helpers for the MovieLens movie catalog."""

import pandas as pd


def filter_movies(
    movies: pd.DataFrame,
    mood=None,
    era=None,
    min_rating=0.0,
    preset=None,
    excluded_ids=None,
):
    """Apply every requested constraint without returning an unfiltered fallback."""
    filtered = movies.copy()

    if mood and mood not in {"All", "Surprise Me", "All / Any"}:
        filtered = filtered[
            filtered["genres"].fillna("").str.split("|").apply(
                lambda genres: mood.casefold() in {genre.casefold() for genre in genres}
            )
        ]

    if era and era not in {"Any", "Any Era"}:
        decade = {
            "70s": 1970,
            "80s": 1980,
            "90s": 1990,
            "00s": 2000,
            "10s": 2010,
            "20s": 2020,
        }.get(era)
        if decade is not None:
            filtered = filtered[
                (filtered["year"] >= decade) & (filtered["year"] < decade + 10)
            ]

    rating_threshold = min_rating / 2 if min_rating > 5 else min_rating
    if rating_threshold > 0:
        filtered = filtered[filtered["avg_rating"] >= rating_threshold]

    if preset == "under_90":
        if "runtime" not in filtered.columns:
            return filtered.iloc[0:0]
        runtime = pd.to_numeric(filtered["runtime"], errors="coerce")
        filtered = filtered[runtime.notna() & (runtime < 90)]
        filtered = filtered[
            (filtered["avg_rating"] >= 3.4) & (filtered["rating_count"] >= 10)
        ]
    elif preset == "hidden_gem":
        filtered = filtered[
            (filtered["avg_rating"] >= 3.5)
            & filtered["rating_count"].between(5, 60)
        ]
    elif preset == "date_night":
        filtered = filtered[
            filtered["genres"].fillna("").str.contains(
                "Romance|Comedy|Drama", case=False, regex=True
            )
            & (filtered["avg_rating"] >= 3.3)
        ]
    elif preset == "highly_rated":
        filtered = filtered[filtered["avg_rating"] >= 3.8]

    if excluded_ids:
        filtered = filtered[~filtered["movieId"].isin(excluded_ids)]

    return filtered
