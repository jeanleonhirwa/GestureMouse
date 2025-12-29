"""
Smoothing and filtering utilities
Various filters for reducing noise in tracking data
"""

import numpy as np
from typing import Optional, Tuple
from collections import deque


class ExponentialMovingAverage:
    """Exponential Moving Average filter"""
    
    def __init__(self, alpha: float = 0.3):
        """
        Initialize EMA filter
        
        Args:
            alpha: Smoothing factor (0-1). Lower = more smoothing
        """
        self.alpha = max(0.0, min(1.0, alpha))
        self.value: Optional[float] = None
    
    def update(self, new_value: float) -> float:
        """
        Update filter with new value
        
        Args:
            new_value: New input value
            
        Returns:
            Filtered value
        """
        if self.value is None:
            self.value = new_value
        else:
            self.value = self.alpha * new_value + (1 - self.alpha) * self.value
        return self.value
    
    def reset(self):
        """Reset filter"""
        self.value = None


class MovingAverageFilter:
    """Simple moving average filter"""
    
    def __init__(self, window_size: int = 5):
        """
        Initialize moving average filter
        
        Args:
            window_size: Number of samples to average
        """
        self.window_size = max(1, window_size)
        self.values = deque(maxlen=window_size)
    
    def update(self, new_value: float) -> float:
        """
        Update filter with new value
        
        Args:
            new_value: New input value
            
        Returns:
            Filtered value (average of window)
        """
        self.values.append(new_value)
        return sum(self.values) / len(self.values)
    
    def reset(self):
        """Reset filter"""
        self.values.clear()


class OneEuroFilter:
    """
    One Euro Filter for low-latency smoothing
    Good for tracking applications
    Reference: http://cristal.univ-lille.fr/~casiez/1euro/
    """
    
    def __init__(self,
                 min_cutoff: float = 1.0,
                 beta: float = 0.007,
                 d_cutoff: float = 1.0):
        """
        Initialize One Euro Filter
        
        Args:
            min_cutoff: Minimum cutoff frequency
            beta: Speed coefficient
            d_cutoff: Cutoff frequency for derivative
        """
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        
        self.x_prev: Optional[float] = None
        self.dx_prev: float = 0.0
        self.t_prev: Optional[float] = None
    
    def update(self, x: float, t: float) -> float:
        """
        Update filter with new value
        
        Args:
            x: New input value
            t: Timestamp (seconds)
            
        Returns:
            Filtered value
        """
        if self.x_prev is None:
            self.x_prev = x
            self.t_prev = t
            return x
        
        # Calculate time delta
        dt = t - self.t_prev
        if dt <= 0:
            dt = 0.001  # Prevent division by zero
        
        # Calculate derivative
        dx = (x - self.x_prev) / dt
        
        # Smooth derivative
        alpha_d = self._smoothing_factor(dt, self.d_cutoff)
        dx_smoothed = self._exponential_smoothing(alpha_d, dx, self.dx_prev)
        
        # Calculate cutoff frequency
        cutoff = self.min_cutoff + self.beta * abs(dx_smoothed)
        
        # Smooth value
        alpha = self._smoothing_factor(dt, cutoff)
        x_smoothed = self._exponential_smoothing(alpha, x, self.x_prev)
        
        # Update state
        self.x_prev = x_smoothed
        self.dx_prev = dx_smoothed
        self.t_prev = t
        
        return x_smoothed
    
    def _smoothing_factor(self, dt: float, cutoff: float) -> float:
        """Calculate smoothing factor"""
        r = 2 * np.pi * cutoff * dt
        return r / (r + 1)
    
    def _exponential_smoothing(self, alpha: float, x: float, x_prev: float) -> float:
        """Apply exponential smoothing"""
        return alpha * x + (1 - alpha) * x_prev
    
    def reset(self):
        """Reset filter"""
        self.x_prev = None
        self.dx_prev = 0.0
        self.t_prev = None


class KalmanFilter:
    """Simple 1D Kalman filter for position tracking"""
    
    def __init__(self,
                 process_variance: float = 1e-5,
                 measurement_variance: float = 1e-1):
        """
        Initialize Kalman filter
        
        Args:
            process_variance: Process noise variance
            measurement_variance: Measurement noise variance
        """
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        
        self.estimate: Optional[float] = None
        self.error_estimate: float = 1.0
    
    def update(self, measurement: float) -> float:
        """
        Update filter with new measurement
        
        Args:
            measurement: New measured value
            
        Returns:
            Filtered estimate
        """
        if self.estimate is None:
            self.estimate = measurement
            return measurement
        
        # Prediction
        prediction = self.estimate
        error_prediction = self.error_estimate + self.process_variance
        
        # Update
        kalman_gain = error_prediction / (error_prediction + self.measurement_variance)
        self.estimate = prediction + kalman_gain * (measurement - prediction)
        self.error_estimate = (1 - kalman_gain) * error_prediction
        
        return self.estimate
    
    def reset(self):
        """Reset filter"""
        self.estimate = None
        self.error_estimate = 1.0
