import random
import threading
import time

class FeedbackDetector:
    """
    Simulated real-time feedback detector.
    Returns feedback score (0-1) from user interactions.
    """
    def __init__(self, update_interval=20):
        self.feedback_score = 0.5
        self.update_interval = update_interval
        self._running = False
        self._thread = None

    def _update_loop(self):
        while self._running:
            # Simulate random feedback score
            self.feedback_score = round(random.uniform(0.3, 1.0), 2)
            time.sleep(self.update_interval)

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._update_loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def get_feedback(self) -> float:
        return self.feedback_score

# Example
if __name__ == "__main__":
    fd = FeedbackDetector()
    fd.start()
    try:
        while True:
            print("Feedback score:", fd.get_feedback())
            time.sleep(5)
    except KeyboardInterrupt:
        fd.stop()
