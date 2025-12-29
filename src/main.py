"""
GestureMouse - Main application entry point
Webcam-based gesture control for mouse operations
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, QObject
import cv2
import logging

from core.camera import CameraManager
from core.hand_tracker import HandDetector
from core.gesture_detector import GestureDetector, GestureType
from core.mouse_controller import MouseController
from ui.main_window import MainWindow
from ui.system_tray import SystemTrayManager
from utils.config import ConfigManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TrackingWorker(QObject):
    """Worker thread for hand tracking and gesture detection"""
    
    # Signals
    frame_processed = pyqtSignal(object, bool, str, float)  # frame, hand_detected, gesture, fps
    error_occurred = pyqtSignal(str)
    
    def __init__(self, config: ConfigManager):
        super().__init__()
        self.config = config
        self.is_running = False
        self.is_paused = False
        
        # Initialize components
        self.camera = None
        self.hand_detector = None
        self.gesture_detector = None
        self.mouse_controller = None
        
        # FPS tracking
        self.frame_count = 0
        self.fps_start_time = time.time()
        self.current_fps = 0.0
    
    def initialize(self):
        """Initialize all components"""
        try:
            # Camera
            camera_config = self.config.get_section('camera')
            self.camera = CameraManager(
                camera_index=camera_config.get('index', 0),
                width=camera_config.get('width', 640),
                height=camera_config.get('height', 480)
            )
            
            if not self.camera.start():
                raise Exception("Failed to start camera")
            
            # Hand detector
            tracking_config = self.config.get_section('tracking')
            self.hand_detector = HandDetector(
                max_hands=tracking_config.get('max_hands', 1),
                detection_confidence=tracking_config.get('detection_confidence', 0.7),
                tracking_confidence=tracking_config.get('tracking_confidence', 0.5)
            )
            
            # Gesture detector
            gesture_config = self.config.get_section('gestures')
            self.gesture_detector = GestureDetector(
                pinch_threshold=gesture_config.get('pinch_threshold', 0.05),
                scroll_threshold=gesture_config.get('scroll_threshold', 0.02),
                click_debounce=gesture_config.get('click_debounce', 0.3)
            )
            
            # Mouse controller
            mouse_config = self.config.get_section('mouse')
            self.mouse_controller = MouseController(
                sensitivity=mouse_config.get('sensitivity', 1.5),
                smoothing=mouse_config.get('smoothing', 0.3),
                scroll_sensitivity=mouse_config.get('scroll_sensitivity', 5.0)
            )
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            self.error_occurred.emit(str(e))
            return False
    
    def run(self):
        """Main tracking loop"""
        self.is_running = True
        logger.info("Tracking worker started")
        
        while self.is_running:
            if self.is_paused:
                time.sleep(0.1)
                continue
            
            try:
                # Read frame from camera
                success, frame = self.camera.read_frame()
                if not success or frame is None:
                    continue
                
                # Detect hand
                hand_landmarks, annotated_frame = self.hand_detector.detect(frame)
                hand_detected = hand_landmarks is not None
                
                # Detect gesture
                gesture_type, gesture_data = self.gesture_detector.detect_gesture(hand_landmarks)
                
                # Execute mouse actions based on gesture
                gesture_name = self._execute_gesture(gesture_type, gesture_data)
                
                # Calculate FPS
                self.frame_count += 1
                elapsed = time.time() - self.fps_start_time
                if elapsed >= 1.0:
                    self.current_fps = self.frame_count / elapsed
                    self.frame_count = 0
                    self.fps_start_time = time.time()
                
                # Emit processed frame
                self.frame_processed.emit(
                    annotated_frame,
                    hand_detected,
                    gesture_name,
                    self.current_fps
                )
                
            except Exception as e:
                logger.error(f"Error in tracking loop: {e}")
                self.error_occurred.emit(str(e))
        
        logger.info("Tracking worker stopped")
    
    def _execute_gesture(self, gesture_type: GestureType, gesture_data: dict) -> str:
        """
        Execute mouse action based on detected gesture
        
        Args:
            gesture_type: Type of gesture detected
            gesture_data: Gesture-specific data
            
        Returns:
            Human-readable gesture name
        """
        gesture_config = self.config.get_section('gestures')
        
        if gesture_type == GestureType.CURSOR_MOVE:
            if gesture_config.get('cursor_control_enabled', True):
                position = gesture_data.get('position', (0.5, 0.5))
                self.mouse_controller.move_cursor(position[0], position[1])
                return "Cursor Move"
        
        elif gesture_type == GestureType.LEFT_CLICK:
            if gesture_config.get('left_click_enabled', True):
                self.mouse_controller.click('left')
                return "Left Click"
        
        elif gesture_type == GestureType.RIGHT_CLICK:
            if gesture_config.get('right_click_enabled', True):
                self.mouse_controller.click('right')
                return "Right Click"
        
        elif gesture_type == GestureType.SCROLL:
            if gesture_config.get('scroll_enabled', True):
                delta_y = gesture_data.get('delta_y', 0)
                if delta_y != 0:
                    self.mouse_controller.scroll(delta_y)
                    return "Scrolling"
                return "Scroll Mode"
        
        return "None"
    
    def stop(self):
        """Stop the tracking worker"""
        self.is_running = False
        if self.camera:
            self.camera.stop()
        if self.hand_detector:
            self.hand_detector.close()
    
    def pause(self):
        """Pause tracking"""
        self.is_paused = True
    
    def resume(self):
        """Resume tracking"""
        self.is_paused = False
    
    def update_mouse_settings(self, sensitivity: float, smoothing: float):
        """Update mouse controller settings"""
        if self.mouse_controller:
            self.mouse_controller.set_sensitivity(sensitivity)
            self.mouse_controller.set_smoothing(smoothing)


class GestureMouseApp:
    """Main application controller"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("GestureMouse")
        
        # Load configuration
        self.config = ConfigManager()
        
        # Create main window
        self.main_window = MainWindow()
        
        # Create system tray
        self.tray_manager = SystemTrayManager(self.app)
        self.tray_manager.setup()
        self.tray_manager.show()
        
        # Tracking components
        self.tracking_thread = None
        self.tracking_worker = None
        self.is_tracking = False
        
        # Connect signals
        self._connect_signals()
        
        logger.info("GestureMouseApp initialized")
    
    def _connect_signals(self):
        """Connect UI signals to handlers"""
        # Main window signals
        self.main_window.start_button.clicked.connect(self._on_start_stop_clicked)
        self.main_window.minimize_button.clicked.connect(self._on_minimize_clicked)
        self.main_window.closing.connect(self._on_window_closing)
        
        # Settings signals
        self.main_window.sensitivity_slider.valueChanged.connect(self._on_sensitivity_changed)
        self.main_window.smoothing_slider.valueChanged.connect(self._on_smoothing_changed)
        
        # Gesture enable/disable signals
        self.main_window.cursor_control_cb.toggled.connect(
            lambda checked: self.config.set('gestures', 'cursor_control_enabled', checked)
        )
        self.main_window.left_click_cb.toggled.connect(
            lambda checked: self.config.set('gestures', 'left_click_enabled', checked)
        )
        self.main_window.right_click_cb.toggled.connect(
            lambda checked: self.config.set('gestures', 'right_click_enabled', checked)
        )
        self.main_window.scroll_cb.toggled.connect(
            lambda checked: self.config.set('gestures', 'scroll_enabled', checked)
        )
        
        # System tray signals
        self.tray_manager.show_window_requested.connect(self._on_show_window)
        self.tray_manager.pause_tracking_requested.connect(self._on_pause_tracking)
        self.tray_manager.resume_tracking_requested.connect(self._on_resume_tracking)
        self.tray_manager.exit_requested.connect(self._on_exit)
    
    def _on_start_stop_clicked(self):
        """Handle start/stop button click"""
        if self.is_tracking:
            self._stop_tracking()
        else:
            self._start_tracking()
    
    def _start_tracking(self):
        """Start tracking"""
        logger.info("Starting tracking...")
        
        # Create tracking thread and worker
        self.tracking_thread = QThread()
        self.tracking_worker = TrackingWorker(self.config)
        self.tracking_worker.moveToThread(self.tracking_thread)
        
        # Connect worker signals
        self.tracking_worker.frame_processed.connect(self._on_frame_processed)
        self.tracking_worker.error_occurred.connect(self._on_tracking_error)
        
        # Connect thread signals
        self.tracking_thread.started.connect(self.tracking_worker.run)
        self.tracking_thread.finished.connect(self.tracking_thread.deleteLater)
        
        # Initialize worker
        if not self.tracking_worker.initialize():
            logger.error("Failed to initialize tracking worker")
            return
        
        # Start thread
        self.tracking_thread.start()
        self.is_tracking = True
        
        # Update UI
        self.main_window.update_status(True)
        self.tray_manager.update_tracking_status(True)
        self.tray_manager.show_message("GestureMouse", "Tracking started")
        
        logger.info("Tracking started successfully")
    
    def _stop_tracking(self):
        """Stop tracking"""
        logger.info("Stopping tracking...")
        
        if self.tracking_worker:
            self.tracking_worker.stop()
        
        if self.tracking_thread:
            self.tracking_thread.quit()
            self.tracking_thread.wait()
        
        self.is_tracking = False
        
        # Update UI
        self.main_window.update_status(False)
        self.main_window.update_hand_detected(False)
        self.main_window.update_gesture("None")
        self.tray_manager.update_tracking_status(False)
        self.tray_manager.show_message("GestureMouse", "Tracking stopped")
        
        logger.info("Tracking stopped")
    
    def _on_frame_processed(self, frame, hand_detected: bool, gesture: str, fps: float):
        """Handle processed frame from tracking worker"""
        self.main_window.update_camera_feed(frame)
        self.main_window.update_hand_detected(hand_detected)
        self.main_window.update_gesture(gesture)
        self.main_window.update_fps(fps)
    
    def _on_tracking_error(self, error: str):
        """Handle tracking error"""
        logger.error(f"Tracking error: {error}")
        self.tray_manager.show_message("GestureMouse Error", error)
    
    def _on_sensitivity_changed(self, value: int):
        """Handle sensitivity slider change"""
        sensitivity = value / 3.0  # Map 1-10 to ~0.3-3.3
        self.config.set('mouse', 'sensitivity', sensitivity)
        if self.tracking_worker:
            self.tracking_worker.update_mouse_settings(
                sensitivity,
                self.config.get('mouse', 'smoothing', 0.3)
            )
    
    def _on_smoothing_changed(self, value: int):
        """Handle smoothing slider change"""
        smoothing = value / 10.0  # Map 1-10 to 0.1-1.0
        self.config.set('mouse', 'smoothing', smoothing)
        if self.tracking_worker:
            self.tracking_worker.update_mouse_settings(
                self.config.get('mouse', 'sensitivity', 1.5),
                smoothing
            )
    
    def _on_minimize_clicked(self):
        """Handle minimize button click"""
        self.main_window.hide()
        self.tray_manager.show_message(
            "GestureMouse",
            "Application minimized to system tray"
        )
    
    def _on_show_window(self):
        """Handle show window request from tray"""
        self.main_window.show()
        self.main_window.activateWindow()
    
    def _on_pause_tracking(self):
        """Handle pause tracking request"""
        if self.tracking_worker:
            self.tracking_worker.pause()
            self.tray_manager.update_tracking_status(False)
    
    def _on_resume_tracking(self):
        """Handle resume tracking request"""
        if self.tracking_worker:
            self.tracking_worker.resume()
            self.tray_manager.update_tracking_status(True)
    
    def _on_window_closing(self):
        """Handle main window closing"""
        self._stop_tracking()
        self.config.save()
    
    def _on_exit(self):
        """Handle exit request"""
        self._stop_tracking()
        self.config.save()
        self.app.quit()
    
    def run(self):
        """Run the application"""
        self.main_window.show()
        return self.app.exec()


def main():
    """Main entry point"""
    logger.info("Starting GestureMouse application")
    
    try:
        app = GestureMouseApp()
        sys.exit(app.run())
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
