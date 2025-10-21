"""
Whisparr File Processor Module

Handles processing of video/audio files for subtitle generation.
"""

import os
import logging
from pathlib import Path
from typing import List, Optional, Callable
from .transcriber import Transcriber, TranscriberConfig
from .subtitle_generator import SubtitleGenerator
from .config_loader import Config

logger = logging.getLogger(__name__)


class FileProcessor:
    """Processes video/audio files to generate subtitles"""

    def __init__(self, config: Config):
        """
        Initialize file processor

        Args:
            config: Application configuration
        """
        self.config = config
        self.transcriber_config = TranscriberConfig(
            model_size=config.get("whisper.model_size", "base"),
            language=config.get("whisper.language"),
            task=config.get("whisper.task", "transcribe"),
            device=config.get("whisper.device"),
            compute_type=config.get("whisper.compute_type", "float16")
        )
        self.transcriber = Transcriber(self.transcriber_config)
        self.subtitle_generator = SubtitleGenerator()

    def process_file(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        subtitle_format: Optional[str] = None,
        progress_callback: Optional[Callable] = None
    ) -> str:
        """
        Process a single video/audio file

        Args:
            input_path: Path to input video/audio file
            output_path: Path to output subtitle file (auto-generated if None)
            subtitle_format: Subtitle format (srt or vtt)
            progress_callback: Optional callback for progress updates

        Returns:
            Path to generated subtitle file
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Determine output path
        if output_path is None:
            subtitle_format = subtitle_format or self.config.get("subtitle.format", "srt")
            output_path = input_path.with_suffix(f".{subtitle_format}")
        else:
            output_path = Path(output_path)
            subtitle_format = subtitle_format or output_path.suffix.lstrip('.')

        # Check if output already exists
        if output_path.exists() and not self.config.get("processing.overwrite_existing", False):
            logger.warning(f"Subtitle file already exists: {output_path}")
            logger.warning("Skipping (set overwrite_existing=true to overwrite)")
            return str(output_path)

        logger.info(f"Processing file: {input_path}")

        # Transcribe
        if progress_callback:
            progress_callback("transcribing", 0)

        result = self.transcriber.transcribe(str(input_path))
        segments = self.transcriber.get_segments(result)

        if progress_callback:
            progress_callback("transcribing", 100)

        # Generate subtitles
        if progress_callback:
            progress_callback("generating", 0)

        subtitle_path = self.subtitle_generator.generate(
            segments,
            str(output_path),
            format=subtitle_format
        )

        if progress_callback:
            progress_callback("generating", 100)

        logger.info(f"Subtitle file created: {subtitle_path}")
        return subtitle_path

    def process_directory(
        self,
        input_directory: str,
        output_directory: Optional[str] = None,
        recursive: bool = False,
        progress_callback: Optional[Callable] = None
    ) -> List[str]:
        """
        Process all video/audio files in a directory

        Args:
            input_directory: Directory containing video/audio files
            output_directory: Directory for output subtitle files (same as input if None)
            recursive: Process subdirectories recursively
            progress_callback: Optional callback for progress updates

        Returns:
            List of paths to generated subtitle files
        """
        input_dir = Path(input_directory)

        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")

        output_dir = Path(output_directory) if output_directory else input_dir

        # Get supported file extensions
        video_extensions = self.config.get("processing.video_extensions", [])
        audio_extensions = self.config.get("processing.audio_extensions", [])
        supported_extensions = video_extensions + audio_extensions

        # Find all media files
        media_files = []
        if recursive:
            for ext in supported_extensions:
                media_files.extend(input_dir.rglob(f"*{ext}"))
        else:
            for ext in supported_extensions:
                media_files.extend(input_dir.glob(f"*{ext}"))

        logger.info(f"Found {len(media_files)} media files to process")

        # Process each file
        generated_files = []
        for idx, media_file in enumerate(media_files, start=1):
            try:
                logger.info(f"Processing file {idx}/{len(media_files)}: {media_file.name}")

                # Determine output path (preserve directory structure)
                relative_path = media_file.relative_to(input_dir)
                output_path = output_dir / relative_path.with_suffix(
                    f".{self.config.get('subtitle.format', 'srt')}"
                )

                # Create output directory if needed
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Process file
                subtitle_path = self.process_file(
                    str(media_file),
                    str(output_path),
                    progress_callback=progress_callback
                )

                generated_files.append(subtitle_path)

            except Exception as e:
                logger.error(f"Error processing {media_file}: {e}")
                continue

        logger.info(f"Successfully processed {len(generated_files)}/{len(media_files)} files")
        return generated_files

    def get_supported_extensions(self) -> List[str]:
        """
        Get list of supported file extensions

        Returns:
            List of supported extensions
        """
        video_extensions = self.config.get("processing.video_extensions", [])
        audio_extensions = self.config.get("processing.audio_extensions", [])
        return video_extensions + audio_extensions
