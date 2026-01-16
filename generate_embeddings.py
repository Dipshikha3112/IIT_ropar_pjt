# scripts/generate_embeddings.py
import os
import pandas as pd
import numpy as np
from embed_utils import load_model, embed_in_chunks, save_parts_to_single

DATA_DIR = "data/cleaned"
EMB_DIR = "embeddings"
os.makedirs(EMB_DIR, exist_ok=True)

# Configuration tuned for a 2-core CPU
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BATCH_SIZE = 64        # batch encode size
CHUNK_SIZE = 2000      # number of items embedded per chunk (keeps memory low)

DATASETS = {
    "news": "news_cleaned.csv",
    "movies": "movies_cleaned.csv",
    "products": "amazon_cleaned.csv"
}

def process_domain(domain):
    print(f"\n=== Embedding domain: {domain} ===")
    path = os.path.join(DATA_DIR, DATASETS[domain])
    if not os.path.exists(path):
        print(f"  ERROR: cleaned file not found: {path}")
        return

    df = pd.read_csv(path)
    if "canonical_text" not in df.columns:
        raise ValueError(f"{path} missing canonical_text column.")

    texts = df["canonical_text"].astype(str).tolist()
    ids = df["item_id"].astype(int).tolist()

    model = load_model(MODEL_NAME)

    # embed in chunks (this is resumable in parts)
    print(f"Embedding {len(texts)} items (chunk_size={CHUNK_SIZE}, batch_size={BATCH_SIZE}) ...")
    parts = embed_in_chunks(model, texts, batch_size=BATCH_SIZE, chunk_size=CHUNK_SIZE)

    # save final embeddings
    out_emb = os.path.join(EMB_DIR, f"{domain}_embeddings.npy")
    save_parts_to_single(parts, out_emb)

    # save id->index mapping as CSV
    idx_df = pd.DataFrame({"item_id": ids, "index": list(range(len(ids)))})
    idx_file = os.path.join(EMB_DIR, f"{domain}_index.csv")
    idx_df.to_csv(idx_file, index=False)
    print(f"Saved id->index mapping: {idx_file}")

def main():
    # iterate domains in order news, movies, products
    for d in ["news", "movies", "products"]:
        process_domain(d)

if __name__ == "__main__":
    main()
