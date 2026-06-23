"""
Virtual Mouse Engine Module
Main processing engine that ties all components together
"""

import logging
import cv2
import time
from .camera_manager import CameraManager
from .hand_detector import HandDetector
from .gesture_recognizer import GestureRecognizer, GestureType
from .cursor_controller import CursorController
from .config_manager import ConfigManager

logger = logging.getLogger(__name__)


class VirtualMouseEngine:
    """Main engine for virtual mouse functionality"""

    def __init__(self, config_manager=None):
        """
        Initialize virtual mouse engine

        Args:
            config_manager: ConfigManager instance
        """
        self.config_manager = config_manager or ConfigManager()
        self.config = self.config_manager.get_config()

        # Initialize components
        self.camera = CameraManager(
            camera_index=self.config.camera_index,
            target_fps=self.config.camera_fps
        )
        self.detector = HandDetector(
            min_detection_confidence=self.config.detection_confidence,
            min_tracking_confidence=self.config.tracking_confidence
        )
        self.recognizer = GestureRecognizer(
            smoothing_window=self.config.smoothing_window,
            gesture_timeout=self.config.gesture_timeout
        )
        self.controller = CursorController(
            smoothing_factor=self.config.cursor_smoothing,
            screen_width=self.config.screen_width,
            screen_height=self.config.screen_height
        )

        # State tracking
        self.running = False
        self.paused = False
        self.current_gesture = GestureType.NONE
        self.gesture_confidence = 0.0
        self.fps = 0
        self.frame_count = 0
        self.start_time = 0
        self.cursor_pos = (0, 0)
        self.current_hands = []

        logger.info("Virtual Mouse Engine initialized")

    def initialize(self):
        """Initialize camera and components"""
        if not self.camera.initialize():
            logger.error("Failed to initialize camera")
            return False

        self.camera.start()
        logger.info("Engine initialized successfully")
        return True

    def process_frame(self):
        """
        Process single frame and return results

        Returns:
            Tuple (frame, detection_results) or (None, None) on error
        """
        try:
            # Capture frame
            frame = self.camera.get_frame()
            if frame is None:
                return None, None

            self.frame_count += 1

            # Detect hands
            hands = self.detector.detect(frame)
            self.current_hands = hands

            # Recognize gestures
            if hands and not self.paused:
                gesture, confidence, hand_idx = self.recognizer.recognize(hands)
                self.current_gesture = gesture
                self.gesture_confidence = confidence

                # Execute actions
                if gesture != GestureType.NONE and gesture != GestureType.MOVE:
                    self._execute_gesture(gesture)
                elif gesture == GestureType.MOVE or gesture == GestureType.DRAG:
                    # Update cursor position
                    self.cursor_pos = self.controller.move_cursor(
                        hands[0].landmarks,
                        frame.shape[1],
                        frame.shape[0],
                        self.config.cursor_speed
                    ) or self.cursor_pos
            else:
                self.current_gesture = GestureType.NONE
                self.gesture_confidence = 0.0

            # Draw landmarks on frame
            if self.config.show_landmarks:
                frame = self.detector.draw_landmarks(frame, hands)

            # Calculate FPS
            if self.frame_count % 10 == 0:
                current_time = time.time()
                if self.start_time > 0:
                    elapsed = current_time - self.start_time
                    self.fps = int(self.frame_count / elapsed) if elapsed > 0 else 0

            return frame, {
                'hands': hands,
                'gesture': self.current_gesture,
                'confidence': self.gesture_confidence,
                'cursor_pos': self.cursor_pos,
                'fps': self.fps,
                'frame_count': self.frame_count
            }

        except Exception as e:
            logger.error(f"Frame processing error: {e}")
            return None, None

    def _execute_gesture(self, gesture):
        """Execute action for gesture"""
        try:
            if gesture == GestureType.LEFT_CLICK:
                self.controller.left_click()
            elif gesture == GestureType.RIGHT_CLICK:
                self.controller.right_click()
            elif gesture == GestureType.DOUBLE_CLICK:
                self.controller.double_click()
            elif gesture == GestureType.SCROLL_UP:
                self.controller.scroll('up', 3)
            elif gesture == GestureType.SCROLL_DOWN:
                self.controller.scroll('down', 3)
            elif gesture == GestureType.DRAG:
                if not self.controller.is_dragging():
                    self.controller.start_drag()
            elif gesture == GestureType.PAUSE:
                self.paused = not self.paused
            elif gesture == GestureType.SCREENSHOT:
                self._take_screenshot()
        except Exception as e:
            logger.error(f"Gesture execution error: {e}")

    def _take_screenshot(self):
        """Take screenshot"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            path = self.config_manager.config_dir / filename
            cv2.imwrite(str(path), self.current_frame)
            logger.info(f"Screenshot saved: {path}")
        except Exception as e:
            logger.error(f"Screenshot error: {e}")

    def toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused
        logger.info(f"Paused: {self.paused}")

    def update_config(self, **kwargs):
        """Update configuration"""
        self.config_manager.update(**kwargs)
        self.config = self.config_manager.get_config()

        # Update components with new config
        if 'cursor_smoothing' in kwargs:
            self.controller.smoothing_factor = kwargs['cursor_smoothing']
        if 'cursor_speed' in kwargs:
            self.controller.smoothing_factor = kwargs['cursor_speed']

    def calibrate(self):
        """Calibrate cursor"""
        return self.controller.calibrate()

    def shutdown(self):
        """Shutdown engine"""
        try:
            self.camera.stop()
            self.config_manager.save()
            logger.info("Engine shutdown complete")
        except Exception as e:
            logger.error(f"Shutdown error: {e}")

    def get_status(self):
        """Get engine status"""
        return {
            'running': self.running,
            'paused': self.paused,
            'frame_count': self.frame_count,
            'fps': self.fps,
            'gesture': self.current_gesture.value,
            'confidence': self.gesture_confidence,
            'hands_detected': len(self.current_hands),
            'cursor_pos': self.cursor_pos
        }
