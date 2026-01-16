import os
import numpy as np
import pandas as pd

BASE = "C:/Users/DIPSHIKHA/Pictures/IIT_ropar_project"

DOMAINS = {
    "news": f"{BASE}/data/cleaned/news_cleaned.csv",
    "movies": f"{BASE}/data/cleaned/movies_cleaned.csv",
    "products": f"{BASE}/data/cleaned/amazon_cleaned.csv",
}

OUT_DIR = f"{BASE}/embeddings"
os.makedirs(OUT_DIR, exist_ok=True)

def rebuild(domain, csv_path):
    print(f"\n🔄 Rebuilding id2index for {domain.upper()}...")

    if not os.path.exists(csv_path):
        print(f"❌ CSV not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    if "item_id" not in df.columns:
        print(f"❌ CSV missing item_id column: {csv_path}")
        return

    id2index = {item_id: idx for idx, item_id in enumerate(df["item_id"].tolist())}

    out_file = f"{OUT_DIR}/{domain}_id2index.npy"
    np.save(out_file, id2index)

    print(f"✅ Saved: {out_file}")


if __name__ == "__main__":
    for domain, csv_path in DOMAINS.items():
        rebuild(domain, csv_path)
