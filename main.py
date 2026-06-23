#!/usr/bin/env python3
"""
AI Virtual Mouse - Main Application Entry Point
Real-time hand gesture recognition system for mouse control
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.app import VirtualMouseApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('virtual_mouse.log'),
        logging.StreamHandler()
    ]
)


if __name__ == "__main__":
    app = VirtualMouseApp()
    app.run()
