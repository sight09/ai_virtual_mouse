"""
Camera Manager Module
Handles webcam capture and frame processing
"""

import cv2
import logging
from threading import Thread, Lock
from queue import Queue
import numpy as np

logger = logging.getLogger(__name__)


class CameraManager:
    """Manages webcam capture and frame delivery"""

    def __init__(self, camera_index=0, target_fps=30):
        self.camera_index = camera_index
        self.target_fps = target_fps
        self.cap = None
        self.running = False
        self.frame_queue = Queue(maxsize=2)
        self.lock = Lock()
        self.thread = None
        self.frame_count = 0
        self.width = 640
        self.height = 480
        self.fps = 30

    def initialize(self):
        """Initialize camera"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                raise RuntimeError(f"Failed to open camera {self.camera_index}")

            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, self.target_fps)

            # Get actual values
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))

            logger.info(f"Camera initialized: {self.width}x{self.height} @ {self.fps} FPS")
            return True
        except Exception as e:
            logger.error(f"Camera initialization failed: {e}")
            return False

    def start(self):
        """Start capturing frames in background thread"""
        if not self.cap:
            self.initialize()

        self.running = True
        self.thread = Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        logger.info("Camera capture started")

    def _capture_loop(self):
        """Background thread for frame capture"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                logger.warning("Failed to read frame")
                continue

            self.frame_count += 1

            # Try to put frame in queue, drop old frame if queue full
            try:
                self.frame_queue.put_nowait(frame)
            except:
                try:
                    self.frame_queue.get_nowait()
                    self.frame_queue.put_nowait(frame)
                except:
                    pass

    def get_frame(self):
        """Get latest frame"""
        try:
            frame = self.frame_queue.get(timeout=1)
            return frame
        except:
            return None

    def stop(self):
        """Stop camera capture"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.cap:
            self.cap.release()
        logger.info("Camera stopped")

    def get_resolution(self):
        """Get camera resolution"""
        return (self.width, self.height)

    def get_fps(self):
        """Get FPS"""
        return self.fps

    def __del__(self):
        """Cleanup"""
        if self.cap:
            self.cap.release()
