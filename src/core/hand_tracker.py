"""
Hand tracking module using MediaPipe
Detects hands and extracts 21 landmark points per hand
"""

import cv2
import numpy as np
from typing import Optional, List, Tuple
import logging
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

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
        
        # Download model if needed
        import urllib.request
        import os
        
        model_path = "hand_landmarker.task"
        if not os.path.exists(model_path):
            logger.info("Downloading hand landmarker model...")
            model_url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            try:
                urllib.request.urlretrieve(model_url, model_path)
                logger.info("Model downloaded successfully")
            except Exception as e:
                logger.error(f"Failed to download model: {e}")
                raise
        
        # Create hand landmarker options
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_confidence,
            min_hand_presence_confidence=tracking_confidence,
            min_tracking_confidence=tracking_confidence
        )
        
        # Create the hand landmarker
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.frame_timestamp_ms = 0
        
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
        
        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Detect hand landmarks
        self.frame_timestamp_ms += 33  # Approximately 30 FPS
        results = self.detector.detect_for_video(mp_image, self.frame_timestamp_ms)
        
        # Create annotated frame
        annotated_frame = frame.copy()
        
        hand_landmarks = None
        
        # Extract hand landmarks
        if results.hand_landmarks and results.handedness:
            # Get the first detected hand
            landmarks = results.hand_landmarks[0]
            handedness = results.handedness[0][0].category_name
            
            # Convert to our HandLandmarks format
            hand_landmarks = self._create_hand_landmarks(landmarks, handedness)
            
            # Draw hand landmarks on frame
            self._draw_landmarks(annotated_frame, landmarks)
        
        return hand_landmarks, annotated_frame
    
    def _create_hand_landmarks(self, landmarks, handedness: str) -> HandLandmarks:
        """Convert MediaPipe landmarks to our format"""
        # Create a simple object to hold landmarks
        class LandmarkList:
            def __init__(self, lm_list):
                self.landmark = lm_list
        
        return HandLandmarks(LandmarkList(landmarks), handedness)
    
    def _draw_landmarks(self, image: np.ndarray, hand_landmarks):
        """Draw hand landmarks on the image"""
        height, width, _ = image.shape
        
        # Convert normalized coordinates to pixel coordinates
        landmark_points = []
        for landmark in hand_landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            landmark_points.append((x, y))
        
        # Draw connections
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),  # Index
            (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
            (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
            (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
            (5, 9), (9, 13), (13, 17)  # Palm
        ]
        
        for connection in connections:
            start_point = landmark_points[connection[0]]
            end_point = landmark_points[connection[1]]
            cv2.line(image, start_point, end_point, (0, 255, 0), 2)
        
        # Draw landmarks
        for point in landmark_points:
            cv2.circle(image, point, 5, (0, 0, 255), -1)
    
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
        if self.detector:
            self.detector.close()
            logger.info("Hand detector closed")
