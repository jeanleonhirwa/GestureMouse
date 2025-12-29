"""
Mouse control module
Maps hand coordinates to screen coordinates and executes mouse actions
"""

import pyautogui
import numpy as np
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable PyAutoGUI fail-safe (moving mouse to corner to abort)
# We'll implement our own safety mechanisms
pyautogui.FAILSAFE = False


class SmoothingFilter:
    """Exponential moving average filter for smooth cursor movement"""
    
    def __init__(self, alpha: float = 0.3):
        """
        Initialize smoothing filter
        
        Args:
            alpha: Smoothing factor (0-1). Lower = more smoothing, higher = more responsive
        """
        self.alpha = max(0.0, min(1.0, alpha))  # Clamp to [0, 1]
        self.smoothed_x: Optional[float] = None
        self.smoothed_y: Optional[float] = None
    
    def filter(self, x: float, y: float) -> Tuple[float, float]:
        """
        Apply exponential moving average smoothing
        
        Args:
            x: Current x coordinate
            y: Current y coordinate
            
        Returns:
            Tuple of (smoothed_x, smoothed_y)
        """
        if self.smoothed_x is None or self.smoothed_y is None:
            # Initialize with first value
            self.smoothed_x = x
            self.smoothed_y = y
        else:
            # Apply EMA: smoothed = alpha * current + (1-alpha) * previous
            self.smoothed_x = self.alpha * x + (1 - self.alpha) * self.smoothed_x
            self.smoothed_y = self.alpha * y + (1 - self.alpha) * self.smoothed_y
        
        return self.smoothed_x, self.smoothed_y
    
    def reset(self):
        """Reset the filter"""
        self.smoothed_x = None
        self.smoothed_y = None


class MouseController:
    """Controls mouse cursor and actions"""
    
    def __init__(self,
                 sensitivity: float = 1.5,
                 smoothing: float = 0.3,
                 scroll_sensitivity: float = 5.0):
        """
        Initialize mouse controller
        
        Args:
            sensitivity: Cursor movement speed multiplier (1.0 = normal, higher = faster)
            smoothing: Smoothing factor (0-1, lower = more smoothing)
            scroll_sensitivity: Scroll speed multiplier
        """
        self.sensitivity = sensitivity
        self.smoothing_filter = SmoothingFilter(alpha=smoothing)
        self.scroll_sensitivity = scroll_sensitivity
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Define active tracking area (avoid edges)
        self.margin = 0.1  # 10% margin on each side
        
        logger.info(f"Mouse controller initialized. Screen: {self.screen_width}x{self.screen_height}")
    
    def map_to_screen(self, x: float, y: float) -> Tuple[int, int]:
        """
        Map normalized hand coordinates (0-1) to screen coordinates
        
        Args:
            x: Normalized x coordinate (0-1)
            y: Normalized y coordinate (0-1)
            
        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        # Apply margin to use only center portion of tracking area
        x_adjusted = (x - self.margin) / (1 - 2 * self.margin)
        y_adjusted = (y - self.margin) / (1 - 2 * self.margin)
        
        # Clamp to valid range
        x_adjusted = max(0.0, min(1.0, x_adjusted))
        y_adjusted = max(0.0, min(1.0, y_adjusted))
        
        # Map to screen coordinates with sensitivity
        screen_x = int(x_adjusted * self.screen_width * self.sensitivity)
        screen_y = int(y_adjusted * self.screen_height * self.sensitivity)
        
        # Clamp to screen bounds
        screen_x = max(0, min(self.screen_width - 1, screen_x))
        screen_y = max(0, min(self.screen_height - 1, screen_y))
        
        return screen_x, screen_y
    
    def move_cursor(self, x: float, y: float, smooth: bool = True):
        """
        Move cursor to specified position
        
        Args:
            x: Normalized x coordinate (0-1)
            y: Normalized y coordinate (0-1)
            smooth: Whether to apply smoothing
        """
        try:
            # Map to screen coordinates
            screen_x, screen_y = self.map_to_screen(x, y)
            
            # Apply smoothing if enabled
            if smooth:
                screen_x, screen_y = self.smoothing_filter.filter(screen_x, screen_y)
            
            # Move cursor (duration=0 for instant movement)
            pyautogui.moveTo(int(screen_x), int(screen_y), duration=0)
            
        except Exception as e:
            logger.error(f"Error moving cursor: {e}")
    
    def click(self, button: str = "left"):
        """
        Perform mouse click
        
        Args:
            button: "left" or "right"
        """
        try:
            if button == "left":
                pyautogui.click()
                logger.debug("Left click executed")
            elif button == "right":
                pyautogui.rightClick()
                logger.debug("Right click executed")
            else:
                logger.warning(f"Unknown button: {button}")
        except Exception as e:
            logger.error(f"Error clicking: {e}")
    
    def scroll(self, delta_y: float):
        """
        Perform scroll action
        
        Args:
            delta_y: Vertical scroll amount (positive = down, negative = up)
        """
        try:
            # Convert normalized delta to scroll clicks
            # Negative because screen y increases downward but scroll should be intuitive
            scroll_amount = int(-delta_y * self.scroll_sensitivity * 100)
            
            if scroll_amount != 0:
                pyautogui.scroll(scroll_amount)
                logger.debug(f"Scroll executed: {scroll_amount}")
        except Exception as e:
            logger.error(f"Error scrolling: {e}")
    
    def set_sensitivity(self, sensitivity: float):
        """
        Update cursor sensitivity
        
        Args:
            sensitivity: New sensitivity value
        """
        self.sensitivity = max(0.1, min(5.0, sensitivity))
        logger.info(f"Sensitivity set to {self.sensitivity}")
    
    def set_smoothing(self, smoothing: float):
        """
        Update smoothing factor
        
        Args:
            smoothing: New smoothing value (0-1)
        """
        self.smoothing_filter.alpha = max(0.0, min(1.0, smoothing))
        logger.info(f"Smoothing set to {self.smoothing_filter.alpha}")
    
    def set_scroll_sensitivity(self, sensitivity: float):
        """
        Update scroll sensitivity
        
        Args:
            sensitivity: New scroll sensitivity value
        """
        self.scroll_sensitivity = max(0.1, min(10.0, sensitivity))
        logger.info(f"Scroll sensitivity set to {self.scroll_sensitivity}")
    
    def reset_smoothing(self):
        """Reset smoothing filter"""
        self.smoothing_filter.reset()
