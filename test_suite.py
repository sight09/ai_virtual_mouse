"""
Testing and Debugging Utilities
Helpers for development and troubleshooting
"""

import logging
import cv2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core import CameraManager, HandDetector, GestureRecognizer

logger = logging.getLogger(__name__)


def test_camera():
    """Test camera functionality"""
    print("Testing camera...")
    camera = CameraManager()

    if not camera.initialize():
        print("❌ Camera initialization failed")
        return False

    camera.start()

    try:
        for i in range(30):
            frame = camera.get_frame()
            if frame is None:
                print(f"Frame {i}: None")
            else:
                print(f"Frame {i}: {frame.shape}")

        print("✅ Camera test passed")
        return True
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False
    finally:
        camera.stop()


def test_hand_detection():
    """Test hand detection"""
    print("\nTesting hand detection...")
    camera = CameraManager()
    detector = HandDetector()

    if not camera.initialize():
        print("❌ Camera initialization failed")
        return False

    camera.start()

    try:
        detected_count = 0
        for i in range(100):
            frame = camera.get_frame()
            if frame is None:
                continue

            hands = detector.detect(frame)
            if hands:
                detected_count += 1
                print(f"Frame {i}: Detected {len(hands)} hand(s)")

        if detected_count > 0:
            print(f"✅ Hand detection test passed ({detected_count}/100 frames with hands)")
            return True
        else:
            print("⚠️  No hands detected in test frames")
            return False
    except Exception as e:
        print(f"❌ Hand detection test failed: {e}")
        return False
    finally:
        camera.stop()


def test_gesture_recognition():
    """Test gesture recognition"""
    print("\nTesting gesture recognition...")
    camera = CameraManager()
    detector = HandDetector()
    recognizer = GestureRecognizer()

    if not camera.initialize():
        print("❌ Camera initialization failed")
        return False

    camera.start()

    try:
        gesture_count = {}
        for i in range(150):
            frame = camera.get_frame()
            if frame is None:
                continue

            hands = detector.detect(frame)
            if hands:
                gesture, confidence, _ = recognizer.recognize(hands)
                gesture_str = gesture.value
                gesture_count[gesture_str] = gesture_count.get(gesture_str, 0) + 1

                if gesture_str != 'move' and gesture_str != 'none':
                    print(f"Frame {i}: {gesture_str} (confidence: {confidence:.2f})")

        print(f"\nGesture distribution:")
        for gesture, count in sorted(gesture_count.items()):
            print(f"  {gesture}: {count}")

        print("✅ Gesture recognition test completed")
        return True
    except Exception as e:
        print(f"❌ Gesture recognition test failed: {e}")
        return False
    finally:
        camera.stop()


def test_camera_resolution():
    """Test camera resolution and FPS"""
    print("\nTesting camera resolution and FPS...")
    camera = CameraManager()

    if not camera.initialize():
        print("❌ Camera initialization failed")
        return False

    width, height = camera.get_resolution()
    fps = camera.get_fps()

    print(f"Resolution: {width}x{height}")
    print(f"FPS: {fps}")

    if width > 0 and height > 0:
        print("✅ Camera resolution test passed")
        return True
    else:
        print("❌ Invalid resolution")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("AI Virtual Mouse - Test Suite")
    print("=" * 50)

    results = {
        "Camera": test_camera_resolution(),
        "Hand Detection": test_hand_detection(),
        "Gesture Recognition": test_gesture_recognition(),
    }

    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")

    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")

    return all(results.values())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success = run_all_tests()
    sys.exit(0 if success else 1)
