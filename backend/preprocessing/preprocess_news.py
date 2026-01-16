import json
from pathlib import Path
import pandas as pd

def load_news_dataset():

    file_path = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project/data/news/news_data.csv"

    # Try common delimiters safely
    delimiters = [",", ";", "\t"]
    for delim in delimiters:
        try:
            df = pd.read_csv(
                file_path,
                sep=delim,
                engine="python",
                on_bad_lines="skip"   # skip malformed lines safely
            )

            # If df has at least 2 columns it worked
            if df.shape[1] >= 2:
                print(f"✓ Loaded news dataset using delimiter '{delim}'")
                break
        except Exception:
            continue

    # Normalize
    df.columns = df.columns.str.lower()

    # Fix missing columns
    if "title" not in df.columns:
        df["title"] = df.iloc[:, 0]

    if "content" not in df.columns:
        # assume column 2 is full text
        df["content"] = df.iloc[:, 1]

    if "category" not in df.columns:
        df["category"] = "unknown"

    if "id" not in df.columns:
        df["id"] = range(1, len(df) + 1)

    return df


def preprocess_news(output_file="processed/news.jsonl"):
    df = load_news_dataset()

    Path("processed").mkdir(exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            canonical = f"{row['title']}. {row['content']}"
            item = {
                "id": str(row["id"]),
                "domain": "news",
                "title": row["title"],
                "canonical_text": canonical,
                "category": row.get("category", "unknown")
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✓ News preprocessing complete → {output_file}")


if __name__ == "__main__":
    preprocess_news()
