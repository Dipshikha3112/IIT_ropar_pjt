import cv2
from deepface import DeepFace

class EmotionDetector:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)

    def detect(self):
        ret, frame = self.cam.read()
        if not ret:
            return "neutral"

        try:
            result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            return result[0]["dominant_emotion"]
        except:
            return "neutral"
