EMOTION_DOMAIN_MAP = {
    "happy": 1.4,
    "sad": 1.2,
    "angry": 1.3,
    "neutral": 1.0,
    "surprise": 1.5
}

def get_emotion_multiplier(emotion, domain):
    return EMOTION_DOMAIN_MAP.get(emotion.lower(), 1.0)
