"""
Tests for subtitle_generator module
"""

import pytest
from pathlib import Path
from src.subtitle_generator import SubtitleGenerator


class TestSubtitleGenerator:
    """Test cases for SubtitleGenerator class"""

    def setup_method(self):
        """Setup test fixtures"""
        self.generator = SubtitleGenerator()
        self.sample_segments = [
            {
                "start": 0.0,
                "end": 2.5,
                "text": "Hello, this is a test."
            },
            {
                "start": 2.5,
                "end": 5.0,
                "text": "This is the second segment."
            }
        ]

    def test_format_timestamp_srt(self):
        """Test SRT timestamp formatting"""
        assert self.generator.format_timestamp_srt(0.0) == "00:00:00,000"
        assert self.generator.format_timestamp_srt(1.5) == "00:00:01,500"
        assert self.generator.format_timestamp_srt(61.234) == "00:01:01,234"
        assert self.generator.format_timestamp_srt(3661.0) == "01:01:01,000"

    def test_format_timestamp_vtt(self):
        """Test VTT timestamp formatting"""
        assert self.generator.format_timestamp_vtt(0.0) == "00:00:00.000"
        assert self.generator.format_timestamp_vtt(1.5) == "00:00:01.500"
        assert self.generator.format_timestamp_vtt(61.234) == "00:01:01.234"
        assert self.generator.format_timestamp_vtt(3661.0) == "01:01:01.000"

    def test_generate_srt(self, tmp_path):
        """Test SRT file generation"""
        output_path = tmp_path / "test.srt"
        result = self.generator.generate_srt(self.sample_segments, str(output_path))

        assert Path(result).exists()
        content = Path(result).read_text()
        assert "1\n" in content
        assert "00:00:00,000 --> 00:00:02,500" in content
        assert "Hello, this is a test." in content

    def test_generate_vtt(self, tmp_path):
        """Test VTT file generation"""
        output_path = tmp_path / "test.vtt"
        result = self.generator.generate_vtt(self.sample_segments, str(output_path))

        assert Path(result).exists()
        content = Path(result).read_text()
        assert "WEBVTT" in content
        assert "00:00:00.000 --> 00:00:02.500" in content
        assert "Hello, this is a test." in content

    def test_generate_unsupported_format(self, tmp_path):
        """Test error handling for unsupported format"""
        output_path = tmp_path / "test.xyz"
        with pytest.raises(ValueError, match="Unsupported subtitle format"):
            self.generator.generate(self.sample_segments, str(output_path), format="xyz")
