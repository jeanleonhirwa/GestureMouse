# GestureMouse Implementation Plan (Post-MVP)

This document outlines the step-by-step plan to move from the current MVP to a fully featured, professional-grade application as defined in the [PRD](../prd.md).

## 📅 Phase 1: Stabilization & Cursor Experience
**Goal:** Improve the "feel" of the mouse and ensure the app doesn't crash on hardware hiccups.

### 1.1 Non-linear Mouse Acceleration
*   **File:** `src/core/mouse_controller.py`
*   **Task:** Replace linear mapping with a sigmoid or power curve.
*   **Logic:** 
    *   Calculate velocity of hand movement.
    *   Apply a multiplier: `actual_move = base_move * (velocity ^ acceleration_factor)`.
    *   This allows for high precision during slow movements and quick navigation during fast movements.

### 1.2 Camera Auto-Reconnect
*   **File:** `src/core/camera.py`
*   **Task:** Implement a retry mechanism.
*   **Logic:** If `read_frame()` fails, enter a "Reconnecting" state. Attempt to re-initialize the `cv2.VideoCapture` every 2 seconds instead of terminating the worker thread.

### 1.3 Advanced Right-Click Logic
*   **File:** `src/core/gesture_detector.py`
*   **Task:** Implement timed pinch.
*   **Logic:** If Thumb-Middle distance is below threshold, start a timer. If held for >1.0s, trigger `RIGHT_CLICK`. (Current implementation only handles the immediate trigger).

---

## 🚀 Phase 2: Core Feature Completion
**Goal:** Implement the missing functionality required by the PRD.

### 2.1 Drag & Drop Implementation
*   **Files:** `src/core/gesture_detector.py`, `src/core/mouse_controller.py`
*   **Task:** Add "Pinch and Hold" state.
*   **Logic:** 
    *   `GestureDetector`: Detect a sustained pinch (Thumb-Index) that lasts longer than the click debounce.
    *   `MouseController`: Execute `pyautogui.mouseDown()` on start and `pyautogui.mouseUp()` on release.

### 2.2 Calibration Wizard
*   **Files:** `src/ui/calibration_wizard.py` (New), `src/utils/coordinate_mapper.py`
*   **Task:** Map physical hand space to digital screen space.
*   **Steps:**
    1.  User clicks "Calibrate".
    2.  Full-screen transparent window appears.
    3.  User is prompted to hold their hand in Top-Left, then Bottom-Right.
    4.  Store these normalized landmark coordinates as the new "Active Area" boundaries.

---

## 🎨 Phase 3: UI/UX Refinement
**Goal:** Make the app comfortable for long-term use.

### 3.1 Advanced Settings Dialog
*   **File:** `src/ui/settings_dialog.py` (New)
*   **Task:** Offload clutter from the main window.
*   **Content:**
    *   Pinch distance thresholds.
    *   Scroll sensitivity multipliers.
    *   Camera resolution and FPS settings.
    *   Hand detection confidence sliders.

### 3.2 Multi-Monitor Support
*   **File:** `src/core/mouse_controller.py`, `src/utils/config.py`
*   **Task:** Targeting specific displays.
*   **Logic:** Use `screeninfo` or `PyQt6.QtGui.QScreen` to list monitors. Allow user to pick "Monitor 1", "Monitor 2", or "All".

### 3.3 Visual Feedback (OSD)
*   **File:** `src/ui/osd_overlay.py` (New)
*   **Task:** Confirmation without looking at the app.
*   **Logic:** A tiny, stay-on-top, click-through widget that appears near the cursor for 500ms showing an icon (e.g., a "Click" icon or "Scroll" arrows) when a gesture is triggered.

---

## ⚡ Phase 4: Performance & Polish
**Goal:** Minimize resource usage and finalize the codebase.

### 4.1 Tracking Resolution Optimization
*   **File:** `src/core/hand_tracker.py`
*   **Task:** Downscale internal processing.
*   **Logic:** Capture at 640x480 for the UI, but resize to 320x240 before passing to MediaPipe. This significantly reduces CPU usage with minimal accuracy loss.

### 4.2 Smart Throttling
*   **File:** `src/main.py` (TrackingWorker)
*   **Task:** Power saving.
*   **Logic:** If no hand is detected for 10 seconds, drop tracking frequency to 5 FPS. Resume 30 FPS immediately upon detecting movement.

---

## 🛠️ AI Direction Instructions

When directing an AI agent to implement these steps, use the following sequence:

1.  **Refactor Mouse Control:** Start with Phase 1.1 and 1.2 to ensure a stable foundation.
2.  **State Machine Upgrade:** Move to Phase 2.1 (Drag & Drop) as it requires modifying both the detector and the controller.
3.  **UI Expansion:** Implement the Calibration Wizard (Phase 2.2) followed by the Advanced Settings (Phase 3.1).
4.  **Polish:** Apply Phase 4 optimizations last.

**Verification Rule:** After every step, run `test_installation.py` and a manual functional test to ensure the MediaPipe-PyQt6 DLL conflict hasn't returned.
