import requests
import threading
import time

class LocationDetector:
    def __init__(self):
        self.city = "Unknown"
        self._running = False
        self._thread = None

    def _loop(self):
        while self._running:
            try:
                res = requests.get("https://ipinfo.io/json", timeout=5).json()
                self.city = res.get("city", "Unknown")
            except:
                pass
            time.sleep(300)  # refresh every 5 min

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print("📍 City-level location detector started")

    def stop(self):
        self._running = False

    def detect_location(self):
        return self.city
