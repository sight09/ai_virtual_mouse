"""
Cursor Controller Module
Handles mouse movements and actions
"""

import pyautogui
import numpy as np
import logging
from collections import deque
import threading
import time

logger = logging.getLogger(__name__)


class CursorController:
    """Controls mouse cursor and performs actions"""

    def __init__(self, smoothing_factor=0.7, screen_width=1920, screen_height=1080):
        """
        Initialize cursor controller

        Args:
            smoothing_factor: Exponential smoothing for cursor movement (0-1)
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.smoothing_factor = smoothing_factor
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.previous_pos = None
        self.movement_history = deque(maxlen=5)
        self.last_click_time = {}
        self.drag_active = False
        self.drag_start = None

        # Get actual screen size
        try:
            screen = pyautogui.size()
            self.screen_width = screen.width
            self.screen_height = screen.height
        except:
            pass

        logger.info(f"Cursor controller initialized: {self.screen_width}x{self.screen_height}")

    def move_cursor(self, hand_landmarks, camera_width, camera_height, sensitivity=1.0):
        """
        Move cursor based on hand index finger position

        Args:
            hand_landmarks: Hand landmarks array
            camera_width: Camera resolution width
            camera_height: Camera resolution height
            sensitivity: Movement sensitivity multiplier

        Returns:
            New cursor position (x, y)
        """
        try:
            # Index finger tip is landmark 8
            index_tip = hand_landmarks[8]
            x_cam, y_cam = index_tip[0], index_tip[1]

            # Convert camera coordinates to screen coordinates
            # Camera: (0,0) is top-left, (1,1) is bottom-right
            # Screen: (0,0) is top-left, (width, height) is bottom-right
            x_screen = x_cam * self.screen_width * sensitivity
            y_screen = y_cam * self.screen_height * sensitivity

            # Apply exponential smoothing
            if self.previous_pos is None:
                self.previous_pos = (x_screen, y_screen)
            else:
                x_smooth = (self.smoothing_factor * self.previous_pos[0] +
                           (1 - self.smoothing_factor) * x_screen)
                y_smooth = (self.smoothing_factor * self.previous_pos[1] +
                           (1 - self.smoothing_factor) * y_screen)
                x_screen, y_screen = x_smooth, y_smooth

            # Clamp to screen boundaries
            x_screen = max(0, min(self.screen_width - 1, x_screen))
            y_screen = max(0, min(self.screen_height - 1, y_screen))

            # Move cursor
            pyautogui.moveTo(int(x_screen), int(y_screen), duration=0)
            self.previous_pos = (x_screen, y_screen)
            self.movement_history.append((x_screen, y_screen))

            return (int(x_screen), int(y_screen))
        except Exception as e:
            logger.error(f"Cursor movement error: {e}")
            return None

    def left_click(self):
        """Perform left click"""
        try:
            pyautogui.click(button='left', clicks=1, interval=0)
            logger.debug("Left click performed")
        except Exception as e:
            logger.error(f"Left click error: {e}")

    def right_click(self):
        """Perform right click"""
        try:
            pyautogui.click(button='right', clicks=1, interval=0)
            logger.debug("Right click performed")
        except Exception as e:
            logger.error(f"Right click error: {e}")

    def double_click(self):
        """Perform double click"""
        try:
            pyautogui.click(button='left', clicks=2, interval=0.1)
            logger.debug("Double click performed")
        except Exception as e:
            logger.error(f"Double click error: {e}")

    def scroll(self, direction, amount=5):
        """
        Scroll in specified direction

        Args:
            direction: 'up' or 'down'
            amount: Scroll amount
        """
        try:
            if direction.lower() == 'up':
                pyautogui.scroll(amount)
                logger.debug(f"Scrolled up by {amount}")
            elif direction.lower() == 'down':
                pyautogui.scroll(-amount)
                logger.debug(f"Scrolled down by {amount}")
        except Exception as e:
            logger.error(f"Scroll error: {e}")

    def start_drag(self):
        """Start drag operation"""
        try:
            if self.previous_pos:
                self.drag_active = True
                self.drag_start = self.previous_pos
                pyautogui.mouseDown(button='left')
                logger.debug(f"Drag started at {self.previous_pos}")
        except Exception as e:
            logger.error(f"Drag start error: {e}")

    def end_drag(self):
        """End drag operation"""
        try:
            if self.drag_active:
                pyautogui.mouseUp(button='left')
                self.drag_active = False
                self.drag_start = None
                logger.debug("Drag ended")
        except Exception as e:
            logger.error(f"Drag end error: {e}")

    def is_dragging(self):
        """Check if drag is active"""
        return self.drag_active

    def set_screen_resolution(self, width, height):
        """Update screen resolution"""
        self.screen_width = width
        self.screen_height = height
        logger.info(f"Screen resolution updated: {width}x{height}")

    def calibrate(self):
        """Calibrate cursor position"""
        try:
            # Move cursor to center for calibration
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            pyautogui.moveTo(center_x, center_y, duration=0)
            self.previous_pos = (center_x, center_y)
            logger.info("Cursor calibrated to center")
            return (center_x, center_y)
        except Exception as e:
            logger.error(f"Calibration error: {e}")
            return None

    def get_cursor_position(self):
        """Get current cursor position"""
        try:
            return pyautogui.position()
        except Exception as e:
            logger.error(f"Position retrieval error: {e}")
            return None
