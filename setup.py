"""
Setup script for Virtual Mouse installation
Run this to verify and install dependencies
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True


def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import cv2
        print("✅ OpenCV installed")
    except ImportError:
        print("❌ OpenCV not installed")
        return False

    try:
        import mediapipe
        print("✅ MediaPipe installed")
    except ImportError:
        print("❌ MediaPipe not installed")
        return False

    try:
        import pyautogui
        print("✅ PyAutoGUI installed")
    except ImportError:
        print("❌ PyAutoGUI not installed")
        return False

    try:
        import customtkinter
        print("✅ CustomTkinter installed")
    except ImportError:
        print("❌ CustomTkinter not installed")
        return False

    try:
        import PIL
        print("✅ Pillow installed")
    except ImportError:
        print("❌ Pillow not installed")
        return False

    try:
        import numpy
        print("✅ NumPy installed")
    except ImportError:
        print("❌ NumPy not installed")
        return False

    return True


def install_dependencies():
    """Install dependencies from requirements.txt"""
    try:
        print("\n📦 Installing dependencies...")
        requirements_file = Path(__file__).parent / "requirements.txt"
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def check_camera():
    """Check if camera is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            print("✅ Webcam detected")
            return True
        else:
            print("⚠️  Webcam not accessible")
            return False
    except Exception as e:
        print(f"⚠️  Camera check failed: {e}")
        return False


def main():
    """Main setup function"""
    print("=" * 50)
    print("AI Virtual Mouse - Setup Assistant")
    print("=" * 50)

    # Check Python version
    print("\n1️⃣ Checking Python version...")
    if not check_python_version():
        sys.exit(1)

    # Check dependencies
    print("\n2️⃣ Checking dependencies...")
    deps_ok = check_dependencies()

    if not deps_ok:
        print("\n❌ Some dependencies are missing")
        response = input("Would you like to install them now? (y/n): ").lower()
        if response == 'y':
            if not install_dependencies():
                sys.exit(1)
        else:
            print("❌ Cannot proceed without dependencies")
            sys.exit(1)
    else:
        print("✅ All dependencies are installed")

    # Check camera
    print("\n3️⃣ Checking camera...")
    check_camera()

    # Create config directory
    print("\n4️⃣ Creating configuration directory...")
    config_dir = Path.home() / ".virtual_mouse"
    config_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Configuration directory: {config_dir}")

    print("\n" + "=" * 50)
    print("✅ Setup complete! You can now run: python main.py")
    print("=" * 50)


if __name__ == "__main__":
    main()
