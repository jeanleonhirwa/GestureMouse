# Product Requirements Document: GestureMouse

## 1. Executive Summary

**Product Name:** GestureMouse  
**Version:** 1.0  
**Date:** December 29, 2025  
**Document Owner:** Development Team

### 1.1 Product Vision
GestureMouse is a desktop application that transforms any standard webcam into a touchless input device, enabling users to control their computer mouse cursor, perform clicks, scroll, and zoom using hand gestures and finger movements detected through computer vision.

### 1.2 Target Audience
- Professionals giving presentations
- Users with mobility impairments seeking alternative input methods
- Touch-free computing enthusiasts
- Content creators and designers seeking innovative workflows
- Users in sterile environments (medical, laboratory, kitchen)

---

## 2. Product Overview

### 2.1 Core Value Proposition
- **Touchless Control:** Control your computer without physical contact with input devices
- **Accessibility:** Alternative input method for users with limited mobility
- **Convenience:** No additional hardware required beyond a standard webcam
- **Hygiene:** Ideal for environments where touching devices is impractical

### 2.2 Key Features

#### Phase 1 - MVP (Minimum Viable Product)
1. **Cursor Movement:** Move mouse cursor by tracking index finger position
2. **Left Click:** Pinch gesture (thumb + index finger)
3. **Right Click:** Two-finger pinch or extended gesture
4. **Scroll:** Two-finger vertical movement
5. **Settings Panel:** Calibration, sensitivity, and gesture customization
6. **System Tray Integration:** Quick enable/disable functionality

#### Phase 2 - Enhanced Features (Future)
- Zoom gesture (pinch in/out with two hands)
- Drag and drop functionality
- Multi-monitor support
- Gesture recording and custom macros
- Voice command integration

---

## 3. Technical Specifications

### 3.1 Technology Stack

#### **Frontend/UI Framework**
- **Python 3.10+** - Primary language
- **PyQt6** or **Tkinter** - GUI framework
  - *Recommendation:* PyQt6 for modern, responsive UI
  - Reason: Better styling, threading support, system tray integration

#### **Computer Vision & Hand Tracking**
- **MediaPipe (Google)** - Hand landmark detection
  - Version: 0.10.9+
  - Provides 21 3D hand landmarks per hand
  - Real-time performance (30+ FPS)
  - Cross-platform support
- **OpenCV (cv2)** - Video capture and image processing
  - Version: 4.8+
  - Webcam interface and frame processing

#### **Mouse Control**
- **PyAutoGUI** - Cross-platform mouse/keyboard automation
  - Version: 0.9.54+
  - Handles screen coordinates and click events
- **pynput** (Alternative/Backup)
  - More granular control over input events

#### **Additional Libraries**
- **NumPy** - Mathematical operations on landmark coordinates
- **Pillow (PIL)** - Image processing for UI elements
- **threading/asyncio** - Concurrent video processing and UI updates

### 3.2 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GestureMouse Application                 │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   UI Layer   │  │ Settings Mgr │  │  System Tray    │  │
│  │  (PyQt6)     │  │              │  │   Integration   │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬────────┘  │
│         │                  │                    │            │
│  ┌──────┴──────────────────┴────────────────────┴────────┐ │
│  │            Application Controller                      │ │
│  │         (Main Loop & Event Coordination)               │ │
│  └──────┬──────────────────────┬─────────────────────────┘ │
│         │                      │                             │
│  ┌──────┴───────┐      ┌──────┴───────────┐                │
│  │ Video Input  │      │ Gesture Processor │                │
│  │   Module     │      │                   │                │
│  │  (OpenCV)    │      │  (MediaPipe +     │                │
│  │              │──────│   Custom Logic)   │                │
│  └──────────────┘      └──────┬────────────┘                │
│                               │                              │
│                        ┌──────┴────────┐                     │
│                        │ Mouse Control │                     │
│                        │ (PyAutoGUI)   │                     │
│                        └───────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Core Modules

#### **Module 1: VideoCapture**
```python
Responsibilities:
- Initialize webcam connection
- Capture frames at 30 FPS minimum
- Handle camera disconnection/reconnection
- Provide frame preprocessing (resize, flip)

Key Classes:
- CameraManager
- FrameBuffer
```

#### **Module 2: HandTracker**
```python
Responsibilities:
- Detect hands in video frames
- Extract 21 landmark points per hand
- Calculate hand metrics (distances, angles)
- Track hand state over time

Key Classes:
- HandDetector (MediaPipe wrapper)
- HandLandmarks
- HandMetrics

Hand Landmarks (MediaPipe):
0:  Wrist
1-4:  Thumb (CMC, MCP, IP, Tip)
5-8:  Index finger (MCP, PIP, DIP, Tip)
9-12: Middle finger
13-16: Ring finger
17-20: Pinky finger
```

#### **Module 3: GestureRecognizer**
```python
Responsibilities:
- Analyze hand landmarks to detect gestures
- Implement gesture state machines
- Debounce gesture detection
- Calculate gesture confidence scores

Key Classes:
- GestureDetector
- GestureState
- GestureFilter

Gestures to Implement:
1. Cursor Control: Index finger extended, others closed
2. Left Click: Thumb-Index pinch (distance < threshold)
3. Right Click: Thumb-Middle pinch OR hold pinch 1s
4. Scroll Mode: Index + Middle fingers extended
5. Scroll: Two-finger vertical movement in scroll mode
6. Drag: Pinch + hold + move
```

#### **Module 4: MouseController**
```python
Responsibilities:
- Map hand coordinates to screen coordinates
- Smooth cursor movement (exponential smoothing)
- Execute click/scroll/drag actions
- Handle multi-monitor scenarios

Key Classes:
- CursorMapper
- SmoothingFilter
- ActionExecutor
```

#### **Module 5: ConfigurationManager**
```python
Responsibilities:
- Load/save user settings
- Manage calibration data
- Handle default configurations

Settings to Store:
- Sensitivity (cursor speed multiplier)
- Smoothing factor (0.0-1.0)
- Gesture thresholds
- Camera selection
- Active area boundaries
- Gesture enable/disable flags
```

### 3.4 Gesture Detection Algorithms

#### **Cursor Movement**
```
Algorithm:
1. Detect hand with index finger extended
2. Get index finger tip coordinates (landmark #8)
3. Normalize coordinates to [0, 1] range
4. Apply smoothing: 
   smoothed_x = alpha * current_x + (1-alpha) * previous_x
5. Map to screen coordinates considering sensitivity
6. Move cursor with PyAutoGUI
```

#### **Pinch Detection (Clicks)**
```
Algorithm:
1. Calculate Euclidean distance between thumb tip (#4) and index tip (#8)
2. Normalize distance by hand size (wrist to middle finger MCP)
3. If distance < pinch_threshold (default: 0.05):
   - State = PINCHED
4. On transition from NOT_PINCHED → PINCHED:
   - Trigger click event
5. Debounce: Minimum 300ms between clicks
```

#### **Scroll Detection**
```
Algorithm:
1. Detect if index (#8) and middle (#12) finger tips both extended
2. Calculate vertical movement of midpoint between two fingers
3. If movement > threshold:
   - scroll_amount = delta_y * scroll_sensitivity
   - Execute scroll with PyAutoGUI
4. Low-pass filter to reduce jitter
```

### 3.5 Performance Requirements

- **Latency:** < 100ms from gesture to action
- **Frame Rate:** 30 FPS minimum for smooth tracking
- **CPU Usage:** < 25% on modern processors (Intel i5 8th gen+)
- **Memory:** < 200MB RAM usage
- **Accuracy:** 95%+ gesture recognition accuracy in good lighting

---

## 4. User Interface Design

### 4.1 Main Window

```
┌────────────────────────────────────────────────────────┐
│  GestureMouse                                    [_][□][×] │
├────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐  ┌──────────────────┐   │
│  │                          │  │  Status          │   │
│  │   Live Camera Feed       │  │  ● Tracking      │   │
│  │   (640x480)              │  │                  │   │
│  │   [Shows hand overlay]   │  │  Hand Detected:  │   │
│  │                          │  │  ✓ Yes           │   │
│  │                          │  │                  │   │
│  │                          │  │  Active Gesture: │   │
│  │                          │  │  → Cursor Move   │   │
│  └──────────────────────────┘  └──────────────────┘   │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │ Gestures                                        │   │
│  │  ☑ Cursor Control    ☑ Left Click              │   │
│  │  ☑ Right Click       ☑ Scrolling               │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │ Settings                                        │   │
│  │  Sensitivity:  [═════●════] 5                   │   │
│  │  Smoothing:    [══●═══════] 3                   │   │
│  │  Camera:       [Integrated Webcam     ▼]        │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│         [Calibrate]  [Advanced Settings]               │
│                                                         │
│         [Start Tracking]  [Minimize to Tray]           │
└────────────────────────────────────────────────────────┘
```

### 4.2 System Tray Interface

```
┌─────────────────────────┐
│ GestureMouse            │
├─────────────────────────┤
│ ● Tracking Active       │
│                         │
│ ▸ Pause Tracking        │
│ ▸ Show Window           │
│ ▸ Settings              │
│ ▸ Exit                  │
└─────────────────────────┘
```

### 4.3 Calibration Wizard

```
Step 1: Position your hand in the center of the frame
Step 2: Move your hand to each corner (visual guides)
Step 3: Test gesture recognition
Step 4: Adjust sensitivity if needed
```

---

## 5. User Flow

### 5.1 First Time Setup

```
1. Launch Application
   ↓
2. Camera Permission Request (if needed)
   ↓
3. Camera Selection (if multiple cameras)
   ↓
4. Quick Tutorial (5 gesture demonstrations)
   ↓
5. Calibration Wizard
   ↓
6. Main Window with Live Tracking
```

### 5.2 Normal Usage Flow

```
1. Start application (or resume from tray)
   ↓
2. Position hand in front of webcam
   ↓
3. Application detects hand automatically
   ↓
4. Perform gestures:
   - Index finger extended → Move cursor
   - Pinch → Click
   - Two fingers → Scroll
   ↓
5. Minimize to tray for background operation
```

### 5.3 Settings Adjustment Flow

```
1. Open Settings Panel
   ↓
2. Adjust parameters in real-time
   ↓
3. Test gestures with live preview
   ↓
4. Save configuration
   ↓
5. Return to tracking
```

---

## 6. Implementation Phases

### Phase 1: Core Infrastructure (Week 1)
- [ ] Setup project structure and dependencies
- [ ] Implement VideoCapture module with OpenCV
- [ ] Integrate MediaPipe hand tracking
- [ ] Create basic PyQt6 window with camera feed
- [ ] Test hand landmark detection

### Phase 2: Gesture Recognition (Week 2)
- [ ] Implement cursor control with index finger
- [ ] Implement pinch detection for left click
- [ ] Create coordinate mapping and smoothing
- [ ] Implement right-click gesture
- [ ] Add gesture debouncing and filtering

### Phase 3: Advanced Features (Week 3)
- [ ] Implement scroll detection and execution
- [ ] Create settings panel UI
- [ ] Implement configuration save/load
- [ ] Add calibration wizard
- [ ] Performance optimization

### Phase 4: Polish & Distribution (Week 4)
- [ ] System tray integration
- [ ] Error handling and edge cases
- [ ] Create user tutorial/onboarding
- [ ] Package application (PyInstaller)
- [ ] Testing and bug fixes

---

## 7. Technical Challenges & Solutions

### Challenge 1: Jittery Cursor Movement
**Problem:** Hand tracking can be noisy, causing cursor jitter  
**Solution:** 
- Exponential moving average (EMA) smoothing
- Kalman filtering for prediction
- Dead zone near current position

### Challenge 2: False Positive Gestures
**Problem:** Unintended gesture detection  
**Solution:**
- Gesture state machines with minimum hold times
- Confidence thresholds
- Gesture debouncing (minimum time between detections)

### Challenge 3: Varying Lighting Conditions
**Problem:** Hand detection fails in poor lighting  
**Solution:**
- MediaPipe is relatively robust to lighting
- Add visual feedback when hand not detected
- Recommend minimum lighting requirements

### Challenge 4: Performance on Lower-End Devices
**Problem:** Real-time processing is CPU-intensive  
**Solution:**
- Reduce camera resolution (640x480 is sufficient)
- Frame skipping if CPU usage too high
- Optimize hand tracking frequency vs. cursor update frequency

### Challenge 5: Accidental Clicks While Moving
**Problem:** Users may accidentally pinch while moving  
**Solution:**
- Implement motion threshold: no click if hand moving rapidly
- Add slight delay before click recognition
- Visual feedback showing pinch detection

---

## 8. Configuration & Settings

### 8.1 User-Adjustable Settings

| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| Sensitivity | 1-10 | 5 | Cursor movement speed multiplier |
| Smoothing | 1-10 | 6 | Amount of cursor smoothing (higher = smoother but slower) |
| Pinch Threshold | 0.02-0.10 | 0.05 | Distance for pinch detection |
| Scroll Sensitivity | 1-10 | 5 | Scroll speed multiplier |
| Click Debounce | 100-500ms | 300ms | Minimum time between clicks |
| Hand Detection Confidence | 0.5-0.9 | 0.7 | Minimum confidence for hand detection |

### 8.2 Advanced Settings

- Camera selection (if multiple cameras)
- Camera resolution (320p, 480p, 720p)
- Mirror mode (flip camera feed)
- Active area definition (use only center portion of frame)
- Gesture enable/disable toggles
- Keyboard shortcuts for pause/resume

---

## 9. File Structure

```
GestureMouse/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── camera.py           # VideoCapture module
│   │   ├── hand_tracker.py     # MediaPipe integration
│   │   ├── gesture_detector.py # Gesture recognition
│   │   └── mouse_controller.py # Mouse automation
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # Main UI window
│   │   ├── settings_dialog.py  # Settings panel
│   │   ├── calibration.py      # Calibration wizard
│   │   └── system_tray.py      # Tray integration
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration manager
│   │   ├── smoothing.py        # Filtering algorithms
│   │   └── coordinate_mapper.py# Coordinate transformations
│   └── resources/
│       ├── icons/              # Application icons
│       ├── images/             # Tutorial images
│       └── config/             # Default configurations
├── tests/
│   ├── test_gestures.py
│   ├── test_tracking.py
│   └── test_smoothing.py
├── docs/
│   ├── user_guide.md
│   └── developer_guide.md
├── requirements.txt
├── setup.py
├── README.md
├── LICENSE
└── .gitignore
```

---

## 10. Dependencies

### 10.1 Python Packages (requirements.txt)

```
# Core Dependencies
mediapipe>=0.10.9
opencv-python>=4.8.0
PyQt6>=6.6.0
pyautogui>=0.9.54
numpy>=1.24.0
pillow>=10.0.0

# Optional/Alternative
pynput>=1.7.6

# Development
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
```

### 10.2 System Requirements

**Minimum:**
- OS: Windows 10/11, macOS 10.14+, Ubuntu 20.04+
- CPU: Intel i3 8th gen or equivalent
- RAM: 4GB
- Webcam: 720p @ 30fps
- Python: 3.10+

**Recommended:**
- CPU: Intel i5 10th gen or equivalent
- RAM: 8GB
- Webcam: 1080p @ 30fps

---

## 11. Security & Privacy

### 11.1 Privacy Considerations
- **Local Processing:** All video processing happens locally, no cloud upload
- **No Recording:** Camera feed is processed in real-time, not stored
- **No Network:** Application does not require internet connection
- **Camera Indicator:** Respect OS camera indicator light

### 11.2 Permissions Required
- Camera access
- Accessibility permissions (for mouse control on macOS)
- No network permissions needed

---

## 12. Testing Strategy

### 12.1 Unit Tests
- Gesture detection accuracy
- Coordinate mapping correctness
- Smoothing algorithm validation
- Configuration save/load

### 12.2 Integration Tests
- Camera → Tracking → Gesture → Mouse flow
- UI interaction with core modules
- Multi-threading stability

### 12.3 User Acceptance Testing
- Gesture recognition accuracy in various lighting
- Cursor smoothness and responsiveness
- UI intuitiveness
- Performance on target hardware

---

## 13. Distribution & Installation

### 13.1 Packaging

**Windows:**
- PyInstaller for standalone .exe
- Optional: NSIS installer with Start Menu shortcuts

**macOS:**
- PyInstaller for .app bundle
- Optional: DMG package with drag-to-Applications

**Linux:**
- PyInstaller for executable
- Optional: AppImage or .deb package

### 13.2 Installation Steps

```bash
# Development Installation
git clone https://github.com/yourusername/gesturemouse.git
cd gesturemouse
pip install -r requirements.txt
python src/main.py

# User Installation (from release)
# Download executable from releases
# Run installer or extract and run
```

---

## 14. Future Enhancements

### Version 2.0 Features
- **Zoom gesture** (two-hand pinch in/out)
- **Drag and drop** (pinch + move + release)
- **Multi-monitor support** with gesture to switch screens
- **Gesture macros** (custom gesture recording)
- **Voice commands** integrated with gestures
- **Multiple hand support** (two hands for advanced controls)
- **Gesture training mode** (improve recognition with user data)

### Version 3.0 Features
- **AI-powered gesture customization**
- **Cross-device control** (control other devices on network)
- **VR/AR integration**
- **Gesture profiles** (different gestures for different applications)

---

## 15. Success Metrics

### Key Performance Indicators (KPIs)
- Gesture recognition accuracy: >95%
- Cursor latency: <100ms
- Application crash rate: <0.1%
- User satisfaction: >4.0/5.0
- CPU usage: <25% average

### User Feedback Metrics
- Ease of setup (tutorial completion rate)
- Daily active usage time
- Feature utilization (which gestures used most)
- Calibration frequency (indicates accuracy issues)

---

## 16. Known Limitations

1. **Lighting Dependency:** Requires adequate lighting for hand detection
2. **Single Hand:** Initially supports one hand tracking
3. **Camera Quality:** Performance depends on webcam quality
4. **Background Complexity:** Busy backgrounds may affect detection
5. **Hand Size:** Very small or very large hands may need recalibration
6. **Occlusion:** Partial hand visibility reduces accuracy

---

## 17. Support & Documentation

### User Documentation
- Quick start guide
- Video tutorials for each gesture
- Troubleshooting FAQ
- Calibration best practices

### Developer Documentation
- Architecture overview
- API documentation
- Contributing guidelines
- Build instructions

---

## Appendix A: MediaPipe Hand Landmarks Reference

```
Landmark IDs and Positions:
0: WRIST
1: THUMB_CMC
2: THUMB_MCP
3: THUMB_IP
4: THUMB_TIP
5: INDEX_FINGER_MCP
6: INDEX_FINGER_PIP
7: INDEX_FINGER_DIP
8: INDEX_FINGER_TIP
9: MIDDLE_FINGER_MCP
10: MIDDLE_FINGER_PIP
11: MIDDLE_FINGER_DIP
12: MIDDLE_FINGER_TIP
13: RING_FINGER_MCP
14: RING_FINGER_PIP
15: RING_FINGER_DIP
16: RING_FINGER_TIP
17: PINKY_MCP
18: PINKY_PIP
19: PINKY_DIP
20: PINKY_TIP
```

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-29 | Development Team | Initial PRD creation |

---

**End of Document**
