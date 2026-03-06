"""
Calibration Wizard UI for GestureMouse
Full-screen overlay to map hand movement range to screen bounds
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QColor, QPainter, QFont
import logging

logger = logging.getLogger(__name__)

class CalibrationWizard(QWidget):
    """Full-screen calibration overlay"""
    
    # Signals
    calibration_complete = pyqtSignal(float, float, float, float)  # x_min, y_min, x_max, y_max
    calibration_cancelled = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Set window properties for full-screen overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        
        # Calibration state
        self.step = 0  # 0: Intro, 1: Top-Left, 2: Bottom-Right, 3: Success
        self.points = []  # List of captured (x, y) coordinates
        
        # UI Components
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label = QLabel("Calibration Wizard")
        self.label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        self.sub_label = QLabel("Position your hand in the center to start")
        self.sub_label.setStyleSheet("color: #DDD; font-size: 18px;")
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sub_label)
        
        self.btn = QPushButton("Start Calibration")
        self.btn.setFixedSize(200, 50)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.btn.clicked.connect(self.next_step)
        layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.hint_label = QLabel("Press 'ESC' to cancel")
        self.hint_label.setStyleSheet("color: #888; font-size: 14px;")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.hint_label)

    def next_step(self):
        self.step += 1
        
        if self.step == 1:
            self.label.setText("Step 1: Top-Left")
            self.sub_label.setText("Move your index finger to the TOP-LEFT corner of your comfortable range and click 'Capture'")
            self.btn.setText("Capture Top-Left")
        elif self.step == 2:
            self.label.setText("Step 2: Bottom-Right")
            self.sub_label.setText("Move your index finger to the BOTTOM-RIGHT corner of your comfortable range and click 'Capture'")
            self.btn.setText("Capture Bottom-Right")
        elif self.step == 3:
            self.finish_calibration()
            
    def capture_point(self, x: float, y: float):
        """Called by main app to provide current hand position"""
        if self.step == 1:
            self.points.append((x, y))
            self.next_step()
        elif self.step == 2:
            self.points.append((x, y))
            self.next_step()
            
    def finish_calibration(self):
        if len(self.points) >= 2:
            p1 = self.points[0]
            p2 = self.points[1]
            
            x_min = min(p1[0], p2[0])
            y_min = min(p1[1], p2[1])
            x_max = max(p1[0], p2[0])
            y_max = max(p1[1], p2[1])
            
            logger.info(f"Calibration successful: Min({x_min}, {y_min}), Max({x_max}, {y_max})")
            self.calibration_complete.emit(x_min, y_min, x_max, y_max)
            
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.calibration_cancelled.emit()
            self.close()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw semi-transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 180))
        
        # Draw focus circles
        if self.step == 1:
            self.draw_target(painter, 100, 100)
        elif self.step == 2:
            self.draw_target(painter, self.width() - 100, self.height() - 100)

    def draw_target(self, painter, x, y):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(76, 175, 80, 100))
        painter.drawEllipse(QPoint(x, y), 50, 50)
        painter.setBrush(QColor(76, 175, 80, 200))
        painter.drawEllipse(QPoint(x, y), 20, 20)
