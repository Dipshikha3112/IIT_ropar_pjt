# retrieval/retriever.py

import os
import numpy as np
import pandas as pd


class Retriever:
    """
    Vector-based semantic retriever using cosine similarity.

    Loads:
    - Precomputed embeddings:  embeddings/{domain}_embeddings.npy
    - Metadata mapping:        embeddings/{domain}_index.csv

    Performs fast top-K similarity search.
    """

    def __init__(self, domain: str, index_dir="embeddings"):
        """
        domain: news | movies | products
        index_dir: folder containing embeddings and index CSVs
        """

        self.domain = domain
        self.index_dir = index_dir

        self.emb_file = os.path.join(index_dir, f"{domain}_embeddings.npy")
        self.map_file = os.path.join(index_dir, f"{domain}_index.csv")

        print(f"\n🔍 Loading vector index for domain: {domain}")

        if not os.path.exists(self.emb_file):
            raise FileNotFoundError(f"❌ Missing embeddings file: {self.emb_file}")

        if not os.path.exists(self.map_file):
            raise FileNotFoundError(f"❌ Missing index CSV file: {self.map_file}")

        # Load embeddings
        self.embeddings = np.load(self.emb_file).astype("float32")

        # Load metadata
        self.id_map = pd.read_csv(self.map_file)

        if "item_id" not in self.id_map.columns:
            raise ValueError("❌ index CSV must contain column: item_id")

        print(f"✔ Loaded {len(self.embeddings)} vectors")
        print(f"✔ Loaded {len(self.id_map)} metadata rows")

        # Normalize embeddings once (for cosine similarity)
        self.embeddings = self._normalize(self.embeddings)

    # --------------------------------------------------
    # Normalize vectors
    # --------------------------------------------------
    def _normalize(self, vectors: np.ndarray):
        norms = np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-10
        return vectors / norms

    # --------------------------------------------------
    # Search
    # --------------------------------------------------
    def search(self, query_embedding: np.ndarray, top_k=10):
        """
        Perform cosine similarity search

        query_embedding: 1D numpy array
        Returns: list of (item_id, score)
        """

        if query_embedding.ndim != 1:
            raise ValueError("query_embedding must be a 1D vector")

        # Normalize query
        query_embedding = query_embedding.astype("float32")
        query_embedding = query_embedding / (np.linalg.norm(query_embedding) + 1e-10)

        # Compute cosine similarity
        scores = np.dot(self.embeddings, query_embedding)

        # Top-K fast selection
        top_k = min(top_k, len(scores))
        top_indices = np.argpartition(-scores, top_k)[:top_k]
        top_indices = top_indices[np.argsort(-scores[top_indices])]

        results = []
        for idx in top_indices:
            item_id = int(self.id_map.iloc[idx]["item_id"])
            score = float(scores[idx])
            results.append((item_id, score))

        return results

    # --------------------------------------------------
    # Get full metadata for an item
    # --------------------------------------------------
    def get_item(self, item_id: int):
        row = self.id_map[self.id_map["item_id"] == item_id]
        if row.empty:
            return None
        return row.iloc[0].to_dict()

    # --------------------------------------------------
    # Health check
    # --------------------------------------------------
    def info(self):
        return {
            "domain": self.domain,
            "num_items": len(self.embeddings),
            "embedding_dim": self.embeddings.shape[1]
        }


# --------------------------------------------------
# Standalone test
# --------------------------------------------------
if __name__ == "__main__":
    print("\n🧪 Testing Retriever...\n")

    retriever = Retriever("movies")

    dummy_query = np.random.rand(retriever.embeddings.shape[1]).astype("float32")
    results = retriever.search(dummy_query, top_k=5)

    print("\nTop results:")
    for item_id, score in results:
        item = retriever.get_item(item_id)
        print(f"{item_id} | score={score:.4f} | title={item.get('title','N/A')}")
