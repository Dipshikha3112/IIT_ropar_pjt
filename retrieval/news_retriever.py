import numpy as np
import pandas as pd
import pickle

class NewsRetriever:
    def __init__(self,
                 index_path="index/news_index.pkl",
                 meta_path="embeddings/news_index.csv"):
        
        with open(index_path, "rb") as f:
            self.index = pickle.load(f)

        self.meta = pd.read_csv(meta_path)

    def search(self, query_embedding, top_k=5):
        D, I = self.index.search(query_embedding, top_k)

        results = []
        for idx in I[0]:
            row = self.meta.iloc[idx]
            results.append({
                "title": row["title"],
                "category": row.get("category", "general"),
                "source": row.get("source", "unknown")
            })

        return results
