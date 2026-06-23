"""
Gesture Recognizer Module
Recognizes hand gestures from landmarks
"""

import numpy as np
import logging
from enum import Enum
from collections import deque
import time

logger = logging.getLogger(__name__)


class GestureType(Enum):
    """Enumeration of gestures"""
    NONE = "none"
    MOVE = "move"
    LEFT_CLICK = "left_click"
    RIGHT_CLICK = "right_click"
    DOUBLE_CLICK = "double_click"
    DRAG = "drag"
    SCROLL_UP = "scroll_up"
    SCROLL_DOWN = "scroll_down"
    VOLUME_UP = "volume_up"
    VOLUME_DOWN = "volume_down"
    BRIGHTNESS_UP = "brightness_up"
    BRIGHTNESS_DOWN = "brightness_down"
    PAUSE = "pause"
    SCREENSHOT = "screenshot"


class GestureRecognizer:
    """Recognizes gestures from hand landmarks"""

    def __init__(self, smoothing_window=5, gesture_timeout=0.3):
        """
        Initialize gesture recognizer

        Args:
            smoothing_window: Number of frames for temporal smoothing
            gesture_timeout: Minimum time between same gestures (seconds)
        """
        self.smoothing_window = smoothing_window
        self.gesture_timeout = gesture_timeout
        self.gesture_history = deque(maxlen=smoothing_window)
        self.last_gesture_time = {}
        self.previous_gesture = GestureType.NONE

    def recognize(self, hands):
        """
        Recognize gestures from hand data

        Args:
            hands: List of HandLandmarks

        Returns:
            Tuple (gesture_type, confidence, hand_index)
        """
        if not hands:
            self.gesture_history.append(GestureType.NONE)
            return GestureType.NONE, 0.0, -1

        # Process primary hand (usually right)
        hand = hands[0]
        gesture, confidence = self._recognize_gesture(hand)

        # Apply temporal smoothing
        self.gesture_history.append(gesture)

        # Check if gesture should be triggered (majority vote)
        if len(self.gesture_history) >= self.smoothing_window:
            gestures = list(self.gesture_history)
            gesture_counts = {}
            for g in gestures:
                gesture_counts[g] = gesture_counts.get(g, 0) + 1

            final_gesture = max(gesture_counts, key=gesture_counts.get)
            count = gesture_counts[final_gesture]
            confidence = count / len(gestures)

            # Check timeout for repeated gestures
            current_time = time.time()
            if final_gesture != GestureType.NONE and final_gesture != GestureType.MOVE:
                last_time = self.last_gesture_time.get(final_gesture, 0)
                if current_time - last_time < self.gesture_timeout:
                    return GestureType.MOVE, 0.0, 0

                self.last_gesture_time[final_gesture] = current_time

            self.previous_gesture = final_gesture
            return final_gesture, confidence, 0

        return GestureType.MOVE, 0.5, 0

    def _recognize_gesture(self, hand):
        """
        Recognize single gesture from hand

        Args:
            hand: HandLandmarks object

        Returns:
            Tuple (gesture_type, confidence)
        """
        landmarks = hand.landmarks

        # Get key distances and angles
        thumb_extended = self._is_thumb_extended(landmarks)
        index_extended = self._is_index_extended(landmarks)
        middle_extended = self._is_middle_extended(landmarks)
        ring_extended = self._is_ring_extended(landmarks)
        pinky_extended = self._is_pinky_extended(landmarks)

        fingers_extended = [thumb_extended, index_extended, middle_extended,
                          ring_extended, pinky_extended]

        # Check for specific gestures
        # Left click: Index and middle extended, others closed
        if index_extended and middle_extended and not ring_extended and not pinky_extended:
            distance = self._get_distance(landmarks[8], landmarks[12])
            if distance < 0.05:
                return GestureType.LEFT_CLICK, 0.8

        # Right click: Only index extended (peace sign)
        if index_extended and middle_extended and not ring_extended and not pinky_extended:
            distance = self._get_distance(landmarks[8], landmarks[12])
            if distance > 0.1:
                return GestureType.RIGHT_CLICK, 0.8

        # Scroll down: Palm down, hand moves down
        if not thumb_extended and not index_extended and not middle_extended:
            return GestureType.SCROLL_DOWN, 0.7

        # Scroll up: Palm up, hand moves up
        if all(fingers_extended):
            return GestureType.SCROLL_UP, 0.7

        # Volume up: Thumb and pinky extended
        if thumb_extended and pinky_extended and not index_extended:
            return GestureType.VOLUME_UP, 0.7

        # Volume down: Only thumb extended
        if thumb_extended and not index_extended and not pinky_extended:
            return GestureType.VOLUME_DOWN, 0.7

        # Double click: Thumb and middle finger touching
        distance = self._get_distance(landmarks[4], landmarks[12])
        if distance < 0.05:
            return GestureType.DOUBLE_CLICK, 0.8

        # Drag: Index extended, middle closed
        if index_extended and not middle_extended:
            return GestureType.DRAG, 0.7

        # Default: Move
        return GestureType.MOVE, 0.5

    def _is_thumb_extended(self, landmarks):
        """Check if thumb is extended"""
        return self._get_distance(landmarks[2], landmarks[3]) > 0.05

    def _is_index_extended(self, landmarks):
        """Check if index finger is extended"""
        return self._get_distance(landmarks[5], landmarks[8]) > 0.1

    def _is_middle_extended(self, landmarks):
        """Check if middle finger is extended"""
        return self._get_distance(landmarks[9], landmarks[12]) > 0.1

    def _is_ring_extended(self, landmarks):
        """Check if ring finger is extended"""
        return self._get_distance(landmarks[13], landmarks[16]) > 0.1

    def _is_pinky_extended(self, landmarks):
        """Check if pinky finger is extended"""
        return self._get_distance(landmarks[17], landmarks[20]) > 0.1

    def _get_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return np.sqrt((point1[0] - point2[0])**2 +
                      (point1[1] - point2[1])**2 +
                      (point1[2] - point2[2])**2)

    def reset(self):
        """Reset gesture history"""
        self.gesture_history.clear()
        self.last_gesture_time.clear()
