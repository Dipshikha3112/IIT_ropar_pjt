# retrieval/products_retriever.py
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from retrieval.retriever import Retriever

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ProductsSearch:
    def __init__(self, top_k=5):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.retriever = Retriever("products", index_dir=os.path.join(BASE_DIR, "embeddings"))
        self.meta = pd.read_csv(os.path.join(BASE_DIR, "data", "cleaned", "products_cleaned.csv"))
        self.top_k = top_k

    def query(self, text: str):
        emb = self.model.encode([text])[0]
        results = self.retriever.search(emb, top_k=self.top_k)

        output = []
        for item_id, score in results:
            row = self.meta[self.meta.item_id == item_id].iloc[0]
            output.append({
                "title": row.get("title", ""),
                "canonical_text": row.get("canonical_text", ""),
                "score": score,
                "item_id": item_id
            })
        return output

if __name__ == "__main__":
    ps = ProductsSearch()
    query_text = "wireless headphones under 3000"
    results = ps.query(query_text)
    for r in results:
        print(r)
