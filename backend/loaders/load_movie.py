import pandas as pd
import os

RAW_ITEM = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project/data/movie_data/u.item"
RAW_GENRE = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project/data/movie_data/u.genre"  # optional
OUT_PATH = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project/data/cleaned/movies_cleaned.csv"

# Default genre names (if u.genre is missing)
DEFAULT_GENRES = [
    "unknown","Action","Adventure","Animation","Children's","Comedy","Crime","Documentary",
    "Drama","Fantasy","Film-Noir","Horror","Musical","Mystery","Romance","Sci-Fi","Thriller","War","Western"
]

def load_movies():
    print("=== load_movies.py ===")
    if not os.path.exists(RAW_ITEM):
        raise FileNotFoundError(f"u.item file not found: {RAW_ITEM}")
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    # Read u.item with pipe delimiter
    df = pd.read_csv(RAW_ITEM, sep="|", header=None, encoding="ISO-8859-1", engine="python", on_bad_lines="skip")
    print("Loaded u.item shape:", df.shape)

    # Try to build genre list from u.genre if present
    genre_names = None
    if os.path.exists(RAW_GENRE):
        genre_names = []
        with open(RAW_GENRE, "r", encoding="latin-1") as f:
            for line in f:
                if "|" in line:
                    name, idx = line.strip().split("|")
                    genre_names.append(name)
        if len(genre_names) < 1:
            genre_names = None

    if genre_names is None:
        genre_names = DEFAULT_GENRES

    # Build header list: movie_id, title, release_date, video_release, imdb_url, then genres
    cols = ["movie_id", "title", "release_date", "video_release_date", "imdb_url"] + genre_names
    # ensure df has at least len(cols) columns; if more, trim; if less, extend
    if df.shape[1] < len(cols):
        # pad columns with generic names for safety
        extra = len(cols) - df.shape[1]
        for i in range(extra):
            df[i + df.shape[1]] = ""  # create empty columns
    df = df.iloc[:, :len(cols)]
    df.columns = cols

    # Compose genres per movie by checking 0/1 flags (if flags numeric)
    genre_cols = genre_names
    def extract_genres(row):
        out = []
        for g in genre_cols:
            try:
                val = int(row[g])
            except Exception:
                # if not numeric, skip or infer
                val = 0
            if val == 1:
                out.append(g)
        return out

    df["genres"] = df.apply(extract_genres, axis=1)

    # canonical_text: title + genres
    df["canonical_text"] = df["title"].astype(str).str.strip() + " — Genres: " + df["genres"].apply(lambda g: ", ".join(g))

    df["item_id"] = df["movie_id"].astype(int)
    df["category"] = "movie"

    df[["item_id", "title", "canonical_text", "genres", "imdb_url"]].to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"Saved cleaned movies CSV → {OUT_PATH}")
    print("Sample:")
    print(df[["item_id", "title", "genres"]].head(3))

if __name__ == "__main__":
    load_movies()
