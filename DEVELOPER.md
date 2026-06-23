# Developer Documentation

## Project Architecture

### Overview

The Virtual Mouse application follows a modular, layered architecture designed for maintainability, extensibility, and testability.

```
┌─────────────────────────────────────────┐
│        GUI Layer (CustomTkinter)        │
└─────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────┐
│      Engine Layer (VirtualMouseEngine)  │
│  - Orchestrates all components         │
│  - Manages data flow                   │
│  - Handles state                       │
└─────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────┐
│         Core Processing Modules         │
├─────────────────────────────────────────┤
│ • CameraManager       - Video capture  │
│ • HandDetector        - Detection      │
│ • GestureRecognizer   - Recognition    │
│ • CursorController    - Action         │
│ • ConfigManager       - Settings       │
└─────────────────────────────────────────┘
```

### Core Modules

#### 1. CameraManager (`core/camera_manager.py`)

**Purpose**: Handles webcam capture and frame delivery

**Key Features**:
- Multi-threaded frame capture
- Configurable resolution and FPS
- Frame queue for optimal performance
- Error handling for camera disconnection

**Usage**:
```python
from core import CameraManager

camera = CameraManager(camera_index=0, target_fps=30)
camera.initialize()
camera.start()

frame = camera.get_frame()
camera.stop()
```

**Extension Points**:
- Support for multiple cameras
- Custom frame processing
- Video file input instead of webcam

#### 2. HandDetector (`core/hand_detector.py`)

**Purpose**: Detects and tracks hand landmarks using MediaPipe

**Key Features**:
- Real-time hand landmark detection
- Support for multiple hands
- Handedness classification (Left/Right)
- Visualization utilities

**Data Structure** - HandLandmarks:
```python
@dataclass
class HandLandmarks:
    landmarks: list        # 21 landmarks [x, y, z]
    handedness: str        # "Left" or "Right"
    confidence: float      # Detection confidence
    hand_id: int          # Hand index
```

**Landmark Points** (0-20):
```
0:  Wrist
1:  Thumb CMC
2:  Thumb MCP
3:  Thumb IP
4:  Thumb Tip
5:  Index Finger MCP
6:  Index Finger PIP
7:  Index Finger DIP
8:  Index Finger Tip (used for cursor)
9:  Middle Finger MCP
...
20: Pinky Tip
```

**Usage**:
```python
from core import HandDetector

detector = HandDetector()
hands = detector.detect(frame)

for hand in hands:
    print(f"Hand: {hand.handedness}")
    print(f"Landmarks: {hand.landmarks}")
```

**Extension Points**:
- Custom landmark filtering
- Pose refinement
- Additional hand metrics

#### 3. GestureRecognizer (`core/gesture_recognizer.py`)

**Purpose**: Recognizes hand gestures from landmarks

**Supported Gestures**:
```python
class GestureType(Enum):
    NONE = "none"
    MOVE = "move"
    LEFT_CLICK = "left_click"
    RIGHT_CLICK = "right_click"
    DOUBLE_CLICK = "double_click"
    DRAG = "drag"
    SCROLL_UP = "scroll_up"
    SCROLL_DOWN = "scroll_down"
    VOLUME_UP = "volume_up"
    VOLUME_DOWN = "volume_down"
    BRIGHTNESS_UP = "brightness_up"
    BRIGHTNESS_DOWN = "brightness_down"
    PAUSE = "pause"
    SCREENSHOT = "screenshot"
```

**Algorithm**:
1. Extract finger extension state
2. Calculate distances and angles
3. Match patterns to gestures
4. Apply temporal smoothing
5. Debounce repeated gestures

**Usage**:
```python
from core import GestureRecognizer

recognizer = GestureRecognizer()
gesture, confidence, hand_idx = recognizer.recognize(hands)

if gesture == GestureType.LEFT_CLICK:
    print("Performing left click")
```

**Adding New Gestures**:
1. Add gesture type to `GestureType` enum
2. Implement recognition logic in `_recognize_gesture()`
3. Add handler in engine's `_execute_gesture()`

Example:
```python
# In _recognize_gesture()
# Pinky extended, others closed
if pinky_extended and not thumb_extended and not index_extended:
    return GestureType.CUSTOM_GESTURE, 0.8
```

#### 4. CursorController (`core/cursor_controller.py`)

**Purpose**: Controls mouse cursor and performs actions

**Key Features**:
- Smooth cursor movement with exponential smoothing
- Screen boundary clamping
- Mouse actions (click, drag, scroll)
- Calibration support

**Actions Available**:
- `move_cursor()` - Move to position
- `left_click()` - Single left click
- `right_click()` - Single right click
- `double_click()` - Double left click
- `scroll()` - Scroll up/down
- `start_drag()` / `end_drag()` - Drag operations
- `calibrate()` - Reset to screen center

**Usage**:
```python
from core import CursorController

controller = CursorController(smoothing_factor=0.7)
controller.move_cursor(landmarks, cam_width, cam_height, sensitivity=1.0)
controller.left_click()
```

**Extending Mouse Actions**:
```python
def custom_action(self):
    """Custom action implementation"""
    try:
        # Your action code here
        pyautogui.hotkey('alt', 'tab')
    except Exception as e:
        logger.error(f"Custom action error: {e}")
```

#### 5. ConfigManager (`core/config_manager.py`)

**Purpose**: Manages application configuration and persistence

**Configuration Structure**:
```python
@dataclass
class Config:
    camera_index: int = 0
    camera_fps: int = 30
    cursor_speed: float = 1.0
    cursor_smoothing: float = 0.7
    detection_confidence: float = 0.7
    tracking_confidence: float = 0.5
    gesture_timeout: float = 0.3
    smoothing_window: int = 5
    # ... more settings
```

**Usage**:
```python
from core import ConfigManager

config_mgr = ConfigManager()
config = config_mgr.get_config()

config_mgr.update(cursor_speed=1.5)
config_mgr.save()
```

#### 6. VirtualMouseEngine (`core/engine.py`)

**Purpose**: Main orchestration engine

**Responsibilities**:
- Initialize all components
- Manage processing loop
- Execute gestures
- Handle configuration updates
- Provide status information

**Usage**:
```python
from core import VirtualMouseEngine

engine = VirtualMouseEngine()
engine.initialize()

frame, results = engine.process_frame()

engine.shutdown()
```

### GUI Layer

The GUI is built with CustomTkinter for a modern, native look.

**Components**:
- Video display with FPS counter
- Real-time status indicators
- Interactive settings panel
- Gesture information display
- Help and documentation

**Key Classes**:
- `VirtualMouseApp` - Main application window

**Extensible Areas**:
- Add new status displays
- Customize theme colors
- Add new setting controls
- Implement additional windows

### Data Flow

```
Main Loop:
  1. Capture frame (CameraManager)
  2. Detect hands (HandDetector)
  3. Recognize gesture (GestureRecognizer)
  4. Execute action (CursorController)
  5. Update GUI (VirtualMouseApp)
  6. Return to step 1
```

## Development Guide

### Adding a New Gesture

1. **Define gesture type** in `core/gesture_recognizer.py`:
```python
class GestureType(Enum):
    MY_GESTURE = "my_gesture"
```

2. **Implement recognition** in `GestureRecognizer._recognize_gesture()`:
```python
# Check for specific finger configuration
if index_extended and middle_extended and ring_extended:
    return GestureType.MY_GESTURE, 0.8
```

3. **Add action handler** in `core/engine.py`:
```python
elif gesture == GestureType.MY_GESTURE:
    self._execute_my_gesture()
```

4. **Implement action**:
```python
def _execute_my_gesture(self):
    """Handle my gesture"""
    # Your implementation
```

5. **Update UI documentation** in `gui/app.py`:
```python
gesture_info = """
My Gesture → Does something cool
"""
```

### Creating a Plugin/Extension

1. **Create new module** in appropriate directory:
```python
# plugins/my_plugin.py
class MyPlugin:
    def __init__(self, engine):
        self.engine = engine

    def process(self, gesture, hands):
        # Your processing
        pass
```

2. **Integrate with engine**:
```python
# In engine.py
from plugins import MyPlugin

self.plugins = [MyPlugin(self)]

# In _execute_gesture()
for plugin in self.plugins:
    plugin.process(gesture, self.current_hands)
```

### Testing

Run the test suite:
```bash
python test_suite.py
```

Tests include:
- Camera functionality
- Hand detection
- Gesture recognition
- Performance metrics

### Performance Optimization

**Bottlenecks to watch**:
1. Frame capture - Keep buffer small
2. Hand detection - MediaPipe is optimized
3. Gesture recognition - Add early termination
4. GUI rendering - Limit update frequency

**Optimization techniques**:
```python
# Use frame skipping
if self.frame_count % 2 == 0:
    process_frame()

# Limit gesture checking
if hand_confidence > threshold:
    recognize_gesture()

# Cache expensive calculations
if cache_valid:
    use_cached_result()
```

## API Reference

### Core Classes

#### CameraManager
- `initialize()` → bool
- `start()` → None
- `stop()` → None
- `get_frame()` → numpy.ndarray
- `get_resolution()` → tuple
- `get_fps()` → int

#### HandDetector
- `detect(frame)` → List[HandLandmarks]
- `draw_landmarks(frame, hands)` → numpy.ndarray

#### GestureRecognizer
- `recognize(hands)` → (GestureType, float, int)
- `reset()` → None

#### CursorController
- `move_cursor(landmarks, width, height, sensitivity)` → tuple
- `left_click()` → None
- `right_click()` → None
- `double_click()` → None
- `scroll(direction, amount)` → None
- `start_drag()` → None
- `end_drag()` → None
- `calibrate()` → tuple

#### ConfigManager
- `load()` → None
- `save()` → bool
- `get(key, default)` → Any
- `update(**kwargs)` → bool
- `reset()` → None

## Troubleshooting Development Issues

### Hand Detection Not Working
- Ensure MediaPipe is properly installed
- Check camera permissions
- Verify lighting conditions
- Test with `test_suite.py`

### Gesture Recognition Issues
- Print landmarks to verify data
- Adjust thresholds in gesture recognizer
- Use debug mode in GUI
- Check temporal smoothing window

### Performance Issues
- Profile with `cProfile`
- Check FPS counter
- Reduce detection confidence threshold
- Lower camera resolution

### GUI Issues
- Verify CustomTkinter installation
- Check Pillow for image handling
- Test on different scales (DPI)
- Use CustomTkinter scaling

## Contributing

When contributing:
1. Follow existing code style
2. Add docstrings to functions
3. Include error handling
4. Test thoroughly
5. Update documentation
6. Submit pull request

## Future Improvements

- [ ] Multi-monitor support
- [ ] Custom gesture recording
- [ ] AI-based gesture learning
- [ ] Performance optimization
- [ ] Cross-platform testing
- [ ] Accessibility features
- [ ] Network sharing
- [ ] Mobile companion app

---

Happy developing! 🚀
