#!/usr/bin/env python3
import json
import csv
from pathlib import Path

SIMPLE_FIELDS = [
    "id",
    "imdb_id",
    "original_title",
    "adult",
    "backdrop_path",
    "budget",
    "homepage",
    "original_language",
    "overview",
    "popularity",
    "poster_path",
    "release_date",
    "revenue",
    "runtime",
    "status",
    "tagline",
    "title",
    "video",
    "vote_average",
    "vote_count",
]


def flatten_movie(movie: dict) -> dict:
    flat = {field: movie.get(field, "") for field in SIMPLE_FIELDS}

    collection = movie.get("belongs_to_collection")
    flat["collection_id"] = collection.get("id", "") if collection else ""
    flat["collection_name"] = collection.get("name", "") if collection else ""

    flat["origin_country"] = "|".join(movie.get("origin_country", []))
    flat["genres"] = "|".join(g["name"] for g in movie.get("genres", []))
    flat["genre_ids"] = "|".join(str(g["id"]) for g in movie.get("genres", []))
    flat["production_companies"] = "|".join(
        c["name"] for c in movie.get("production_companies", [])
    )
    flat["production_countries"] = "|".join(
        c["name"] for c in movie.get("production_countries", [])
    )
    flat["spoken_languages"] = "|".join(
        lang.get("english_name", lang.get("name", ""))
        for lang in movie.get("spoken_languages", [])
    )
    flat["keywords"] = "|".join(kw["name"] for kw in movie.get("keywords", []))

    return flat


def main():
    input_path = Path(__file__).parent / "movies.json"
    output_path = Path(__file__).parent / "movies.csv"

    with open(input_path, "r", encoding="utf-8") as f:
        movies = json.load(f)

    movies = [m for m in movies if m.get("original_language") == "en" and m.get("budget") != 0 and m.get("vote_count") != 0]

    if not movies:
        print("No movies found in JSON file")
        return

    flat_movies = [flatten_movie(m) for m in movies]
    fieldnames = list(flat_movies[0].keys())

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_movies)

    print(f"Converted {len(movies)} movies to {output_path}")


if __name__ == "__main__":
    main()
