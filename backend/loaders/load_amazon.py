# scripts/load_amazon.py
import pandas as pd
import os

RAW_PATH = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project/data/e_commerce_data/train.csv"
OUT_PATH = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project/data/cleaned/amazon_cleaned.csv"
SAMPLE_N = 50000  # chosen option A

def load_amazon(sample_n=SAMPLE_N):
    print("=== load_amazon.py ===")
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Amazon train.csv not found: {RAW_PATH}")
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    # read with no header; common Amazon polarity format: label, title, content
    try:
        df = pd.read_csv(RAW_PATH, header=None, names=["label", "title", "content"], encoding="utf-8", engine="python", on_bad_lines="skip")
    except Exception:
        # fallback with latin-1 if utf-8 fails
        df = pd.read_csv(RAW_PATH, header=None, names=["label", "title", "content"], encoding="latin-1", engine="python", on_bad_lines="skip")

    print("Raw shape:", df.shape)

    # drop missing text rows
    df = df.dropna(subset=["title", "content"]).reset_index(drop=True)
    print("After dropping NA:", df.shape)

    # If dataset is huge, sample deterministically
    if len(df) > sample_n:
        df = df.sample(n=sample_n, random_state=42).reset_index(drop=True)
        print(f"Downsampled to {sample_n} rows for fast embedding/demo.")

    # Build canonical_text
    df["item_id"] = df.index.astype(int)
    df["canonical_text"] = df["title"].astype(str).str.strip() + ". " + df["content"].astype(str).str.replace("\n", " ").str.strip()
    df["category"] = df["label"].map({1: "negative", 2: "positive"}) if "label" in df.columns else "product"

    # Save
    df[["item_id", "title", "canonical_text", "category"]].to_csv(OUT_PATH, index=False, encoding="utf-8")
    print(f"Saved cleaned Amazon CSV → {OUT_PATH}")
    print("Sample:")
    print(df[["item_id", "title", "category"]].head(3))

if __name__ == "__main__":
    load_amazon()
