"""
Camera/Video capture module for GestureMouse
Handles webcam initialization, frame capture, and preprocessing
"""

import cv2
import numpy as np
from typing import Optional, Tuple
import logging

import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CameraManager:
    """Manages webcam connection and frame capture"""
    
    def __init__(self, camera_index: int = 0, width: int = 640, height: int = 480):
        """
        Initialize camera manager
        
        Args:
            camera_index: Camera device index (0 for default webcam)
            width: Frame width in pixels
            height: Frame height in pixels
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_active = False
        
        # Reconnection settings
        self.is_reconnecting = False
        self.last_reconnect_time = 0
        self.reconnect_interval = 2.0  # seconds
        
    def start(self) -> bool:
        """
        Start camera capture
        
        Returns:
            True if camera started successfully, False otherwise
        """
        try:
            if self.cap is not None:
                self.cap.release()
                
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                logger.error(f"Failed to open camera {self.camera_index}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_active = True
            self.is_reconnecting = False
            logger.info(f"Camera {self.camera_index} started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error starting camera: {e}")
            return False
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read a frame from the camera with auto-reconnect logic
        
        Returns:
            Tuple of (success, frame)
            - success: True if frame was read successfully
            - frame: The captured frame as numpy array (BGR format)
        """
        if self.is_reconnecting:
            current_time = time.time()
            if current_time - self.last_reconnect_time >= self.reconnect_interval:
                logger.info(f"Attempting to reconnect camera {self.camera_index}...")
                self.last_reconnect_time = current_time
                if self.start():
                    logger.info("Camera reconnected!")
                else:
                    return False, None
            else:
                return False, None

        if not self.is_active or self.cap is None:
            return False, None
        
        try:
            ret, frame = self.cap.read()
            
            if not ret or frame is None:
                logger.warning("Failed to read frame from camera. Entering reconnect mode.")
                self.is_reconnecting = True
                self.is_active = False
                self.last_reconnect_time = time.time()
                return False, None
            
            # Flip frame horizontally for mirror effect (more intuitive for users)
            frame = cv2.flip(frame, 1)
            
            return True, frame
            
        except Exception as e:
            logger.error(f"Error reading frame: {e}")
            self.is_reconnecting = True
            self.is_active = False
            self.last_reconnect_time = time.time()
            return False, None
    
    def stop(self):
        """Stop camera capture and release resources"""
        if self.cap is not None:
            self.cap.release()
            self.is_active = False
            logger.info("Camera stopped")
    
    def get_available_cameras(self) -> list:
        """
        Get list of available camera indices
        
        Returns:
            List of available camera indices
        """
        available = []
        for i in range(5):  # Check first 5 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available.append(i)
                cap.release()
        return available
    
    def get_frame_size(self) -> Tuple[int, int]:
        """
        Get current frame dimensions
        
        Returns:
            Tuple of (width, height)
        """
        if self.cap is not None and self.is_active:
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            return width, height
        return self.width, self.height
    
    def __del__(self):
        """Cleanup on destruction"""
        self.stop()
