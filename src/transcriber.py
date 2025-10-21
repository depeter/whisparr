"""
Whisparr Transcriber Module

Handles audio/video transcription using OpenAI's Whisper model.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, List
import whisper

logger = logging.getLogger(__name__)


class TranscriberConfig:
    """Configuration for the transcriber"""

    def __init__(
        self,
        model_size: str = "base",
        language: Optional[str] = None,
        task: str = "transcribe",
        device: Optional[str] = None,
        compute_type: str = "float16"
    ):
        """
        Initialize transcriber configuration

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            language: Source language (None for auto-detect)
            task: Task type (transcribe or translate)
            device: Device to use (cuda, cpu, or None for auto)
            compute_type: Computation precision (float16, int8, float32)
        """
        self.model_size = model_size
        self.language = language
        self.task = task
        self.device = device
        self.compute_type = compute_type


class Transcriber:
    """Handles transcription of audio/video files using Whisper"""

    def __init__(self, config: TranscriberConfig):
        """
        Initialize the transcriber

        Args:
            config: Transcriber configuration
        """
        self.config = config
        self.model = None
        logger.info(f"Initializing transcriber with model size: {config.model_size}")

    def load_model(self):
        """Load the Whisper model"""
        if self.model is None:
            logger.info(f"Loading Whisper model: {self.config.model_size}")
            self.model = whisper.load_model(
                self.config.model_size,
                device=self.config.device
            )
            logger.info("Model loaded successfully")

    def transcribe(
        self,
        audio_path: str,
        **kwargs
    ) -> Dict:
        """
        Transcribe an audio or video file

        Args:
            audio_path: Path to audio/video file
            **kwargs: Additional arguments to pass to whisper.transcribe()

        Returns:
            Dictionary containing transcription results with segments
        """
        self.load_model()

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        logger.info(f"Transcribing: {audio_path}")

        # Prepare transcription options
        options = {
            "language": self.config.language,
            "task": self.config.task,
            "verbose": False,
        }
        options.update(kwargs)

        # Remove None values
        options = {k: v for k, v in options.items() if v is not None}

        # Transcribe
        result = self.model.transcribe(audio_path, **options)

        logger.info(f"Transcription complete. Detected language: {result.get('language', 'unknown')}")
        logger.info(f"Found {len(result.get('segments', []))} segments")

        return result

    def get_segments(self, result: Dict) -> List[Dict]:
        """
        Extract segments from transcription result

        Args:
            result: Transcription result dictionary

        Returns:
            List of segment dictionaries
        """
        return result.get("segments", [])

    def get_text(self, result: Dict) -> str:
        """
        Extract full text from transcription result

        Args:
            result: Transcription result dictionary

        Returns:
            Full transcribed text
        """
        return result.get("text", "").strip()
