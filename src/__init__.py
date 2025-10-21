"""
Whisparr - AI Subtitles Generator

An automated subtitle generation tool using OpenAI's Whisper model.
Similar to Sonarr/Radarr but for subtitle automation.
"""

__version__ = "0.1.0"

from .transcriber import Transcriber, TranscriberConfig
from .subtitle_generator import SubtitleGenerator
from .translator import Translator, TranslatorConfig, LLMProvider
from .config_loader import Config
from .processor import FileProcessor

__all__ = [
    "Transcriber",
    "TranscriberConfig",
    "SubtitleGenerator",
    "Translator",
    "TranslatorConfig",
    "LLMProvider",
    "Config",
    "FileProcessor",
]
