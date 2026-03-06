"""
On-Screen Display (OSD) Overlay for GestureMouse
Provides immediate visual feedback near the cursor when gestures are triggered
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QFont
import pyautogui

class OSDOverlay(QWidget):
    """Small, transient overlay near the mouse cursor"""
    
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput # Click-through
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # UI Setup
        self.layout = QVBoxLayout(self)
        self.label = QLabel("")
        self.label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 160);
                color: #4CAF50;
                border: 1px solid #4CAF50;
                border-radius: 10px;
                padding: 5px 15px;
                font-weight: bold;
                font-size: 16px;
            }
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)
        
        # Timer to hide the OSD
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)
        
        # Animation for fade out
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self.hide)

    def show_message(self, text: str, duration: int = 800):
        """Show a message at the current mouse position"""
        self.label.setText(text)
        self.adjustSize()
        
        # Move to mouse position (slightly offset)
        curr_x, curr_y = pyautogui.position()
        self.move(curr_x + 20, curr_y + 20)
        
        # Reset animation and show
        self.animation.stop()
        self.setWindowOpacity(1.0)
        self.show()
        
        # Restart timer
        self.hide_timer.start(duration - 300) # Leave time for animation
        
        # Start fade out animation slightly before hiding
        QTimer.singleShot(duration - 300, self.animation.start)
