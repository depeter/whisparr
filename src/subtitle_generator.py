"""
Whisparr Subtitle Generator Module

Converts transcription results into subtitle files (SRT, VTT formats).
"""

import os
import logging
from pathlib import Path
from typing import List, Dict
from datetime import timedelta

logger = logging.getLogger(__name__)


class SubtitleGenerator:
    """Generates subtitle files from transcription segments"""

    @staticmethod
    def format_timestamp_srt(seconds: float) -> str:
        """
        Format timestamp for SRT format (HH:MM:SS,mmm)

        Args:
            seconds: Time in seconds

        Returns:
            Formatted timestamp string
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    @staticmethod
    def format_timestamp_vtt(seconds: float) -> str:
        """
        Format timestamp for WebVTT format (HH:MM:SS.mmm)

        Args:
            seconds: Time in seconds

        Returns:
            Formatted timestamp string
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        secs = int(td.total_seconds() % 60)
        millis = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

    def generate_srt(
        self,
        segments: List[Dict],
        output_path: str,
        max_line_length: int = 42,
        max_lines: int = 2
    ) -> str:
        """
        Generate SRT subtitle file

        Args:
            segments: List of transcription segments
            output_path: Output file path
            max_line_length: Maximum characters per line
            max_lines: Maximum lines per subtitle

        Returns:
            Path to generated SRT file
        """
        logger.info(f"Generating SRT file: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as f:
            for idx, segment in enumerate(segments, start=1):
                start_time = self.format_timestamp_srt(segment['start'])
                end_time = self.format_timestamp_srt(segment['end'])
                text = segment['text'].strip()

                # Write subtitle entry
                f.write(f"{idx}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n")
                f.write("\n")

        logger.info(f"SRT file generated with {len(segments)} entries")
        return output_path

    def generate_vtt(
        self,
        segments: List[Dict],
        output_path: str,
        max_line_length: int = 42,
        max_lines: int = 2
    ) -> str:
        """
        Generate WebVTT subtitle file

        Args:
            segments: List of transcription segments
            output_path: Output file path
            max_line_length: Maximum characters per line
            max_lines: Maximum lines per subtitle

        Returns:
            Path to generated VTT file
        """
        logger.info(f"Generating VTT file: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")

            for idx, segment in enumerate(segments, start=1):
                start_time = self.format_timestamp_vtt(segment['start'])
                end_time = self.format_timestamp_vtt(segment['end'])
                text = segment['text'].strip()

                # Write subtitle entry
                f.write(f"{idx}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n")
                f.write("\n")

        logger.info(f"VTT file generated with {len(segments)} entries")
        return output_path

    def generate(
        self,
        segments: List[Dict],
        output_path: str,
        format: str = "srt"
    ) -> str:
        """
        Generate subtitle file in specified format

        Args:
            segments: List of transcription segments
            output_path: Output file path
            format: Subtitle format (srt or vtt)

        Returns:
            Path to generated subtitle file
        """
        format = format.lower()

        if format == "srt":
            return self.generate_srt(segments, output_path)
        elif format == "vtt":
            return self.generate_vtt(segments, output_path)
        else:
            raise ValueError(f"Unsupported subtitle format: {format}")
