# AI Virtual Mouse - Hand Gesture Recognition System

A professional-grade Python application that allows you to control your computer entirely through hand gestures detected by your webcam. This system replaces traditional mouse interactions with intuitive, real-time gesture controls powered by computer vision and machine learning.

## Features

- **Real-Time Hand Detection**: Detect and track hand landmarks using MediaPipe
- **Gesture Recognition**: 14+ supported gestures including click, drag, scroll, and volume control
- **Smooth Cursor Movement**: Advanced smoothing algorithms minimize jitter
- **Customizable Settings**: Adjust sensitivity, smoothing, and detection confidence
- **Modern GUI**: Clean, intuitive interface with real-time feedback
- **Calibration Tools**: Automatic and manual calibration for optimal performance
- **Low Latency**: Optimized for real-time responsiveness

## System Requirements

- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.11 or higher
- **Webcam**: Any USB webcam or built-in camera
- **RAM**: 4GB minimum (8GB recommended)
- **CPU**: Multi-core processor recommended

## Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd ai_virtual_mouse
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

## Quick Start Guide

1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Grant Camera Permission**
   - Allow the application to access your webcam when prompted

3. **Position Your Hand**
   - Sit in front of your camera
   - Ensure adequate lighting
   - Keep your hand within the camera frame

4. **Calibrate**
   - Click "🎯 Calibrate Cursor" to set the cursor to center
   - This helps establish baseline coordinates

5. **Start Controlling**
   - Move your index finger to control cursor
   - Use gestures to click, scroll, and interact

## Supported Gestures

### Movement & Selection
| Gesture | Action | How to Perform |
|---------|--------|----------------|
| Index Finger Point | Move Cursor | Point index finger, keep others down |
| Index + Middle Together | Left Click | Bring index and middle fingertips close |
| Peace Sign (Spread) | Right Click | Index and middle up and spread apart |
| Thumb + Middle Touch | Double Click | Touch thumb tip to middle fingertip |

### Scrolling & Navigation
| Gesture | Action | How to Perform |
|---------|--------|----------------|
| All Fingers Up | Scroll Up | Open all fingers wide |
| Closed Fist | Scroll Down | Make a closed fist |
| Index Up + Others Down | Drag | Index extended, others closed |

### System Controls
| Gesture | Action | How to Perform |
|---------|--------|----------------|
| Thumb + Pinky | Volume Up | Only thumb and pinky extended |
| Thumb Only | Volume Down | Only thumb extended |

## Settings & Configuration

### Cursor Speed
Adjusts how far the cursor moves with your hand movement.
- **Range**: 0.5x - 2.0x
- **Default**: 1.0x
- **Tip**: Lower for precision, higher for larger movements

### Smoothing
Reduces jitter and makes cursor movement smoother.
- **Range**: 0.0 - 1.0
- **Default**: 0.7
- **Tip**: Higher values = smoother movement but slight lag

### Detection Confidence
Minimum confidence required for hand detection.
- **Range**: 0.3 - 0.9
- **Default**: 0.7
- **Tip**: Lower = more detections but more false positives

### Show Landmarks
Display hand joint positions on screen.
- Useful for debugging detection issues
- Toggle in settings panel

### Show FPS
Display frames per second counter.
- Helps monitor performance
- Toggle in settings panel

## Configuration File

Configuration is automatically saved to:
- **Windows**: `C:\Users\YourUsername\.virtual_mouse\config.json`
- **macOS**: `~/.virtual_mouse/config.json`
- **Linux**: `~/.virtual_mouse/config.json`

Edit this file to customize default settings:

```json
{
  "camera_index": 0,
  "camera_fps": 30,
  "cursor_speed": 1.0,
  "cursor_smoothing": 0.7,
  "detection_confidence": 0.7,
  "tracking_confidence": 0.5,
  "gesture_timeout": 0.3,
  "smoothing_window": 5,
  "theme": "dark",
  "show_fps": true,
  "show_landmarks": true,
  "screen_width": 1920,
  "screen_height": 1080,
  "calibrated": false
}
```

## Troubleshooting

### Hand Not Detected

**Problem**: Application doesn't detect your hand
- **Solution**: 
  - Improve lighting (avoid shadows)
  - Move closer to camera
  - Reduce background clutter
  - Ensure camera is clean
  - Lower detection confidence in settings

### Cursor Jittering

**Problem**: Cursor movement is jerky or unstable
- **Solution**:
  - Increase smoothing value
  - Improve lighting
  - Move more slowly and deliberately
  - Increase detection confidence

### Poor Gesture Recognition

**Problem**: Gestures not being recognized consistently
- **Solution**:
  - Calibrate cursor again
  - Adjust gesture timeout in advanced settings
  - Make gestures slower and more deliberate
  - Ensure adequate lighting
  - Check hand visibility to camera

### Low FPS / Lag

**Problem**: Application runs slowly
- **Solution**:
  - Close other demanding applications
  - Reduce camera resolution in settings
  - Lower detection confidence
  - Check CPU usage
  - Upgrade computer hardware if necessary

### Camera Not Working

**Problem**: "Failed to open camera" error
- **Solution**:
  - Check camera permissions (Windows/macOS/Linux)
  - Ensure camera is not in use by another application
  - Try different camera index in config.json (0, 1, 2, etc.)
  - Reinstall camera drivers
  - Restart application

### Mouse Control Not Working

**Problem**: Cursor moves but clicks don't work
- **Solution**:
  - Check if application has necessary permissions
  - Try running as administrator (Windows)
  - Disable gesture recognition timeout
  - Test with a different application (Notepad)

## Performance Optimization

### For Better Performance:

1. **Lighting**: Use consistent, bright lighting without shadows
2. **Camera**: Position camera at eye level, 60-90cm away
3. **Background**: Use plain, non-reflective background
4. **Hand Visibility**: Keep hand fully visible to camera
5. **Computer**: Close unnecessary applications
6. **Settings**: Balance sensitivity and accuracy

### FPS Guide:

- **30 FPS**: Optimal - smooth cursor movement
- **20-30 FPS**: Good - acceptable performance
- **15-20 FPS**: Fair - noticeable lag
- **Below 15 FPS**: Poor - significant delays

## Architecture

### Core Modules

```
core/
├── camera_manager.py      # Webcam capture & frame delivery
├── hand_detector.py       # MediaPipe-based hand detection
├── gesture_recognizer.py  # Gesture classification
├── cursor_controller.py   # Mouse control & actions
├── config_manager.py      # Settings management
└── engine.py              # Main processing engine

gui/
└── app.py                 # CustomTkinter GUI application
```

### Data Flow

```
Webcam
  ↓
CameraManager (capture frames)
  ↓
HandDetector (detect landmarks)
  ↓
GestureRecognizer (recognize gestures)
  ↓
CursorController (move mouse, perform actions)
  ↓
GUI (display feedback)
```

## Advanced Features

### Multi-Hand Support
The system can detect up to 2 hands simultaneously. The primary hand (usually right) is used for cursor control.

### Temporal Smoothing
Gestures are smoothed over multiple frames to reduce false positives and improve reliability.

### Confidence Scoring
Each gesture recognition includes a confidence score indicating reliability.

### Debouncing
Repeated gestures are debounced to prevent accidental double-triggers.

## Limitations

- Single monitor support (multi-monitor in development)
- Hand occlusion reduces accuracy
- Requires adequate lighting
- Works best with clear backgrounds
- Some gestures may be ambiguous

## Future Enhancements

- [ ] Multi-monitor support
- [ ] Custom gesture recording
- [ ] AI-based gesture training
- [ ] Voice commands integration
- [ ] Eye tracking support
- [ ] Gaming mode profiles
- [ ] Remote network control
- [ ] Cross-platform optimization

## License

MIT License - Feel free to use and modify

## Acknowledgments

- MediaPipe by Google for hand detection
- OpenCV for computer vision
- PyAutoGUI for mouse control
- CustomTkinter for modern GUI framework

## Support & Documentation

For issues, suggestions, or contributions:
- Check the logs in `virtual_mouse.log`
- Review troubleshooting section above
- Consult advanced settings documentation

## Version History

### v1.0.0 (Current)
- Initial release
- 14 gesture types supported
- Real-time hand detection
- Modern GUI interface
- Configurable settings
- Cross-platform support

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Disclaimer

This application requires webcam access and monitors hand movements. Ensure you have proper permissions and privacy considerations in place. The application does not store or transmit video data beyond the local machine.

---

**Enjoy gesture-based control! Happy clicking! 🖱️👋**
