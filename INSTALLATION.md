# GestureMouse Installation Guide

## Quick Start

### 1. Prerequisites

Make sure you have Python 3.10 or higher installed:
```bash
python --version
```

### 2. Install Dependencies

Navigate to the project directory and install required packages:

```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues with MediaPipe or OpenCV, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### 3. Run the Application

Simply run:
```bash
python run.py
```

Or:
```bash
python src/main.py
```

## Platform-Specific Instructions

### Windows

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. Open Command Prompt or PowerShell
3. Navigate to the project folder
4. Run:
   ```cmd
   pip install -r requirements.txt
   python run.py
   ```

**Note:** On Windows, you may need to allow camera permissions in Windows Settings > Privacy > Camera.

### macOS

1. Install Python 3.10+ (recommended via Homebrew):
   ```bash
   brew install python@3.10
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python3 run.py
   ```

**Important:** macOS requires accessibility permissions for mouse control:
- Go to System Preferences > Security & Privacy > Privacy > Accessibility
- Add Terminal or your Python executable to the list

### Linux (Ubuntu/Debian)

1. Install system dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-tk
   ```

2. Install Python packages:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python3 run.py
   ```

## Troubleshooting

### Camera Not Working

**Windows:**
- Check Windows Settings > Privacy > Camera
- Ensure "Allow apps to access your camera" is ON
- Allow the specific app to access camera

**macOS:**
- Check System Preferences > Security & Privacy > Camera
- Grant permission to Terminal or Python

**Linux:**
- Check if your user is in the `video` group:
  ```bash
  sudo usermod -a -G video $USER
  ```
- Log out and log back in

### ModuleNotFoundError

If you get `ModuleNotFoundError: No module named 'mediapipe'` or similar:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### PyAutoGUI Not Working

**macOS:** Grant accessibility permissions as mentioned above.

**Linux:** Install additional dependencies:
```bash
sudo apt install python3-tk python3-dev
```

### Qt Platform Plugin Error

If you get "qt.qpa.plugin: Could not load the Qt platform plugin" error:

**Linux:**
```bash
sudo apt install libxcb-xinerama0 libxcb-cursor0
```

### MediaPipe Import Error

If MediaPipe fails to import, try:
```bash
pip uninstall mediapipe
pip install mediapipe --no-cache-dir
```

## Virtual Environment (Recommended)

Using a virtual environment helps isolate dependencies:

### Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install and Run

```bash
pip install -r requirements.txt
python run.py
```

### Deactivate

```bash
deactivate
```

## Verifying Installation

Run this test script to verify all components:

```python
# test_installation.py
import sys

def test_imports():
    packages = {
        'cv2': 'OpenCV',
        'mediapipe': 'MediaPipe',
        'PyQt6': 'PyQt6',
        'pyautogui': 'PyAutoGUI',
        'numpy': 'NumPy',
        'PIL': 'Pillow'
    }
    
    print("Testing package imports...")
    all_ok = True
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name} - OK")
        except ImportError as e:
            print(f"✗ {name} - FAILED: {e}")
            all_ok = False
    
    if all_ok:
        print("\n✓ All packages installed successfully!")
    else:
        print("\n✗ Some packages failed to import. Please reinstall.")
    
    return all_ok

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
```

Save as `test_installation.py` and run:
```bash
python test_installation.py
```

## Next Steps

Once installed successfully:
1. Run `python run.py`
2. Click "Start Tracking"
3. Position your hand in front of the camera
4. Try the gestures:
   - Point with index finger → Move cursor
   - Pinch thumb + index → Click
   - Two fingers + move → Scroll

Enjoy GestureMouse! 🎉
