"""
Whisparr Configuration Loader

Handles loading and managing application configuration.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class Config:
    """Application configuration"""

    DEFAULT_CONFIG = {
        "whisper": {
            "model_size": "base",
            "language": None,
            "task": "transcribe",
            "device": None,
            "compute_type": "float16"
        },
        "translation": {
            "enabled": False,
            "provider": "openai",
            "model": None,
            "api_key": None,
            "target_language": "English",
            "preserve_timing": True,
            "context_aware": True
        },
        "subtitle": {
            "format": "srt",
            "max_line_length": 42,
            "max_lines": 2
        },
        "processing": {
            "watch_directory": None,
            "output_directory": None,
            "video_extensions": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
            "audio_extensions": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"],
            "overwrite_existing": False,
            "auto_detect_language": True
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration

        Args:
            config_path: Path to configuration file (JSON)
        """
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()

        if config_path and os.path.exists(config_path):
            self.load_config(config_path)

    def load_config(self, config_path: str):
        """
        Load configuration from JSON file

        Args:
            config_path: Path to configuration file
        """
        logger.info(f"Loading configuration from: {config_path}")

        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)

            # Deep merge user config with defaults
            self._merge_config(self.config, user_config)
            logger.info("Configuration loaded successfully")

        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            logger.warning("Using default configuration")

    def _merge_config(self, base: Dict, override: Dict):
        """
        Recursively merge override config into base config

        Args:
            base: Base configuration dictionary
            override: Override configuration dictionary
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation

        Args:
            key_path: Configuration key path (e.g., "whisper.model_size")
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation

        Args:
            key_path: Configuration key path (e.g., "whisper.model_size")
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    def save(self, output_path: str):
        """
        Save configuration to JSON file

        Args:
            output_path: Output file path
        """
        logger.info(f"Saving configuration to: {output_path}")

        with open(output_path, 'w') as f:
            json.dump(self.config, f, indent=2)

        logger.info("Configuration saved successfully")

    def to_dict(self) -> Dict:
        """
        Get configuration as dictionary

        Returns:
            Configuration dictionary
        """
        return self.config.copy()
