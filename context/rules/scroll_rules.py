"""
scroll_rules.py

Maps scrolling behavior → content length preference
"""

BASE = 1.0

SCROLL_RULES = {
    "fast_scroller": {
        "short": 1.6,
        "medium": 1.2,
        "long": 0.6
    },
    "slow_scroller": {
        "short": 0.7,
        "medium": 1.2,
        "long": 1.6
    },
    "normal": {
        "short": 1.0,
        "medium": 1.0,
        "long": 1.0
    }
}

def get_scroll_multiplier(scroll_type: str, content_length: str) -> float:
    scroll_type = scroll_type.lower()
    content_length = content_length.lower()
    rules = SCROLL_RULES.get(scroll_type, {})
    return rules.get(content_length, BASE)


# Demo
if __name__ == "__main__":
    print("Scroll Rules Demo")
    while True:
        st = input("Scroll type (fast_scroller/slow_scroller/normal, q to quit): ")
        if st in ["q", "quit", "exit"]:
            break
        cl = input("Content length (short/medium/long): ")
        m = get_scroll_multiplier(st, cl)
        print("Multiplier:", m)
