import json
from pathlib import Path
import pandas as pd

def load_amazon_dataset(max_rows=10000):
    """
    Loads Amazon Review Polarity dataset (train.csv).
    We sample 10k items to keep embeddings fast.
    """
    file_path = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project/data/e_commerce_data/train.csv"
    
    df = pd.read_csv(
        file_path,
        header=None,
        names=["polarity", "title", "content"]
    )
    
    # Sample for speed
    df = df.sample(n=max_rows, random_state=42)
    
    df["id"] = range(1, len(df) + 1)
    df["category"] = df["polarity"].map({1: "positive", 2: "negative"})
    
    return df


def preprocess_products(output_file="processed/products.jsonl"):
    df = load_amazon_dataset()

    Path("processed").mkdir(exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            canonical = f"{row['title']}. {row['content']}"

            item = {
                "id": str(row["id"]),
                "domain": "products",
                "title": row["title"],
                "canonical_text": canonical,
                "category": row["category"]
            }
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✓ Products preprocessing complete → {output_file}")


if __name__ == "__main__":
    preprocess_products()
