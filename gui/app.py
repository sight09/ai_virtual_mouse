"""
Main GUI Application Module
User interface for Virtual Mouse application
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import threading
import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core import VirtualMouseEngine, GestureType

logger = logging.getLogger(__name__)


class VirtualMouseApp(ctk.CTk):
    """Main application window"""

    def __init__(self):
        """Initialize application"""
        super().__init__()

        self.title("AI Virtual Mouse - Hand Gesture Control")
        self.geometry("1400x900")
        self.resizable(True, True)

        # Initialize engine
        self.engine = VirtualMouseEngine()
        if not self.engine.initialize():
            logger.error("Failed to initialize engine")
            return

        self.running = True
        self.current_frame = None

        # Setup UI
        self._setup_ui()

        # Start processing thread
        self.process_thread = threading.Thread(target=self._process_loop, daemon=True)
        self.process_thread.start()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        logger.info("Application started")

    def _setup_ui(self):
        """Setup user interface"""
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)

        # Left panel - Video
        left_frame = ctk.CTkFrame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        # Video label
        self.video_label = ctk.CTkLabel(left_frame, text="", fg_color="black")
        self.video_label.grid(row=0, column=0, sticky="nsew")

        # Right panel - Controls and info
        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_frame.grid_rowconfigure(4, weight=1)

        # Status section
        status_frame = ctk.CTkFrame(right_frame, fg_color="gray25")
        status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(status_frame, text="STATUS", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        self.fps_label = ctk.CTkLabel(status_frame, text="FPS: 0", font=("Arial", 11))
        self.fps_label.pack(anchor="w", padx=15, pady=2)

        self.gesture_label = ctk.CTkLabel(status_frame, text="Gesture: None", font=("Arial", 11))
        self.gesture_label.pack(anchor="w", padx=15, pady=2)

        self.confidence_label = ctk.CTkLabel(status_frame, text="Confidence: 0%", font=("Arial", 11))
        self.confidence_label.pack(anchor="w", padx=15, pady=2)

        self.hands_label = ctk.CTkLabel(status_frame, text="Hands: 0", font=("Arial", 11))
        self.hands_label.pack(anchor="w", padx=15, pady=2)

        self.cursor_label = ctk.CTkLabel(status_frame, text="Cursor: (0, 0)", font=("Arial", 11))
        self.cursor_label.pack(anchor="w", padx=15, pady=5)

        # Controls section
        control_frame = ctk.CTkFrame(right_frame, fg_color="gray25")
        control_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(control_frame, text="CONTROLS", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        self.pause_btn = ctk.CTkButton(
            control_frame,
            text="⏸ Pause Tracking",
            command=self._toggle_pause,
            font=("Arial", 11)
        )
        self.pause_btn.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            control_frame,
            text="🎯 Calibrate Cursor",
            command=self._calibrate,
            font=("Arial", 11)
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            control_frame,
            text="⚙️ Settings",
            command=self._open_settings,
            font=("Arial", 11)
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            control_frame,
            text="ℹ️ Help",
            command=self._show_help,
            font=("Arial", 11)
        ).pack(fill="x", padx=10, pady=5)

        # Settings section
        settings_frame = ctk.CTkFrame(right_frame, fg_color="gray25")
        settings_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(settings_frame, text="SETTINGS", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)

        # Cursor speed
        ctk.CTkLabel(settings_frame, text="Cursor Speed:", font=("Arial", 10)).pack(anchor="w", padx=10, pady=(5, 2))
        speed_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        speed_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.speed_slider = ctk.CTkSlider(
            speed_frame,
            from_=0.5,
            to=2.0,
            number_of_steps=15,
            command=self._update_speed
        )
        self.speed_slider.set(self.engine.config.cursor_speed)
        self.speed_slider.pack(side="left", fill="x", expand=True)

        self.speed_label = ctk.CTkLabel(speed_frame, text="1.0x", font=("Arial", 10), width=40)
        self.speed_label.pack(side="left", padx=(5, 0))

        # Smoothing
        ctk.CTkLabel(settings_frame, text="Smoothing:", font=("Arial", 10)).pack(anchor="w", padx=10, pady=(5, 2))
        smooth_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        smooth_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.smooth_slider = ctk.CTkSlider(
            smooth_frame,
            from_=0.0,
            to=1.0,
            number_of_steps=20,
            command=self._update_smoothing
        )
        self.smooth_slider.set(self.engine.config.cursor_smoothing)
        self.smooth_slider.pack(side="left", fill="x", expand=True)

        self.smooth_label = ctk.CTkLabel(smooth_frame, text="0.7", font=("Arial", 10), width=40)
        self.smooth_label.pack(side="left", padx=(5, 0))

        # Detection confidence
        ctk.CTkLabel(settings_frame, text="Detection Confidence:", font=("Arial", 10)).pack(anchor="w", padx=10, pady=(5, 2))
        conf_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        conf_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.conf_slider = ctk.CTkSlider(
            conf_frame,
            from_=0.3,
            to=0.9,
            number_of_steps=12,
            command=self._update_confidence
        )
        self.conf_slider.set(self.engine.config.detection_confidence)
        self.conf_slider.pack(side="left", fill="x", expand=True)

        self.conf_label = ctk.CTkLabel(conf_frame, text="0.7", font=("Arial", 10), width=40)
        self.conf_label.pack(side="left", padx=(5, 0))

        # Checkboxes
        self.landmarks_var = ctk.BooleanVar(value=self.engine.config.show_landmarks)
        ctk.CTkCheckBox(
            settings_frame,
            text="Show Hand Landmarks",
            variable=self.landmarks_var,
            command=self._toggle_landmarks
        ).pack(anchor="w", padx=10, pady=5)

        self.fps_var = ctk.BooleanVar(value=self.engine.config.show_fps)
        ctk.CTkCheckBox(
            settings_frame,
            text="Show FPS",
            variable=self.fps_var,
            command=self._toggle_fps
        ).pack(anchor="w", padx=10, pady=5)

        # Gesture info section
        info_frame = ctk.CTkFrame(right_frame, fg_color="gray25")
        info_frame.grid(row=4, column=0, sticky="nsew", pady=(0, 0))

        ctk.CTkLabel(info_frame, text="SUPPORTED GESTURES", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 5))

        gestures_text = ctk.CTkTextbox(info_frame, height=200, font=("Arial", 9))
        gestures_text.pack(fill="both", expand=True, padx=10, pady=10)

        gesture_info = """
Index finger pointing → Move cursor
Two fingers up → Left click
Peace sign (spread) → Right click
Both hands (fist) → Scroll down
All fingers up → Scroll up
Thumb + pinky → Volume up
Thumb only → Volume down
Thumb + middle touch → Double click
Index up + middle down → Drag
        """
        gestures_text.insert("1.0", gesture_info)
        gestures_text.configure(state="disabled")

    def _process_loop(self):
        """Main processing loop"""
        while self.running:
            try:
                frame, results = self.engine.process_frame()
                if frame is not None:
                    self.current_frame = frame
                    self._update_display(frame, results)
                else:
                    pass
            except Exception as e:
                logger.error(f"Processing loop error: {e}")

    def _update_display(self, frame, results):
        """Update display with frame and info"""
        try:
            # Resize frame for display
            display_height = 600
            aspect_ratio = frame.shape[1] / frame.shape[0]
            display_width = int(display_height * aspect_ratio)
            frame_resized = cv2.resize(frame, (display_width, display_height))

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            # Convert to PIL Image
            pil_image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(pil_image)

            # Update label
            self.video_label.configure(image=photo)
            self.video_label.image = photo

            # Update status
            status = self.engine.get_status()
            self.fps_label.configure(text=f"FPS: {status['fps']}")
            self.gesture_label.configure(text=f"Gesture: {status['gesture'].title()}")
            self.confidence_label.configure(text=f"Confidence: {int(status['confidence'] * 100)}%")
            self.hands_label.configure(text=f"Hands: {status['hands_detected']}")
            cursor_x, cursor_y = status['cursor_pos']
            self.cursor_label.configure(text=f"Cursor: ({cursor_x}, {cursor_y})")

        except Exception as e:
            logger.error(f"Display update error: {e}")

    def _toggle_pause(self):
        """Toggle tracking pause"""
        self.engine.toggle_pause()
        text = "▶ Resume Tracking" if self.engine.paused else "⏸ Pause Tracking"
        self.pause_btn.configure(text=text)

    def _calibrate(self):
        """Calibrate cursor"""
        self.engine.calibrate()
        logger.info("Cursor calibrated")

    def _open_settings(self):
        """Open settings window"""
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Advanced Settings")
        settings_window.geometry("500x600")
        settings_window.resizable(False, False)

        # Configure dark mode
        settings_window.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(settings_window, text="Advanced Settings", font=("Arial", 16, "bold")).pack(pady=10)

        # Settings frame with scrollbar
        scrollable_frame = ctk.CTkScrollableFrame(settings_window)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Detection settings
        ctk.CTkLabel(scrollable_frame, text="Detection Settings", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(scrollable_frame, text="Min Detection Confidence").pack(anchor="w", padx=10)
        det_slider = ctk.CTkSlider(scrollable_frame, from_=0.3, to=0.9, number_of_steps=12)
        det_slider.set(self.engine.config.detection_confidence)
        det_slider.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(scrollable_frame, text="Min Tracking Confidence").pack(anchor="w", padx=10)
        track_slider = ctk.CTkSlider(scrollable_frame, from_=0.3, to=0.9, number_of_steps=12)
        track_slider.set(self.engine.config.tracking_confidence)
        track_slider.pack(fill="x", padx=10, pady=5)

        # Gesture settings
        ctk.CTkLabel(scrollable_frame, text="Gesture Settings", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(scrollable_frame, text="Gesture Timeout (seconds)").pack(anchor="w", padx=10)
        timeout_slider = ctk.CTkSlider(scrollable_frame, from_=0.1, to=1.0, number_of_steps=18)
        timeout_slider.set(self.engine.config.gesture_timeout)
        timeout_slider.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(scrollable_frame, text="Smoothing Window (frames)").pack(anchor="w", padx=10)
        window_slider = ctk.CTkSlider(scrollable_frame, from_=1, to=15, number_of_steps=14)
        window_slider.set(self.engine.config.smoothing_window)
        window_slider.pack(fill="x", padx=10, pady=5)

        # Info
        ctk.CTkLabel(scrollable_frame, text="Application Info", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(scrollable_frame, text="Version: 1.0.0", font=("Arial", 10)).pack(anchor="w", padx=10)
        ctk.CTkLabel(scrollable_frame, text="Camera: Webcam", font=("Arial", 10)).pack(anchor="w", padx=10)

        # Save button
        def save_settings():
            self.engine.update_config(
                detection_confidence=det_slider.get(),
                tracking_confidence=track_slider.get(),
                gesture_timeout=timeout_slider.get(),
                smoothing_window=int(window_slider.get())
            )
            settings_window.destroy()

        ctk.CTkButton(settings_window, text="Save Settings", command=save_settings).pack(pady=10, padx=10, fill="x")

    def _show_help(self):
        """Show help window"""
        help_window = ctk.CTkToplevel(self)
        help_window.title("Help & Instructions")
        help_window.geometry("600x700")
        help_window.resizable(False, False)

        help_text = ctk.CTkTextbox(help_window, font=("Arial", 10))
        help_text.pack(fill="both", expand=True, padx=10, pady=10)

        help_content = """
AI VIRTUAL MOUSE - USER GUIDE

Getting Started:
1. Allow the application to access your webcam
2. Position yourself in front of the camera
3. Make sure there's adequate lighting
4. Calibrate your cursor position before use

Hand Tracking:
- The system detects your hand landmarks
- Confidence level indicates detection accuracy
- If hands are not detected, improve lighting or move closer

Gesture Controls:
- Cursor Movement: Point your index finger
- Left Click: Bring index and middle fingers together
- Right Click: Make a peace sign (index & middle apart)
- Scroll Down: Close all fingers (fist)
- Scroll Up: Open all fingers
- Volume Up: Thumb + pinky extended
- Volume Down: Thumb only extended
- Double Click: Thumb touches middle finger
- Drag: Index up, others closed

Settings:
- Cursor Speed: Adjust movement sensitivity
- Smoothing: Reduce cursor jitter (higher = smoother)
- Detection Confidence: Higher = more accurate but slower

Troubleshooting:
- Poor detection: Improve lighting, reduce background clutter
- Jerky movement: Increase smoothing value
- Missed gestures: Calibrate cursor and adjust confidence
- No hand detected: Check camera permissions and lighting

Performance:
- Optimal FPS: 25-30
- Lower FPS may affect responsiveness
- Check system resources if FPS drops

Tips:
- Keep your hand within camera view
- Avoid sudden movements
- Use consistent lighting
- Calibrate after moving camera
- Take breaks to avoid fatigue

Questions? Check the README.md file for more information.
        """
        help_text.insert("1.0", help_content)
        help_text.configure(state="disabled")

    def _update_speed(self, value):
        """Update cursor speed"""
        value = float(value)
        self.speed_label.configure(text=f"{value:.1f}x")
        self.engine.update_config(cursor_speed=value)

    def _update_smoothing(self, value):
        """Update smoothing factor"""
        value = float(value)
        self.smooth_label.configure(text=f"{value:.2f}")
        self.engine.update_config(cursor_smoothing=value)

    def _update_confidence(self, value):
        """Update detection confidence"""
        value = float(value)
        self.conf_label.configure(text=f"{value:.2f}")
        self.engine.update_config(detection_confidence=value)

    def _toggle_landmarks(self):
        """Toggle landmark display"""
        self.engine.update_config(show_landmarks=self.landmarks_var.get())

    def _toggle_fps(self):
        """Toggle FPS display"""
        self.engine.update_config(show_fps=self.fps_var.get())

    def on_closing(self):
        """Handle window closing"""
        self.running = False
        self.engine.shutdown()
        self.destroy()

    def run(self):
        """Run the application"""
        self.mainloop()
