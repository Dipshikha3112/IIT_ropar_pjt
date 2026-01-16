CITY_GENRE_MAP = {
    "Mumbai": ["Bollywood", "Drama", "Romance"],
    "Bangalore": ["Tech", "Sci-Fi", "Startups"],
    "Delhi": ["Politics", "News", "Documentary"],
    "Chennai": ["Tamil", "Action", "Music"],
    "Hyderabad": ["Tollywood", "Thriller"],
    "Kolkata": ["Art", "Classic", "Drama"]
}

def get_location_multiplier(city, domain):
    if city in CITY_GENRE_MAP:
        return 1.3
    return 1.0
