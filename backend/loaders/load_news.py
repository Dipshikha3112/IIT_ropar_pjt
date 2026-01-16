import pandas as pd
import os

RAW_PATH = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project/data/news/news_data.csv"
OUT_PATH = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project/data/cleaned/news_cleaned.csv"


def load_news():
    print("=== load_news.py ===")
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Raw news file not found: {RAW_PATH}")

    # Try to detect delimiter; prefer tab for this dataset
    try:
        df = pd.read_csv(RAW_PATH, sep="\t", engine="python", encoding="utf-8", on_bad_lines="skip")
        print("Loaded with sep='\\t'")
    except Exception:
        # fallback
        df = pd.read_csv(RAW_PATH, engine="python", encoding="utf-8", on_bad_lines="skip")
        print("Loaded with python engine default sep (fallback)")

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Fix common variations
    if "title" not in df.columns and "headline" in df.columns:
        df.rename(columns={"headline": "title"}, inplace=True)

    # Many versions have single col with 'category\tfilename\ttitle\tcontent'
    if df.shape[1] == 1 and "category\tfilename\ttitle\tcontent" in df.columns:
        # split the single column by tab
        s = df.iloc[:, 0].astype(str).str.split("\t", expand=True)
        # if split produced >=4 cols, assign meaningful names
        if s.shape[1] >= 4:
            s = s.iloc[:, :4]
            s.columns = ["category", "filename", "title", "content"]
            df = s
        else:
            raise ValueError("Unexpected single-column format in news file.")

    # Ensure title and content columns exist
    if "title" not in df.columns or "content" not in df.columns:
        # try fallback mapping
        cols = df.columns.tolist()
        if len(cols) >= 2:
            df = df.rename(columns={cols[0]: "title", cols[1]: "content"})
        else:
            raise ValueError("Could not find title/content columns in news dataset.")

    # Drop blank content/title rows
    df = df.dropna(subset=["title", "content"])
    df = df.reset_index(drop=True)

    # assign item_id
    df["item_id"] = df.index.astype(int)

    # canonical text
    df["canonical_text"] = df["title"].astype(str).str.strip() + ". " + df["content"].astype(str).str.replace("\n", " ").str.strip()

    # ensure category column exists
    if "category" not in df.columns:
        df["category"] = "news"

    # Save cleaned CSV
    df[["item_id", "title", "canonical_text", "category"]].to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"Saved cleaned news CSV → {OUT_PATH}")
    print("Sample:")
    print(df[["item_id", "title", "category"]].head(3))

if __name__ == "__main__":
    load_news()
