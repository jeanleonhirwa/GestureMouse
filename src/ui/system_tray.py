"""
System tray integration for GestureMouse
"""

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QObject, pyqtSignal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SystemTrayManager(QObject):
    """Manages system tray icon and menu"""
    
    # Signals
    show_window_requested = pyqtSignal()
    pause_tracking_requested = pyqtSignal()
    resume_tracking_requested = pyqtSignal()
    exit_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tray_icon = None
        self.menu = None
        self.is_tracking = False
        
    def setup(self):
        """Setup system tray icon and menu"""
        # Create tray icon (using a simple colored icon for now)
        # In production, you would use an actual icon file
        self.tray_icon = QSystemTrayIcon(self.parent())
        
        # For now, we'll use the default application icon
        # TODO: Create and load custom icon
        # self.tray_icon.setIcon(QIcon("path/to/icon.png"))
        
        # Create context menu
        self.menu = QMenu()
        
        # Status action (non-clickable)
        self.status_action = QAction("● Stopped", self.menu)
        self.status_action.setEnabled(False)
        self.menu.addAction(self.status_action)
        
        self.menu.addSeparator()
        
        # Pause/Resume action
        self.pause_resume_action = QAction("▸ Start Tracking", self.menu)
        self.pause_resume_action.triggered.connect(self._on_pause_resume)
        self.menu.addAction(self.pause_resume_action)
        
        # Show window action
        show_action = QAction("▸ Show Window", self.menu)
        show_action.triggered.connect(self.show_window_requested.emit)
        self.menu.addAction(show_action)
        
        self.menu.addSeparator()
        
        # Exit action
        exit_action = QAction("▸ Exit", self.menu)
        exit_action.triggered.connect(self.exit_requested.emit)
        self.menu.addAction(exit_action)
        
        # Set the context menu
        self.tray_icon.setContextMenu(self.menu)
        
        # Connect double-click to show window
        self.tray_icon.activated.connect(self._on_tray_activated)
        
        # Set tooltip
        self.tray_icon.setToolTip("GestureMouse - Gesture Control")
        
        logger.info("System tray initialized")
    
    def show(self):
        """Show the system tray icon"""
        if self.tray_icon:
            self.tray_icon.show()
            logger.info("System tray icon shown")
    
    def hide(self):
        """Hide the system tray icon"""
        if self.tray_icon:
            self.tray_icon.hide()
            logger.info("System tray icon hidden")
    
    def update_tracking_status(self, is_tracking: bool):
        """
        Update tracking status in tray menu
        
        Args:
            is_tracking: Whether tracking is active
        """
        self.is_tracking = is_tracking
        
        if is_tracking:
            self.status_action.setText("● Tracking Active")
            self.pause_resume_action.setText("▸ Pause Tracking")
            self.tray_icon.setToolTip("GestureMouse - Tracking Active")
        else:
            self.status_action.setText("● Stopped")
            self.pause_resume_action.setText("▸ Resume Tracking")
            self.tray_icon.setToolTip("GestureMouse - Stopped")
    
    def show_message(self, title: str, message: str, duration: int = 3000):
        """
        Show a system tray notification
        
        Args:
            title: Notification title
            message: Notification message
            duration: Duration in milliseconds
        """
        if self.tray_icon:
            self.tray_icon.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                duration
            )
    
    def _on_pause_resume(self):
        """Handle pause/resume action"""
        if self.is_tracking:
            self.pause_tracking_requested.emit()
        else:
            self.resume_tracking_requested.emit()
    
    def _on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window_requested.emit()
