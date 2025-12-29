# GestureMouse User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Understanding the Interface](#understanding-the-interface)
3. [Gestures Guide](#gestures-guide)
4. [Settings & Customization](#settings--customization)
5. [Tips & Best Practices](#tips--best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Launch

1. **Run the application:**
   ```bash
   python run.py
   ```

2. **Grant camera permissions** when prompted by your operating system

3. **Position yourself:**
   - Sit comfortably in front of your webcam
   - Ensure your face and upper body are well-lit
   - Keep your hand visible in the camera frame

4. **Click "Start Tracking"** to begin

---

## Understanding the Interface

### Main Window Components

#### Camera Feed
- **Location:** Left side of the window
- **Purpose:** Shows live camera feed with hand landmarks overlay
- **What you'll see:** Green dots and lines showing detected hand joints

#### Status Panel
- **Tracking Status:** Shows if tracking is active (green) or stopped (red)
- **Hand Detected:** Indicates if your hand is visible
- **Active Gesture:** Shows current gesture being performed
- **FPS:** Frames per second (should be 20-30 for smooth operation)

#### Gestures Panel
- Checkboxes to enable/disable specific gestures
- Useful if you want to use only certain features

#### Settings Panel
- **Sensitivity:** How fast the cursor moves (1=slow, 10=fast)
- **Smoothing:** How smooth cursor movement is (1=responsive, 10=smooth)
- **Camera:** Select which camera to use (if multiple available)

---

## Gestures Guide

### 1. Cursor Control (Move Mouse)

**How to perform:**
- Extend your **index finger** (point)
- Keep other fingers closed (make a fist)
- Move your hand to control cursor

**Tips:**
- Use small, smooth movements
- Keep hand at comfortable distance from camera
- Adjust sensitivity if cursor moves too fast/slow

**Visual:**
```
     ☝️  ← Index finger extended
    ✊   ← Other fingers closed
```

---

### 2. Left Click

**How to perform:**
- Bring your **thumb** and **index finger** together (pinch gesture)
- Touch them briefly and release

**Tips:**
- No need to hold the pinch
- Quick pinch works best
- Increase click debounce time if getting accidental clicks

**Visual:**
```
    🤏  ← Thumb + Index pinch
```

---

### 3. Right Click

**How to perform:**
- Bring your **thumb** and **middle finger** together
- Pinch and release

**Tips:**
- Similar to left click but with middle finger
- Useful for context menus

**Visual:**
```
    👌  ← Thumb + Middle pinch
```

---

### 4. Scroll

**How to perform:**
1. Extend **index** and **middle** fingers (peace sign ✌️)
2. Keep other fingers closed
3. Move hand **up** to scroll up, **down** to scroll down

**Tips:**
- Use smooth vertical movements
- Adjust scroll sensitivity if scrolling too fast/slow
- Keep fingers clearly separated

**Visual:**
```
    ✌️  ← Two fingers extended
    ↕️  ← Move up/down to scroll
```

---

## Settings & Customization

### Sensitivity (1-10)

**What it does:** Controls cursor movement speed

- **Low (1-3):** Precise control, slower movement
  - *Best for:* Detailed work, small targets
  
- **Medium (4-6):** Balanced speed and control
  - *Best for:* General use (recommended)
  
- **High (7-10):** Fast movement, less precise
  - *Best for:* Large screens, quick navigation

### Smoothing (1-10)

**What it does:** Reduces cursor jitter

- **Low (1-3):** More responsive, may be jittery
  - *Best for:* Quick actions, gaming
  
- **Medium (4-6):** Balanced smoothness
  - *Best for:* General use (recommended)
  
- **High (7-10):** Very smooth, slightly delayed
  - *Best for:* Presentations, smooth movements

### Gesture Enable/Disable

Toggle individual gestures on/off:
- Disable gestures you don't use
- Prevent accidental triggers
- Customize your workflow

---

## Tips & Best Practices

### Lighting
✓ **Good:** Bright, even lighting from front or sides  
✗ **Bad:** Backlit (window behind you), very dim rooms

### Camera Position
✓ **Good:** Eye level, 1-2 feet away, stable mount  
✗ **Bad:** Too close, shaky, extreme angles

### Hand Position
✓ **Good:** Within camera frame, palm facing camera  
✗ **Bad:** Partially visible, sideways, moving too fast

### Environment
✓ **Good:** Simple background, stable position  
✗ **Bad:** Busy background, constant movement behind you

### Performance Tips
1. **Close unused applications** to reduce CPU usage
2. **Use lower camera resolution** if experiencing lag
3. **Ensure good lighting** for better detection
4. **Keep background simple** for more reliable tracking

---

## Troubleshooting

### "Hand Not Detected"

**Possible causes & solutions:**

1. **Poor lighting**
   - Solution: Increase room lighting or move closer to light source

2. **Hand outside frame**
   - Solution: Move hand into camera view

3. **Hand too close/far**
   - Solution: Position hand 1-2 feet from camera

4. **Background too busy**
   - Solution: Move to simpler background or adjust camera angle

### "Cursor Too Jittery"

**Solutions:**
1. Increase **Smoothing** slider value
2. Ensure stable lighting (avoid flickering lights)
3. Keep hand steady while moving
4. Reduce camera exposure in camera settings

### "Cursor Moves Too Slow/Fast"

**Solutions:**
1. Adjust **Sensitivity** slider
2. Move hand closer/farther from camera
3. Use smaller/larger hand movements

### "Accidental Clicks"

**Solutions:**
1. Disable unwanted gestures in Gestures panel
2. Increase click debounce time in config
3. Make more deliberate pinch gestures
4. Keep fingers separated when not clicking

### "Low FPS / Laggy"

**Solutions:**
1. Close other applications
2. Reduce camera resolution
3. Disable visual effects in UI settings
4. Check CPU usage (should be <25%)

### "Application Crashes"

**Solutions:**
1. Update all dependencies: `pip install -r requirements.txt --upgrade`
2. Check camera is not in use by other apps
3. Restart the application
4. Check logs for error messages

---

## Keyboard Shortcuts

*(To be implemented in future versions)*

- `Ctrl+P` - Pause/Resume tracking
- `Ctrl+H` - Hide/Show window
- `Ctrl+Q` - Quit application
- `Ctrl+R` - Reset settings to defaults

---

## Advanced Usage

### System Tray

When minimized to tray, you can:
- **Double-click icon** - Show window
- **Right-click icon** - Access menu
  - Pause/Resume tracking
  - Show window
  - Exit application

### Configuration File

Settings are saved in `config.json`:
- Edit manually for advanced customization
- Backup/restore settings by copying this file
- Share settings with other users

---

## Getting Help

If you encounter issues not covered in this guide:

1. Check the **Troubleshooting** section above
2. Review the **INSTALLATION.md** for setup issues
3. Check application logs for error messages
4. Open an issue on GitHub with:
   - Description of the problem
   - Steps to reproduce
   - System information (OS, Python version)
   - Error messages or logs

---

**Enjoy using GestureMouse! 🎉**

For more information, visit the [GitHub repository](https://github.com/yourusername/gesturemouse).
