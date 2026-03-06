"""
Advanced Settings Dialog for GestureMouse
Allows fine-tuning of gesture thresholds, camera settings, and confidence levels
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSlider, QPushButton, QGroupBox, QGridLayout,
                             QDoubleSpinBox, QSpinBox)
from PyQt6.QtCore import Qt
import logging

logger = logging.getLogger(__name__)

class SettingsDialog(QDialog):
    """Dialog for advanced configuration"""
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("Advanced Settings")
        self.setMinimumWidth(400)
        
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # --- Gesture Thresholds Group ---
        gesture_group = QGroupBox("Gesture Thresholds")
        gesture_layout = QGridLayout()
        
        # Pinch Threshold
        gesture_layout.addWidget(QLabel("Pinch Threshold:"), 0, 0)
        self.pinch_spin = QDoubleSpinBox()
        self.pinch_spin.setRange(0.01, 0.20)
        self.pinch_spin.setSingleStep(0.01)
        self.pinch_spin.setDecimals(3)
        gesture_layout.addWidget(self.pinch_spin, 0, 1)
        gesture_layout.addWidget(QLabel("(Lower = harder to click)"), 0, 2)
        
        # Scroll Threshold
        gesture_layout.addWidget(QLabel("Scroll Threshold:"), 1, 0)
        self.scroll_spin = QDoubleSpinBox()
        self.scroll_spin.setRange(0.005, 0.10)
        self.scroll_spin.setSingleStep(0.005)
        self.scroll_spin.setDecimals(3)
        gesture_layout.addWidget(self.scroll_spin, 1, 1)
        
        # Click Debounce
        gesture_layout.addWidget(QLabel("Click Debounce (s):"), 2, 0)
        self.debounce_spin = QDoubleSpinBox()
        self.debounce_spin.setRange(0.1, 1.0)
        self.debounce_spin.setSingleStep(0.1)
        gesture_layout.addWidget(self.debounce_spin, 2, 1)
        
        gesture_group.setLayout(gesture_layout)
        layout.addWidget(gesture_group)
        
        # --- Tracking Confidence Group ---
        tracking_group = QGroupBox("Tracking Confidence")
        tracking_layout = QGridLayout()
        
        # Detection Confidence
        tracking_layout.addWidget(QLabel("Detection:"), 0, 0)
        self.det_conf_spin = QDoubleSpinBox()
        self.det_conf_spin.setRange(0.1, 1.0)
        self.det_conf_spin.setSingleStep(0.05)
        tracking_layout.addWidget(self.det_conf_spin, 0, 1)
        
        # Tracking Confidence
        tracking_layout.addWidget(QLabel("Tracking:"), 1, 0)
        self.track_conf_spin = QDoubleSpinBox()
        self.track_conf_spin.setRange(0.1, 1.0)
        self.track_conf_spin.setSingleStep(0.05)
        tracking_layout.addWidget(self.track_conf_spin, 1, 1)
        
        tracking_group.setLayout(tracking_layout)
        layout.addWidget(tracking_group)
        
        # --- Buttons ---
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save && Apply")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

    def load_settings(self):
        """Load current values from config"""
        gestures = self.config.get_section('gestures')
        self.pinch_spin.setValue(gestures.get('pinch_threshold', 0.05))
        self.scroll_spin.setValue(gestures.get('scroll_threshold', 0.02))
        self.debounce_spin.setValue(gestures.get('click_debounce', 0.3))
        
        tracking = self.config.get_section('tracking')
        self.det_conf_spin.setValue(tracking.get('detection_confidence', 0.7))
        self.track_conf_spin.setValue(tracking.get('tracking_confidence', 0.5))

    def get_settings(self):
        """Return the current UI values as a dictionary"""
        return {
            'gestures': {
                'pinch_threshold': self.pinch_spin.value(),
                'scroll_threshold': self.scroll_spin.value(),
                'click_debounce': self.debounce_spin.value()
            },
            'tracking': {
                'detection_confidence': self.det_conf_spin.value(),
                'tracking_confidence': self.track_conf_spin.value()
            }
        }
