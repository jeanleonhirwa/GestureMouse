"""
Hand tracking module using MediaPipe
Detects hands and extracts 21 landmark points per hand
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HandLandmarks:
    """Container for hand landmark data"""
    
    # MediaPipe hand landmark indices
    WRIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_FINGER_MCP = 5
    INDEX_FINGER_PIP = 6
    INDEX_FINGER_DIP = 7
    INDEX_FINGER_TIP = 8
    MIDDLE_FINGER_MCP = 9
    MIDDLE_FINGER_PIP = 10
    MIDDLE_FINGER_DIP = 11
    MIDDLE_FINGER_TIP = 12
    RING_FINGER_MCP = 13
    RING_FINGER_PIP = 14
    RING_FINGER_DIP = 15
    RING_FINGER_TIP = 16
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20
    
    def __init__(self, landmarks, handedness: str):
        """
        Initialize hand landmarks
        
        Args:
            landmarks: MediaPipe landmarks object
            handedness: "Left" or "Right"
        """
        self.landmarks = landmarks
        self.handedness = handedness
        self.points = []
        
        # Extract landmark points as (x, y, z) tuples
        for lm in landmarks.landmark:
            self.points.append((lm.x, lm.y, lm.z))
    
    def get_landmark(self, index: int) -> Tuple[float, float, float]:
        """
        Get specific landmark point
        
        Args:
            index: Landmark index (0-20)
            
        Returns:
            Tuple of (x, y, z) coordinates (normalized 0-1)
        """
        if 0 <= index < len(self.points):
            return self.points[index]
        return (0.0, 0.0, 0.0)
    
    def get_distance(self, index1: int, index2: int) -> float:
        """
        Calculate Euclidean distance between two landmarks
        
        Args:
            index1: First landmark index
            index2: Second landmark index
            
        Returns:
            Distance between the two landmarks
        """
        p1 = np.array(self.get_landmark(index1))
        p2 = np.array(self.get_landmark(index2))
        return np.linalg.norm(p1 - p2)


class HandDetector:
    """Detects hands in video frames using MediaPipe"""
    
    def __init__(self, 
                 max_hands: int = 1,
                 detection_confidence: float = 0.7,
                 tracking_confidence: float = 0.5):
        """
        Initialize hand detector
        
        Args:
            max_hands: Maximum number of hands to detect
            detection_confidence: Minimum confidence for hand detection
            tracking_confidence: Minimum confidence for hand tracking
        """
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        # Initialize MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        
        logger.info("Hand detector initialized")
    
    def detect(self, frame: np.ndarray) -> Tuple[Optional[HandLandmarks], np.ndarray]:
        """
        Detect hands in a frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Tuple of (hand_landmarks, annotated_frame)
            - hand_landmarks: HandLandmarks object if hand detected, None otherwise
            - annotated_frame: Frame with hand landmarks drawn
        """
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        # Convert back to BGR for OpenCV
        rgb_frame.flags.writeable = True
        annotated_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        
        hand_landmarks = None
        
        # Extract hand landmarks
        if results.multi_hand_landmarks and results.multi_handedness:
            # Get the first detected hand
            landmarks = results.multi_hand_landmarks[0]
            handedness = results.multi_handedness[0].classification[0].label
            
            hand_landmarks = HandLandmarks(landmarks, handedness)
            
            # Draw hand landmarks on frame
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style()
            )
        
        return hand_landmarks, annotated_frame
    
    def is_finger_extended(self, hand: HandLandmarks, finger_tip_idx: int) -> bool:
        """
        Check if a finger is extended
        
        Args:
            hand: HandLandmarks object
            finger_tip_idx: Index of the finger tip landmark
            
        Returns:
            True if finger is extended, False otherwise
        """
        # Get corresponding PIP joint (2 indices before tip)
        pip_idx = finger_tip_idx - 2
        
        # Get y-coordinates (lower y means higher on screen)
        tip_y = hand.get_landmark(finger_tip_idx)[1]
        pip_y = hand.get_landmark(pip_idx)[1]
        
        # Finger is extended if tip is above PIP joint
        return tip_y < pip_y
    
    def count_extended_fingers(self, hand: HandLandmarks) -> int:
        """
        Count number of extended fingers
        
        Args:
            hand: HandLandmarks object
            
        Returns:
            Number of extended fingers (0-5)
        """
        extended = 0
        
        # Check each finger (excluding thumb for now)
        finger_tips = [
            HandLandmarks.INDEX_FINGER_TIP,
            HandLandmarks.MIDDLE_FINGER_TIP,
            HandLandmarks.RING_FINGER_TIP,
            HandLandmarks.PINKY_TIP
        ]
        
        for tip_idx in finger_tips:
            if self.is_finger_extended(hand, tip_idx):
                extended += 1
        
        # Special handling for thumb (check x-coordinate)
        thumb_tip = hand.get_landmark(HandLandmarks.THUMB_TIP)
        thumb_mcp = hand.get_landmark(HandLandmarks.THUMB_MCP)
        
        if hand.handedness == "Right":
            if thumb_tip[0] < thumb_mcp[0]:  # Thumb extended to the left
                extended += 1
        else:
            if thumb_tip[0] > thumb_mcp[0]:  # Thumb extended to the right
                extended += 1
        
        return extended
    
    def close(self):
        """Release MediaPipe resources"""
        if self.hands:
            self.hands.close()
            logger.info("Hand detector closed")
