"""
Coordinate mapping utilities
Maps between different coordinate systems (camera, screen, normalized)
"""

import numpy as np
from typing import Tuple, Optional


class CoordinateMapper:
    """Maps coordinates between different coordinate systems"""
    
    def __init__(self,
                 camera_width: int = 640,
                 camera_height: int = 480,
                 screen_width: int = 1920,
                 screen_height: int = 1080):
        """
        Initialize coordinate mapper
        
        Args:
            camera_width: Camera frame width
            camera_height: Camera frame height
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Calibration offsets (can be adjusted through calibration)
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0
    
    def normalize_camera_coords(self, x: float, y: float) -> Tuple[float, float]:
        """
        Normalize camera coordinates to [0, 1] range
        
        Args:
            x: X coordinate in camera space
            y: Y coordinate in camera space
            
        Returns:
            Tuple of (normalized_x, normalized_y)
        """
        norm_x = x / self.camera_width if self.camera_width > 0 else 0
        norm_y = y / self.camera_height if self.camera_height > 0 else 0
        
        # Clamp to [0, 1]
        norm_x = max(0.0, min(1.0, norm_x))
        norm_y = max(0.0, min(1.0, norm_y))
        
        return norm_x, norm_y
    
    def normalized_to_screen(self, x: float, y: float) -> Tuple[int, int]:
        """
        Convert normalized coordinates to screen coordinates
        
        Args:
            x: Normalized x coordinate (0-1)
            y: Normalized y coordinate (0-1)
            
        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        # Apply calibration
        x_adjusted = (x - self.offset_x) * self.scale_x
        y_adjusted = (y - self.offset_y) * self.scale_y
        
        # Clamp to valid range
        x_adjusted = max(0.0, min(1.0, x_adjusted))
        y_adjusted = max(0.0, min(1.0, y_adjusted))
        
        # Map to screen
        screen_x = int(x_adjusted * self.screen_width)
        screen_y = int(y_adjusted * self.screen_height)
        
        # Ensure within bounds
        screen_x = max(0, min(self.screen_width - 1, screen_x))
        screen_y = max(0, min(self.screen_height - 1, screen_y))
        
        return screen_x, screen_y
    
    def camera_to_screen(self, x: float, y: float) -> Tuple[int, int]:
        """
        Convert camera coordinates directly to screen coordinates
        
        Args:
            x: X coordinate in camera space
            y: Y coordinate in camera space
            
        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        norm_x, norm_y = self.normalize_camera_coords(x, y)
        return self.normalized_to_screen(norm_x, norm_y)
    
    def set_calibration(self,
                       offset_x: float = 0.0,
                       offset_y: float = 0.0,
                       scale_x: float = 1.0,
                       scale_y: float = 1.0):
        """
        Set calibration parameters
        
        Args:
            offset_x: X offset in normalized space
            offset_y: Y offset in normalized space
            scale_x: X scale factor
            scale_y: Y scale factor
        """
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.scale_x = scale_x
        self.scale_y = scale_y
    
    def reset_calibration(self):
        """Reset calibration to defaults"""
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0
    
    def update_screen_size(self, width: int, height: int):
        """
        Update screen dimensions
        
        Args:
            width: New screen width
            height: New screen height
        """
        self.screen_width = width
        self.screen_height = height
    
    def update_camera_size(self, width: int, height: int):
        """
        Update camera dimensions
        
        Args:
            width: New camera width
            height: New camera height
        """
        self.camera_width = width
        self.camera_height = height
