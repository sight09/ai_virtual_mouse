"""
Installation Verification Script
Verifies that all components are properly installed and configured
"""

import sys
import os
from pathlib import Path

def verify_installation():
    """Verify complete installation"""
    print("\n" + "="*60)
    print("AI Virtual Mouse - Installation Verification")
    print("="*60 + "\n")

    checks = {
        "Python Version": check_python_version,
        "Required Packages": check_packages,
        "Project Files": check_project_files,
        "Camera Access": check_camera,
        "Configuration": check_config,
    }

    results = {}
    for check_name, check_func in checks.items():
        print(f"\n🔍 {check_name}...")
        try:
            result = check_func()
            results[check_name] = result
            status = "✅ PASS" if result else "⚠️  WARNING"
            print(f"   {status}")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            results[check_name] = False

    # Summary
    print("\n" + "="*60)
    print("Verification Summary")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for check_name, result in results.items():
        status = "✅" if result else "⚠️ "
        print(f"{status} {check_name}")

    print(f"\nResult: {passed}/{total} checks passed\n")

    if passed == total:
        print("🎉 Installation is complete and ready to use!")
        print("   Run: python main.py")
        return True
    else:
        print("⚠️  Some checks failed. See details above.")
        return False


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    return version >= (3, 11)


def check_packages():
    """Check if all required packages are installed"""
    packages = {
        'cv2': 'OpenCV',
        'mediapipe': 'MediaPipe',
        'pyautogui': 'PyAutoGUI',
        'customtkinter': 'CustomTkinter',
        'PIL': 'Pillow',
        'numpy': 'NumPy',
    }

    all_installed = True
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} - Not installed")
            all_installed = False

    return all_installed


def check_project_files():
    """Check if all project files exist"""
    project_root = Path(__file__).parent
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'core/__init__.py',
        'core/engine.py',
        'gui/__init__.py',
        'gui/app.py',
        'config.example.json',
    ]

    all_exist = True
    missing = []

    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Missing")
            all_exist = False
            missing.append(file_path)

    if not all_exist:
        print(f"\n   Missing files: {', '.join(missing)}")

    return all_exist


def check_camera():
    """Check camera availability"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            cap.release()
            print(f"   ✅ Camera found: {width}x{height} @ {fps}fps")
            return True
        else:
            print("   ⚠️  Camera not accessible (may need permission)")
            return False
    except Exception as e:
        print(f"   ⚠️  Camera check failed: {e}")
        return False


def check_config():
    """Check configuration system"""
    try:
        from core.config_manager import ConfigManager
        config_mgr = ConfigManager()
        config = config_mgr.get_config()
        config_dir = config_mgr.config_dir
        print(f"   ✅ Configuration ready")
        print(f"   📁 Config directory: {config_dir}")
        return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False


def print_system_info():
    """Print system information"""
    print("\nSystem Information:")
    print(f"  Python: {sys.version}")
    print(f"  Platform: {sys.platform}")
    print(f"  Home: {Path.home()}")


if __name__ == "__main__":
    print_system_info()
    success = verify_installation()
    sys.exit(0 if success else 1)
