"""
Gesture recognition module
Analyzes hand landmarks to detect specific gestures
"""

import time
import numpy as np
from typing import Optional, Tuple
from enum import Enum
import logging
from .hand_tracker import HandLandmarks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GestureType(Enum):
    """Types of gestures that can be detected"""
    NONE = "none"
    CURSOR_MOVE = "cursor_move"
    LEFT_CLICK = "left_click"
    RIGHT_CLICK = "right_click"
    SCROLL = "scroll"
    DRAG = "drag"


class GestureState:
    """Tracks the state of a gesture over time"""
    
    def __init__(self, debounce_time: float = 0.3):
        """
        Initialize gesture state
        
        Args:
            debounce_time: Minimum time between gesture triggers (seconds)
        """
        self.current_gesture = GestureType.NONE
        self.last_trigger_time = 0
        self.debounce_time = debounce_time
        self.is_pinched = False
        self.scroll_baseline = None
        
    def can_trigger(self) -> bool:
        """Check if enough time has passed to trigger a new gesture"""
        return (time.time() - self.last_trigger_time) >= self.debounce_time
    
    def trigger(self):
        """Mark that a gesture was triggered"""
        self.last_trigger_time = time.time()


class GestureDetector:
    """Detects gestures from hand landmarks"""
    
    def __init__(self,
                 pinch_threshold: float = 0.05,
                 scroll_threshold: float = 0.02,
                 click_debounce: float = 0.3):
        """
        Initialize gesture detector
        
        Args:
            pinch_threshold: Distance threshold for pinch detection
            scroll_threshold: Movement threshold for scroll detection
            click_debounce: Minimum time between clicks (seconds)
        """
        self.pinch_threshold = pinch_threshold
        self.scroll_threshold = scroll_threshold
        self.state = GestureState(debounce_time=click_debounce)
        
        # Previous positions for motion tracking
        self.prev_index_pos = None
        self.prev_scroll_pos = None
        
        logger.info("Gesture detector initialized")
    
    def detect_gesture(self, hand: Optional[HandLandmarks]) -> Tuple[GestureType, dict]:
        """
        Detect gesture from hand landmarks
        
        Args:
            hand: HandLandmarks object
            
        Returns:
            Tuple of (gesture_type, gesture_data)
            - gesture_type: The detected gesture
            - gesture_data: Dictionary with gesture-specific data
        """
        if hand is None:
            self.state.current_gesture = GestureType.NONE
            self.prev_index_pos = None
            self.prev_scroll_pos = None
            return GestureType.NONE, {}
        
        # Get key landmark positions
        thumb_tip = hand.get_landmark(HandLandmarks.THUMB_TIP)
        index_tip = hand.get_landmark(HandLandmarks.INDEX_FINGER_TIP)
        middle_tip = hand.get_landmark(HandLandmarks.MIDDLE_FINGER_TIP)
        
        # Calculate distances
        thumb_index_dist = hand.get_distance(HandLandmarks.THUMB_TIP, 
                                             HandLandmarks.INDEX_FINGER_TIP)
        thumb_middle_dist = hand.get_distance(HandLandmarks.THUMB_TIP,
                                               HandLandmarks.MIDDLE_FINGER_TIP)
        
        # Normalize distances by hand size (wrist to middle finger MCP)
        hand_size = hand.get_distance(HandLandmarks.WRIST, 
                                      HandLandmarks.MIDDLE_FINGER_MCP)
        thumb_index_dist_norm = thumb_index_dist / hand_size if hand_size > 0 else 1.0
        thumb_middle_dist_norm = thumb_middle_dist / hand_size if hand_size > 0 else 1.0
        
        # Check for pinch gestures (clicks)
        is_thumb_index_pinched = thumb_index_dist_norm < self.pinch_threshold
        is_thumb_middle_pinched = thumb_middle_dist_norm < self.pinch_threshold
        
        # Detect left click (thumb-index pinch)
        if is_thumb_index_pinched and not self.state.is_pinched:
            if self.state.can_trigger():
                self.state.is_pinched = True
                self.state.trigger()
                logger.debug("Left click detected")
                return GestureType.LEFT_CLICK, {"position": index_tip[:2]}
        elif not is_thumb_index_pinched:
            self.state.is_pinched = False
        
        # Detect right click (thumb-middle pinch)
        if is_thumb_middle_pinched and self.state.can_trigger():
            self.state.trigger()
            logger.debug("Right click detected")
            return GestureType.RIGHT_CLICK, {"position": middle_tip[:2]}
        
        # Check if index and middle fingers are extended (scroll mode)
        index_extended = self._is_finger_extended(hand, HandLandmarks.INDEX_FINGER_TIP)
        middle_extended = self._is_finger_extended(hand, HandLandmarks.MIDDLE_FINGER_TIP)
        ring_extended = self._is_finger_extended(hand, HandLandmarks.RING_FINGER_TIP)
        pinky_extended = self._is_finger_extended(hand, HandLandmarks.PINKY_TIP)
        
        # Scroll mode: index and middle extended, ring and pinky closed
        if index_extended and middle_extended and not ring_extended and not pinky_extended:
            # Calculate midpoint between index and middle finger
            scroll_pos = (
                (index_tip[0] + middle_tip[0]) / 2,
                (index_tip[1] + middle_tip[1]) / 2
            )
            
            if self.prev_scroll_pos is not None:
                delta_y = scroll_pos[1] - self.prev_scroll_pos[1]
                
                if abs(delta_y) > self.scroll_threshold:
                    self.prev_scroll_pos = scroll_pos
                    logger.debug(f"Scroll detected: delta_y={delta_y}")
                    return GestureType.SCROLL, {"delta_y": delta_y, "position": scroll_pos}
            
            self.prev_scroll_pos = scroll_pos
            return GestureType.SCROLL, {"delta_y": 0, "position": scroll_pos}
        else:
            self.prev_scroll_pos = None
        
        # Default: Cursor control with index finger
        if index_extended:
            position = index_tip[:2]
            
            # Calculate velocity (for motion detection)
            velocity = 0
            if self.prev_index_pos is not None:
                dx = position[0] - self.prev_index_pos[0]
                dy = position[1] - self.prev_index_pos[1]
                velocity = np.sqrt(dx**2 + dy**2)
            
            self.prev_index_pos = position
            
            return GestureType.CURSOR_MOVE, {
                "position": position,
                "velocity": velocity
            }
        
        # No recognized gesture
        self.prev_index_pos = None
        return GestureType.NONE, {}
    
    def _is_finger_extended(self, hand: HandLandmarks, finger_tip_idx: int) -> bool:
        """
        Check if a finger is extended
        
        Args:
            hand: HandLandmarks object
            finger_tip_idx: Index of the finger tip
            
        Returns:
            True if finger is extended
        """
        # Get corresponding PIP joint (2 indices before tip)
        pip_idx = finger_tip_idx - 2
        
        tip_y = hand.get_landmark(finger_tip_idx)[1]
        pip_y = hand.get_landmark(pip_idx)[1]
        
        # Finger is extended if tip is above PIP joint
        return tip_y < pip_y
    
    def reset(self):
        """Reset gesture detector state"""
        self.state = GestureState(debounce_time=self.state.debounce_time)
        self.prev_index_pos = None
        self.prev_scroll_pos = None
        logger.info("Gesture detector reset")
