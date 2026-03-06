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
                 scroll_sensitivity: float = 5.0,
                 acceleration_factor: float = 1.2):
        """
        Initialize mouse controller
        
        Args:
            sensitivity: Cursor movement speed multiplier (1.0 = normal, higher = faster)
            smoothing: Smoothing factor (0-1, lower = more smoothing)
            scroll_sensitivity: Scroll speed multiplier
            acceleration_factor: Multiplier for fast movements (non-linear)
        """
        self.sensitivity = sensitivity
        self.smoothing_filter = SmoothingFilter(alpha=smoothing)
        self.scroll_sensitivity = scroll_sensitivity
        self.acceleration_factor = acceleration_factor
        
        # Monitor management
        self.target_monitor = 0  # 0 means primary or all (standard behavior)
        self.screen_width, self.screen_height = pyautogui.size()
        self.monitor_offset_x = 0
        self.monitor_offset_y = 0
        
        # Define active tracking area (calibrated range)
        self.x_min, self.y_min = 0.1, 0.1
        self.x_max, self.y_max = 0.9, 0.9
        
        logger.info(f"Mouse controller initialized. Screen: {self.screen_width}x{self.screen_height}")
    
    def set_active_area(self, x_min: float, y_min: float, x_max: float, y_max: float):
        """Update the tracking boundaries based on calibration"""
        self.x_min = max(0.0, min(1.0, x_min))
        self.y_min = max(0.0, min(1.0, y_min))
        self.x_max = max(0.0, min(1.0, x_max))
        self.y_max = max(0.0, min(1.0, y_max))
        logger.info(f"Active area updated: ({self.x_min}, {self.y_min}) to ({self.x_max}, {self.y_max})")

    def map_to_screen(self, x: float, y: float) -> Tuple[int, int]:
        """
        Map normalized hand coordinates (0-1) to screen coordinates
        
        Args:
            x: Normalized x coordinate (0-1)
            y: Normalized y coordinate (0-1)
            
        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        # Apply calibrated range
        range_x = self.x_max - self.x_min
        range_y = self.y_max - self.y_min
        
        if range_x <= 0: range_x = 0.1
        if range_y <= 0: range_y = 0.1

        x_adjusted = (x - self.x_min) / range_x
        y_adjusted = (y - self.y_min) / range_y
        
        # Clamp to valid range
        x_adjusted = max(0.0, min(1.0, x_adjusted))
        y_adjusted = max(0.0, min(1.0, y_adjusted))
        
        # Map to screen coordinates with sensitivity
        screen_x = int(x_adjusted * self.screen_width * self.sensitivity)
        screen_y = int(y_adjusted * self.screen_height * self.sensitivity)
        
        # Add monitor offset
        screen_x += self.monitor_offset_x
        screen_y += self.monitor_offset_y
        
        return screen_x, screen_y

    def set_monitor(self, monitor_index: int, width: int, height: int, offset_x: int, offset_y: int):
        """Set target monitor parameters"""
        self.target_monitor = monitor_index
        self.screen_width = width
        self.screen_height = height
        self.monitor_offset_x = offset_x
        self.monitor_offset_y = offset_y
        logger.info(f"Monitor {monitor_index} set as target: {width}x{height} offset({offset_x}, {offset_y})")
    
    def move_cursor(self, x: float, y: float, smooth: bool = True):
        """
        Move cursor to specified position with acceleration
        
        Args:
            x: Normalized x coordinate (0-1)
            y: Normalized y coordinate (0-1)
            smooth: Whether to apply smoothing
        """
        try:
            # Map to screen coordinates
            target_x, target_y = self.map_to_screen(x, y)
            
            # Apply smoothing if enabled
            if smooth:
                target_x, target_y = self.smoothing_filter.filter(target_x, target_y)
            
            # Calculate distance from current mouse position
            curr_x, curr_y = pyautogui.position()
            dx = target_x - curr_x
            dy = target_y - curr_y
            distance = np.sqrt(dx**2 + dy**2)
            
            # Apply acceleration curve
            if distance > 2:  # Threshold to ignore micro-jitter
                # Normalize distance to a factor (0-1 based on screen size)
                diag = np.sqrt(self.screen_width**2 + self.screen_height**2)
                norm_dist = distance / diag
                
                # Apply acceleration: multiplier increases with distance
                # We use a power curve for a more natural feel
                multiplier = 1.0 + (norm_dist * self.acceleration_factor * 15)
                
                # Move relative to current position with acceleration
                new_x = curr_x + dx * multiplier
                new_y = curr_y + dy * multiplier
                
                # Clamp to screen bounds
                new_x = max(0, min(self.screen_width - 1, new_x))
                new_y = max(0, min(self.screen_height - 1, new_y))
                
                pyautogui.moveTo(int(new_x), int(new_y), duration=0)
            
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

    def mouse_down(self, button: str = "left"):
        """Press mouse button down"""
        try:
            pyautogui.mouseDown(button=button)
            logger.debug(f"Mouse down: {button}")
        except Exception as e:
            logger.error(f"Error mouse down: {e}")

    def mouse_up(self, button: str = "left"):
        """Release mouse button"""
        try:
            pyautogui.mouseUp(button=button)
            logger.debug(f"Mouse up: {button}")
        except Exception as e:
            logger.error(f"Error mouse up: {e}")
    
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
