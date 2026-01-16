from typing import List, Optional
from pydantic import BaseModel
import re


# --------------------------------------------------
# Intent Schema
# --------------------------------------------------
class Intent(BaseModel):
    rewritten_query: str
    domains: Optional[List[str]] = None
    intent_type: str = "search"
    mood: Optional[str] = None


# --------------------------------------------------
# Domain keyword map (lightweight + fast)
# --------------------------------------------------
DOMAIN_KEYWORDS = {
    "movies": [
        "movie", "film", "series", "show", "episode", "netflix",
        "amazon prime", "hotstar", "comedy", "thriller", "drama"
    ],
    "news": [
        "news", "headline", "breaking", "politics", "election",
        "economy", "finance", "technology", "sports"
    ],
    "products": [
        "buy", "price", "product", "laptop", "phone", "mobile",
        "amazon", "flipkart", "review", "best"
    ]
}

MOOD_KEYWORDS = {
    "happy": ["funny", "uplifting", "light", "feel good", "happy"],
    "sad": ["sad", "emotional", "heart touching"],
    "serious": ["serious", "informative", "deep"],
    "relaxed": ["chill", "relax", "easy"]
}


# --------------------------------------------------
# Intent Parser (Step I)
# --------------------------------------------------
def parse_intent(query: str) -> Intent:
    """
    Converts raw user query into a structured intent.
    This version is rule-based but LLM-ready.
    """

    q = query.lower().strip()

    # -------- Domain detection --------
    detected_domains = set()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in q:
                detected_domains.add(domain)
                break

    domains = list(detected_domains) if detected_domains else None

    # -------- Mood detection --------
    detected_mood = None
    for mood, keywords in MOOD_KEYWORDS.items():
        for kw in keywords:
            if kw in q:
                detected_mood = mood
                break
        if detected_mood:
            break

    # -------- Rewrite query (cleanup) --------
    rewritten = clean_query(q)

    return Intent(
        rewritten_query=rewritten,
        domains=domains,
        intent_type="recommendation" if detected_mood else "search",
        mood=detected_mood
    )


# --------------------------------------------------
# Helper: Query cleaning
# --------------------------------------------------
def clean_query(text: str) -> str:
    """
    Light query normalization before embedding
    """
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
