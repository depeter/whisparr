"""
Tests for config_loader module
"""

import pytest
import json
from pathlib import Path
from src.config_loader import Config


class TestConfig:
    """Test cases for Config class"""

    def test_default_config(self):
        """Test default configuration is loaded"""
        config = Config()
        assert config.get("whisper.model_size") == "base"
        assert config.get("subtitle.format") == "srt"
        assert config.get("logging.level") == "INFO"

    def test_get_nested_value(self):
        """Test getting nested configuration values"""
        config = Config()
        assert config.get("whisper.model_size") == "base"
        assert config.get("subtitle.max_line_length") == 42

    def test_get_with_default(self):
        """Test getting value with default fallback"""
        config = Config()
        assert config.get("nonexistent.key", "default") == "default"

    def test_set_value(self):
        """Test setting configuration values"""
        config = Config()
        config.set("whisper.model_size", "medium")
        assert config.get("whisper.model_size") == "medium"

    def test_set_new_nested_value(self):
        """Test setting a new nested value"""
        config = Config()
        config.set("new.nested.value", 123)
        assert config.get("new.nested.value") == 123

    def test_load_config(self, tmp_path):
        """Test loading configuration from file"""
        config_data = {
            "whisper": {
                "model_size": "large"
            }
        }
        config_path = tmp_path / "config.json"
        with open(config_path, 'w') as f:
            json.dump(config_data, f)

        config = Config(str(config_path))
        assert config.get("whisper.model_size") == "large"
        # Check that defaults are still present
        assert config.get("subtitle.format") == "srt"

    def test_save_config(self, tmp_path):
        """Test saving configuration to file"""
        config = Config()
        config.set("whisper.model_size", "small")

        output_path = tmp_path / "output.json"
        config.save(str(output_path))

        # Verify file was created and has correct content
        assert output_path.exists()
        with open(output_path) as f:
            saved_config = json.load(f)
        assert saved_config["whisper"]["model_size"] == "small"

    def test_to_dict(self):
        """Test converting config to dictionary"""
        config = Config()
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert "whisper" in config_dict
        assert "subtitle" in config_dict
