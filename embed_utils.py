# scripts/embed_utils.py
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from typing import List

def load_model(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    return model

def embed_in_chunks(model, texts: List[str], batch_size=64, chunk_size=2000):
    """
    Embeds texts by processing chunk-by-chunk.
    Returns a list of numpy arrays (one per chunk).
    """
    parts = []
    n = len(texts)
    i = 0
    while i < n:
        end = min(n, i + chunk_size)
        # within chunk, encode in batches
        chunk_texts = texts[i:end]
        emb = model.encode(chunk_texts, batch_size=batch_size, show_progress_bar=False)
        parts.append(emb)
        print(f"  - Embedded items {i}..{end-1}  (shape {emb.shape})")
        i = end
    return parts

def save_parts_to_single(parts, out_file):
    """
    Concatenate parts (list of arrays) and save as single .npy file.
    """
    if len(parts) == 0:
        raise ValueError("No parts to save.")
    embeddings = np.concatenate(parts, axis=0)
    np.save(out_file, embeddings)
    print(f"Saved final embeddings: {out_file}  (shape: {embeddings.shape})")
    return embeddings.shape

# --- Runtime embedding helper for live queries ---

_model = None

def embed_query(text: str):
    global _model
    if _model is None:
        _model = load_model()
    emb = _model.encode([text])
    return emb
