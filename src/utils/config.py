"""
Configuration management module
Handles loading, saving, and managing application settings
"""

import json
import os
from typing import Any, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration"""
    
    DEFAULT_CONFIG = {
        "camera": {
            "index": 0,
            "width": 640,
            "height": 480,
            "mirror": True
        },
        "tracking": {
            "max_hands": 1,
            "detection_confidence": 0.7,
            "tracking_confidence": 0.5
        },
        "gestures": {
            "cursor_control_enabled": True,
            "left_click_enabled": True,
            "right_click_enabled": True,
            "scroll_enabled": True,
            "pinch_threshold": 0.05,
            "scroll_threshold": 0.02,
            "click_debounce": 0.3
        },
        "mouse": {
            "sensitivity": 1.5,
            "smoothing": 0.3,
            "scroll_sensitivity": 5.0
        },
        "ui": {
            "show_camera_feed": True,
            "show_landmarks": True,
            "start_minimized": False
        }
    }
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize configuration manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self._deep_merge(self.config, loaded_config)
                logger.info(f"Configuration loaded from {self.config_path}")
            except Exception as e:
                logger.error(f"Error loading config: {e}. Using defaults.")
        else:
            logger.info("No config file found. Using default configuration.")
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: Any):
        """
        Set configuration value
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section
        
        Args:
            section: Section name
            
        Returns:
            Dictionary of section configuration
        """
        return self.config.get(section, {})
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        logger.info("Configuration reset to defaults")
    
    def _deep_merge(self, base: dict, update: dict):
        """
        Deep merge two dictionaries
        
        Args:
            base: Base dictionary to merge into
            update: Dictionary with updates
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
