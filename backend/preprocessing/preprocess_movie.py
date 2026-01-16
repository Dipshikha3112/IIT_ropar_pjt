import json
from pathlib import Path
import pandas as pd

def load_movies_dataset():
    """Loads MovieLens u.item file (pipe-delimited)."""
    file_path = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project/data/movie_data/u.item"

    df = pd.read_csv(
        file_path,
        sep="|",
        header=None,
        encoding="latin-1"
    )

    df.columns = [
        "movie_id",
        "title",
        "release_date",
        "video_release_date",
        "imdb_url",
        "genre_unknown", "genre_action", "genre_adventure", "genre_animation",
        "genre_children", "genre_comedy", "genre_crime", "genre_documentary",
        "genre_drama", "genre_fantasy", "genre_film_noir", "genre_horror",
        "genre_musical", "genre_mystery", "genre_romance", "genre_sci_fi",
        "genre_thriller", "genre_war", "genre_western"
    ]

    # convert binary genre columns → list of genres
    genre_cols = [col for col in df.columns if col.startswith("genre_")]

    df["genres"] = df[genre_cols].apply(
        lambda row: [g.replace("genre_", "") for g in genre_cols if row[g] == 1],
        axis=1
    )

    return df


def preprocess_movies(output_file="processed/movies.jsonl"):
    df = load_movies_dataset()

    Path("processed").mkdir(exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            canonical = f"{row['title']} — Genres: {', '.join(row['genres'])}"

            item = {
                "id": str(row["movie_id"]),
                "domain": "movies",
                "title": row["title"],
                "canonical_text": canonical,
                "genres": row["genres"]
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✓ Movies preprocessing complete → {output_file}")


if __name__ == "__main__":
    preprocess_movies()
