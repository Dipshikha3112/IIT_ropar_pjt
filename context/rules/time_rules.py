def get_time_multiplier(time_of_day, domain):
    if time_of_day == "morning" and domain == "news":
        return 1.4
    if time_of_day == "evening" and domain == "movies":
        return 1.5
    if time_of_day == "night" and domain == "movies":
        return 1.3
    return 1.0
