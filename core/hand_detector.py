"""
Hand Detector Module
Detects and tracks hand landmarks using MediaPipe
"""

import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import cv2
import numpy as np
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class HandLandmarks:
    """Container for hand landmark data"""
    landmarks: list  # 21 landmarks (x, y, z)
    handedness: str  # "Left" or "Right"
    confidence: float  # Detection confidence
    hand_id: int = 0


class HandDetector:
    """Detects hand landmarks in real-time"""

    def __init__(self, static_image_mode=False, max_num_hands=2,
                 min_detection_confidence=0.7, min_tracking_confidence=0.5):
        """
        Initialize hand detector

        Args:
            static_image_mode: Use static image mode
            max_num_hands: Maximum number of hands to detect
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def detect(self, frame):
        """
        Detect hands in frame

        Args:
            frame: Input image (BGR format)

        Returns:
            List of HandLandmarks objects
        """
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            hand_list = []
            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(
                    results.multi_hand_landmarks, results.multi_handedness
                ):
                    # Extract landmarks
                    landmarks = []
                    for landmark in hand_landmarks.landmark:
                        landmarks.append([landmark.x, landmark.y, landmark.z])

                    hand_data = HandLandmarks(
                        landmarks=np.array(landmarks),
                        handedness=handedness.classification[0].label,
                        confidence=handedness.classification[0].score,
                        hand_id=len(hand_list)
                    )
                    hand_list.append(hand_data)

            return hand_list
        except Exception as e:
            logger.error(f"Hand detection error: {e}")
            return []

    def draw_landmarks(self, frame, hands):
        """
        Draw hand landmarks on frame

        Args:
            frame: Input image
            hands: List of HandLandmarks

        Returns:
            Frame with drawn landmarks
        """
        try:
            # Convert landmarks back to MediaPipe format for drawing
            for hand in hands:
                hand_landmarks = landmark_pb2.NormalizedLandmarkList()

                for landmark in hand.landmarks:
                    landmark_proto = landmark_pb2.NormalizedLandmark()
                    landmark_proto.x = float(landmark[0])
                    landmark_proto.y = float(landmark[1])
                    landmark_proto.z = float(landmark[2])
                    hand_landmarks.landmark.append(landmark_proto)

                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )

            return frame
        except Exception as e:
            logger.error(f"Drawing error: {e}")
            return frame

    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'hands') and self.hands:
            try:
                self.hands.close()
            except Exception:
                pass
