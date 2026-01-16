# retrieval/movies_retriever.py
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from retrieval.retriever import Retriever

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MoviesSearch:
    def __init__(self, top_k=5):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.retriever = Retriever("movies", index_dir=os.path.join(BASE_DIR, "embeddings"))
        self.meta = pd.read_csv(os.path.join(BASE_DIR, "data", "cleaned", "movies_cleaned.csv"))
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
    ms = MoviesSearch()
    query_text = "action thriller movies"
    results = ms.query(query_text)
    for r in results:
        print(r)
