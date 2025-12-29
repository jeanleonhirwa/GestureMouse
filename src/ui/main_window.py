"""
Main window UI for GestureMouse application
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSlider, QCheckBox, QComboBox,
                             QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QCloseEvent
import cv2
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""
    
    # Signal emitted when window is closed
    closing = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GestureMouse - Webcam Gesture Control")
        self.setMinimumSize(900, 700)
        
        # Initialize UI components
        self.init_ui()
        
        logger.info("Main window initialized")
    
    def init_ui(self):
        """Initialize the user interface"""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Top section: Camera feed and status
        top_layout = QHBoxLayout()
        
        # Camera feed
        self.camera_label = QLabel()
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setMaximumSize(640, 480)
        self.camera_label.setStyleSheet("border: 2px solid #333; background-color: #000;")
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setText("Camera feed will appear here")
        top_layout.addWidget(self.camera_label)
        
        # Status panel
        status_group = self.create_status_panel()
        top_layout.addWidget(status_group)
        
        main_layout.addLayout(top_layout)
        
        # Gestures panel
        gestures_group = self.create_gestures_panel()
        main_layout.addWidget(gestures_group)
        
        # Settings panel
        settings_group = self.create_settings_panel()
        main_layout.addWidget(settings_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Tracking")
        self.start_button.setMinimumHeight(40)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(self.start_button)
        
        self.minimize_button = QPushButton("Minimize to Tray")
        self.minimize_button.setMinimumHeight(40)
        button_layout.addWidget(self.minimize_button)
        
        main_layout.addLayout(button_layout)
    
    def create_status_panel(self) -> QGroupBox:
        """Create the status panel"""
        group = QGroupBox("Status")
        layout = QVBoxLayout()
        
        # Tracking status
        self.status_label = QLabel("● Stopped")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #f44336;")
        layout.addWidget(self.status_label)
        
        layout.addSpacing(10)
        
        # Hand detected
        hand_layout = QHBoxLayout()
        hand_layout.addWidget(QLabel("Hand Detected:"))
        self.hand_detected_label = QLabel("✗ No")
        self.hand_detected_label.setStyleSheet("font-weight: bold; color: #f44336;")
        hand_layout.addWidget(self.hand_detected_label)
        hand_layout.addStretch()
        layout.addLayout(hand_layout)
        
        layout.addSpacing(10)
        
        # Active gesture
        gesture_layout = QHBoxLayout()
        gesture_layout.addWidget(QLabel("Active Gesture:"))
        self.gesture_label = QLabel("None")
        self.gesture_label.setStyleSheet("font-weight: bold;")
        gesture_layout.addWidget(self.gesture_label)
        gesture_layout.addStretch()
        layout.addLayout(gesture_layout)
        
        layout.addSpacing(10)
        
        # FPS counter
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS:"))
        self.fps_label = QLabel("0")
        self.fps_label.setStyleSheet("font-weight: bold;")
        fps_layout.addWidget(self.fps_label)
        fps_layout.addStretch()
        layout.addLayout(fps_layout)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
    
    def create_gestures_panel(self) -> QGroupBox:
        """Create the gestures enable/disable panel"""
        group = QGroupBox("Gestures")
        layout = QGridLayout()
        
        self.cursor_control_cb = QCheckBox("Cursor Control")
        self.cursor_control_cb.setChecked(True)
        layout.addWidget(self.cursor_control_cb, 0, 0)
        
        self.left_click_cb = QCheckBox("Left Click")
        self.left_click_cb.setChecked(True)
        layout.addWidget(self.left_click_cb, 0, 1)
        
        self.right_click_cb = QCheckBox("Right Click")
        self.right_click_cb.setChecked(True)
        layout.addWidget(self.right_click_cb, 1, 0)
        
        self.scroll_cb = QCheckBox("Scrolling")
        self.scroll_cb.setChecked(True)
        layout.addWidget(self.scroll_cb, 1, 1)
        
        group.setLayout(layout)
        return group
    
    def create_settings_panel(self) -> QGroupBox:
        """Create the settings panel"""
        group = QGroupBox("Settings")
        layout = QGridLayout()
        
        # Sensitivity slider
        layout.addWidget(QLabel("Sensitivity:"), 0, 0)
        self.sensitivity_slider = QSlider(Qt.Orientation.Horizontal)
        self.sensitivity_slider.setMinimum(1)
        self.sensitivity_slider.setMaximum(10)
        self.sensitivity_slider.setValue(5)
        self.sensitivity_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.sensitivity_slider.setTickInterval(1)
        layout.addWidget(self.sensitivity_slider, 0, 1)
        self.sensitivity_value_label = QLabel("5")
        layout.addWidget(self.sensitivity_value_label, 0, 2)
        
        # Smoothing slider
        layout.addWidget(QLabel("Smoothing:"), 1, 0)
        self.smoothing_slider = QSlider(Qt.Orientation.Horizontal)
        self.smoothing_slider.setMinimum(1)
        self.smoothing_slider.setMaximum(10)
        self.smoothing_slider.setValue(3)
        self.smoothing_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.smoothing_slider.setTickInterval(1)
        layout.addWidget(self.smoothing_slider, 1, 1)
        self.smoothing_value_label = QLabel("3")
        layout.addWidget(self.smoothing_value_label, 1, 2)
        
        # Camera selection
        layout.addWidget(QLabel("Camera:"), 2, 0)
        self.camera_combo = QComboBox()
        self.camera_combo.addItem("Camera 0 (Default)")
        layout.addWidget(self.camera_combo, 2, 1, 1, 2)
        
        # Connect slider signals
        self.sensitivity_slider.valueChanged.connect(
            lambda v: self.sensitivity_value_label.setText(str(v))
        )
        self.smoothing_slider.valueChanged.connect(
            lambda v: self.smoothing_value_label.setText(str(v))
        )
        
        group.setLayout(layout)
        return group
    
    def update_camera_feed(self, frame: np.ndarray):
        """
        Update the camera feed display
        
        Args:
            frame: Frame to display (BGR format)
        """
        if frame is None:
            return
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize to fit label if needed
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        
        # Convert to QImage
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Convert to QPixmap and display
        pixmap = QPixmap.fromImage(qt_image)
        self.camera_label.setPixmap(pixmap.scaled(
            self.camera_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
    
    def update_status(self, is_tracking: bool):
        """
        Update tracking status display
        
        Args:
            is_tracking: Whether tracking is active
        """
        if is_tracking:
            self.status_label.setText("● Tracking")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4CAF50;")
            self.start_button.setText("Stop Tracking")
            self.start_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
        else:
            self.status_label.setText("● Stopped")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #f44336;")
            self.start_button.setText("Start Tracking")
            self.start_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
    
    def update_hand_detected(self, detected: bool):
        """
        Update hand detection status
        
        Args:
            detected: Whether hand is detected
        """
        if detected:
            self.hand_detected_label.setText("✓ Yes")
            self.hand_detected_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        else:
            self.hand_detected_label.setText("✗ No")
            self.hand_detected_label.setStyleSheet("font-weight: bold; color: #f44336;")
    
    def update_gesture(self, gesture: str):
        """
        Update active gesture display
        
        Args:
            gesture: Name of active gesture
        """
        self.gesture_label.setText(gesture)
    
    def update_fps(self, fps: float):
        """
        Update FPS display
        
        Args:
            fps: Current FPS
        """
        self.fps_label.setText(f"{fps:.1f}")
    
    def closeEvent(self, event: QCloseEvent):
        """Handle window close event"""
        self.closing.emit()
        event.accept()
