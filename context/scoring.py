"""
scoring.py

Applies all contextual multipliers to a base content score.
"""

from context.rules.scroll_rules import get_scroll_multiplier
from context.rules.time_rules import get_time_multiplier
from context.rules.emotion_rules import get_emotion_multiplier
from context.rules.location_rules import get_location_multiplier

BASE_SCORE = 1.0

def score_content(item, context):
    """
    item: dict containing at least 'domain', 'length', 'category'
    context: dict containing current user context
        {
            'scroll_type': str,
            'time_context': str,
            'emotion': str,
            'location': str
        }
    Returns adjusted score (float)
    """

    domain = item.get("domain", "news")
    length = item.get("length", "medium")
    category = item.get("category", domain)  # fallback to domain

    # Start with base score
    score = item.get("score", BASE_SCORE)

    # Scroll multiplier
    scroll_mult = get_scroll_multiplier(context.get("scroll_type", "normal"), length)

    # Time multiplier
    time_mult = get_time_multiplier(context.get("time_context", "morning"), category)

    # Emotion multiplier
    emotion_mult = get_emotion_multiplier(context.get("emotion", "neutral"), domain)

    # Location multiplier
    location_mult = get_location_multiplier(context.get("location", "unknown"), domain)

    # Combine multipliers
    final_score = score * scroll_mult * time_mult * emotion_mult * location_mult

    return final_score
