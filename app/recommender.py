from sentence_transformers import SentenceTransformer
from retrieval.retriever import Retriever
from context.context_manager import ContextManager
from context.scoring import score_content
import pandas as pd
import random



class SmartRecommender:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.context = ContextManager()

        self.retrievers = {
            "movies": Retriever("movies"),
            "news": Retriever("news"),
            "products": Retriever("products")
        }

        self.data = {
            "movies": pd.read_csv("data/cleaned/movies_cleaned.csv"),
            "news": pd.read_csv("data/cleaned/news_cleaned.csv"),
            "products": pd.read_csv("data/cleaned/products_cleaned.csv")
        }

    def recommend(self, query, domain="movies"):
        ctx = self.context.get_live_context()
        emb = self.model.encode(query)

        results = self.retrievers[domain].search(emb, top_k=15)

        final = []

        for item_id, base_score in results:
            row = self.data[domain][self.data[domain].item_id == item_id].iloc[0]

            item = {
                "item_id": int(item_id),
                "title": row["title"],
                "category": domain,
                "domain": domain,
                "length": row.get("length", "medium"),
                "score": base_score
            }

            final_score = score_content(item, ctx)

            item["final_score"] = round(final_score, 3)
            item["context"] = ctx

            final.append(item)

        final.sort(key=lambda x: x["final_score"], reverse=True)
        return final[:10]

    def random_discovery(self, domain="movies"):
        df = self.data[domain].sample(10)
        results = []
        for _, row in df.iterrows():
            results.append({
                "title": row["title"],
                "final_score": round(random.uniform(0.8, 1.5), 2),
                "context": self.context.get_live_context()
                })
        return results
