# retrieval/index_builder.py
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIR = os.path.join(BASE_DIR, "index")
os.makedirs(INDEX_DIR, exist_ok=True)

DOMAINS = {
    "news": {
        "csv": os.path.join(BASE_DIR, "data", "cleaned", "news_cleaned.csv"),
        "emb": os.path.join(BASE_DIR, "embeddings", "news_embeddings.npy"),
        "id2index": os.path.join(BASE_DIR, "embeddings", "news_id2index.npy"),
    },
    "movies": {
        "csv": os.path.join(BASE_DIR, "data", "cleaned", "movies_cleaned.csv"),
        "emb": os.path.join(BASE_DIR, "embeddings", "movies_embeddings.npy"),
        "id2index": os.path.join(BASE_DIR, "embeddings", "movies_id2index.npy"),
    },
    "products": {
        "csv": os.path.join(BASE_DIR, "data", "cleaned", "products_cleaned.csv"),
        "emb": os.path.join(BASE_DIR, "embeddings", "products_embeddings.npy"),
        "id2index": os.path.join(BASE_DIR, "embeddings", "products_id2index.npy"),
    },
}

def build_index(domain_name, paths):
    print(f"\n=== Building index for {domain_name.upper()} ===")

    for key, path in paths.items():
        if not os.path.exists(path):
            print(f"❌ Missing {key} file: {path}")
            return

    print("📥 Loading CSV and embeddings...")
    df = pd.read_csv(paths["csv"])
    embeddings = np.load(paths["emb"])
    id2index = np.load(paths["id2index"], allow_pickle=True).item()

    print("🔢 Normalizing embeddings...")
    normalized = normalize(embeddings)

    out_file = os.path.join(INDEX_DIR, f"{domain_name}_index.pkl")
    with open(out_file, "wb") as f:
        pickle.dump({
            "df": df,
            "embeddings": normalized,
            "id2index": id2index
        }, f)

    print(f"✅ Saved index at: {out_file}")

if __name__ == "__main__":
    for domain, paths in DOMAINS.items():
        build_index(domain, paths)
