# GestureMouse

Control your computer mouse using hand gestures detected through your webcam!

## Features

- 🖱️ **Cursor Control** - Move your mouse by pointing with your index finger
- 🤏 **Click Gestures** - Left and right click using pinch gestures
- 📜 **Scroll** - Scroll using two-finger movements
- ⚙️ **Customizable** - Adjust sensitivity, smoothing, and gesture thresholds
- 🔒 **Privacy First** - All processing happens locally, no cloud uploads

## Installation

### Prerequisites

- Python 3.10 or higher
- Webcam (720p @ 30fps recommended)
- Windows 10/11, macOS 10.14+, or Ubuntu 20.04+

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gesturemouse.git
cd gesturemouse
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## Quick Start

1. Launch GestureMouse
2. Allow camera permissions when prompted
3. Position your hand in front of the webcam
4. Use these gestures:
   - **Point with index finger** → Move cursor
   - **Pinch thumb + index** → Left click
   - **Two fingers extended + move** → Scroll

## Gestures Guide

| Gesture | Action |
|---------|--------|
| Index finger extended | Move cursor |
| Thumb-Index pinch | Left click |
| Thumb-Middle pinch | Right click |
| Two fingers + vertical movement | Scroll |

## Configuration

Access settings through the main window to adjust:
- Cursor sensitivity (1-10)
- Smoothing factor (1-10)
- Gesture thresholds
- Camera selection

## System Requirements

**Minimum:**
- CPU: Intel i3 8th gen or equivalent
- RAM: 4GB
- Webcam: 720p @ 30fps

**Recommended:**
- CPU: Intel i5 10th gen or equivalent
- RAM: 8GB
- Webcam: 1080p @ 30fps

## Privacy & Security

- ✅ All video processing happens locally on your device
- ✅ No recording or storage of video feed
- ✅ No internet connection required
- ✅ No data collection or telemetry

## Troubleshooting

**Hand not detected?**
- Ensure good lighting conditions
- Keep hand within camera frame
- Try adjusting camera position

**Cursor movement jittery?**
- Increase smoothing factor in settings
- Ensure stable lighting
- Reduce background complexity

**Gestures not responding?**
- Recalibrate using the Calibration Wizard
- Check gesture enable/disable toggles
- Adjust gesture thresholds in settings

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## Support

For issues and feature requests, please open an issue on GitHub.
