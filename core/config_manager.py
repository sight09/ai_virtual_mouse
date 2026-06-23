"""
Configuration Manager Module
Handles application settings and configuration
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
import os

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Application configuration"""
    # Camera settings
    camera_index: int = 0
    camera_fps: int = 30

    # Cursor settings
    cursor_speed: float = 1.0
    cursor_smoothing: float = 0.7

    # Detection settings
    detection_confidence: float = 0.7
    tracking_confidence: float = 0.5

    # Gesture settings
    gesture_timeout: float = 0.3
    smoothing_window: int = 5

    # UI settings
    theme: str = "dark"
    show_fps: bool = True
    show_landmarks: bool = True

    # Action settings
    enable_double_click: bool = True
    enable_drag: bool = True
    enable_scroll: bool = True

    # Screen calibration
    screen_width: int = 1920
    screen_height: int = 1080
    calibrated: bool = False


class ConfigManager:
    """Manages application configuration"""

    CONFIG_DIR = Path.home() / ".virtual_mouse"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self):
        """Initialize config manager"""
        self.config_dir = self.CONFIG_DIR
        self.config_file = self.CONFIG_FILE
        self.config = Config()
        self._ensure_config_dir()
        self.load()

    def _ensure_config_dir(self):
        """Ensure config directory exists"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Config directory: {self.config_dir}")
        except Exception as e:
            logger.error(f"Failed to create config directory: {e}")

    def load(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.config = Config(**data)
                logger.info("Configuration loaded successfully")
            else:
                self.save()
                logger.info("Default configuration created")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            self.config = Config()

    def save(self):
        """Save configuration to file"""
        try:
            self._ensure_config_dir()
            with open(self.config_file, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
            logger.info("Configuration saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    def get_config(self):
        """Get configuration object"""
        return self.config

    def update(self, **kwargs):
        """Update configuration values"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                    logger.debug(f"Config updated: {key} = {value}")
            return True
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
            return False

    def get(self, key, default=None):
        """Get configuration value"""
        try:
            return getattr(self.config, key, default)
        except Exception as e:
            logger.error(f"Failed to get config value: {e}")
            return default

    def reset(self):
        """Reset to default configuration"""
        self.config = Config()
        self.save()
        logger.info("Configuration reset to defaults")

    def get_config_path(self):
        """Get configuration file path"""
        return self.config_file
