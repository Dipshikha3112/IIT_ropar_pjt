from context.detectors.emotion_detector import EmotionDetector
from context.detectors.time_detector import TimeDetector
from context.detectors.location_detector import LocationDetector
from context.detectors.scroll_detector import ScrollDetector
from context.detectors.feedback_detector import FeedbackDetector


class ContextManager:
    def __init__(self):
        self.emotion = EmotionDetector()
        self.time = TimeDetector()
        self.location = LocationDetector()
        self.scroll = ScrollDetector()
        self.feedback = FeedbackDetector()

        # Start background detectors
        self.location.start()
        self.scroll.start()
        self.feedback.start()

    def get_live_context(self):
        return {
            "emotion": self.emotion.detect(),
            "time_context": self.time.get_time_context(),
            "location": self.location.detect_location(),
            "scroll_type": self.scroll.detect_scroll(),
            "feedback": self.feedback.get_feedback()
        }
