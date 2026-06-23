# Quick Start Guide

Get up and running with AI Virtual Mouse in minutes!

## System Requirements

- **Python**: 3.11 or higher
- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: 4GB minimum
- **Webcam**: Standard USB or built-in camera

## Installation (5 minutes)

### Option 1: Windows (Easiest)

1. **Download and unzip** the project
2. **Double-click** `run.bat`
3. **Wait** for dependencies to install (first time only)
4. **Allow** webcam access when prompted
5. **Done!** The app should start automatically

### Option 2: macOS/Linux

1. **Open Terminal** in the project directory
2. **Run**: `chmod +x run.sh && ./run.sh`
3. **Allow** webcam access when prompted
4. **Done!** The app should start

### Option 3: Manual Installation

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py
```

## First Time Setup

1. **Launch the application**
   - Windows: Double-click `run.bat`
   - macOS/Linux: Run `./run.sh`

2. **Grant Camera Permission**
   - Click "Allow" when prompted by your OS

3. **Position yourself**
   - Sit 60-90cm in front of camera
   - Ensure good lighting (no shadows on hand)
   - Keep hand fully visible

4. **Click "🎯 Calibrate Cursor"**
   - This sets baseline coordinates

5. **Start using gestures!**

## Basic Gestures (Learn These First)

### Move Cursor
```
Point your index finger
Other fingers closed
```

### Left Click
```
Index + Middle fingertips together
Like pressing a button
```

### Scroll Down
```
Close all fingers (fist)
```

### Scroll Up
```
Open all fingers wide
```

## Troubleshooting First Run

### "Camera not found"
- Check camera is connected
- Try different USB port
- Allow camera permissions in Settings
- Restart application

### "Hand not detected"
- Improve lighting
- Move closer to camera
- Reduce background clutter
- Wear contrasting sleeve (light/dark hand)

### "Cursor jumps around"
- Increase smoothing slider
- Improve lighting
- Move more slowly
- Adjust cursor speed slider

## Basic Settings

All settings are in the right panel:

**Cursor Speed**: How far cursor moves
- Start: 1.0x (default)
- Too slow? Increase to 1.5x
- Too fast? Decrease to 0.5x

**Smoothing**: Reduce jitter
- Start: 0.7 (default)
- Too jumpy? Increase to 0.9
- Too laggy? Decrease to 0.5

**Detection Confidence**: Hand detection strictness
- Start: 0.7 (default)
- Missing detections? Lower to 0.5
- Too many false positives? Increase to 0.8

## Common Tasks

### Control Volume
- **Volume Up**: Thumb + Pinky extended
- **Volume Down**: Thumb only
- **Test**: Open Settings → Sound to verify

### Navigate Browser
- **Scroll**: Scroll up/down with fist/open-hand gesture
- **Click links**: Left-click gesture on link
- **Go back**: Right-click gesture for context menu

### Control Presentation
- **Move to next slide**: Use scroll down gesture
- **Move to previous slide**: Use scroll up gesture
- **Click slides**: Use left-click gesture

### Basic Accessibility
- Use as primary mouse on keyboard
- Combine with keyboard shortcuts (Alt+Tab, Win+D)
- Click UI elements without touching screen

## Performance Tips

1. **Better Detection**: Clean camera lens
2. **Smoother Movement**: Increase smoothing value
3. **Lower Lag**: Reduce smoothing window (advanced settings)
4. **Better Accuracy**: Improve lighting conditions
5. **Higher FPS**: Close other applications

## Keyboard Shortcuts

While application is running:
- **ESC**: Pause/resume tracking
- **Q**: Open settings (within app)
- **H**: Show help window
- **C**: Calibrate cursor

## Next Steps

1. **Practice gestures**: Get comfortable with basic gestures
2. **Adjust settings**: Fine-tune for your setup
3. **Explore advanced settings**: Click "⚙️ Settings" button
4. **Read full README.md**: For detailed documentation
5. **Check DEVELOPER.md**: If you want to extend functionality

## Helpful Tips

✅ **Do:**
- Practice in good lighting
- Position camera at eye level
- Keep hand steady when clicking
- Move smoothly and deliberately
- Take breaks to prevent fatigue

❌ **Don't:**
- Use in low light
- Have cluttered background
- Wave hand erratically
- Move camera during use
- Cover camera lens

## Need Help?

1. **Check README.md** - Full documentation
2. **Run test_suite.py** - Test components
   ```bash
   python test_suite.py
   ```
3. **Check virtual_mouse.log** - Error details
4. **See DEVELOPER.md** - Technical details

## Uninstall

Just delete the project folder. No system files are modified.

Configuration files stored at:
- **Windows**: `C:\Users\YourName\.virtual_mouse`
- **macOS**: `~/.virtual_mouse`
- **Linux**: `~/.virtual_mouse`

## Enjoy! 🎉

You're now ready to control your computer with hand gestures!

---

**Pro Tip**: Once you're comfortable, try these advanced features:
- Use drag gestures for drawing
- Combine with keyboard for gaming
- Set up custom shortcuts in settings
- Practice with different hand positions

Happy gesturing! 👋
