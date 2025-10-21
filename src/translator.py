"""
Whisparr Translator Module

Handles translation of transcribed text using LLM APIs.
"""

import os
import logging
from typing import List, Dict, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"


class TranslatorConfig:
    """Configuration for the translator"""

    def __init__(
        self,
        provider: str = "openai",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        target_language: str = "English",
        preserve_timing: bool = True,
        context_aware: bool = True
    ):
        """
        Initialize translator configuration

        Args:
            provider: LLM provider (openai, anthropic, local)
            model: Model name (e.g., gpt-4, claude-3-sonnet)
            api_key: API key for the provider
            target_language: Target language for translation
            preserve_timing: Keep original timing segments
            context_aware: Use context from previous segments
        """
        self.provider = provider
        self.model = model or self._get_default_model(provider)
        self.api_key = api_key or self._get_api_key_from_env(provider)
        self.target_language = target_language
        self.preserve_timing = preserve_timing
        self.context_aware = context_aware

    def _get_default_model(self, provider: str) -> str:
        """Get default model for provider"""
        defaults = {
            "openai": "gpt-4o-mini",
            "anthropic": "claude-3-5-sonnet-20241022",
            "local": "llama2"
        }
        return defaults.get(provider, "gpt-4o-mini")

    def _get_api_key_from_env(self, provider: str) -> Optional[str]:
        """Get API key from environment variables"""
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY"
        }
        env_var = env_vars.get(provider)
        return os.getenv(env_var) if env_var else None


class Translator:
    """Handles translation of transcribed text using LLMs"""

    def __init__(self, config: TranslatorConfig):
        """
        Initialize the translator

        Args:
            config: Translator configuration
        """
        self.config = config
        self.client = None
        logger.info(f"Initializing translator with provider: {config.provider}, model: {config.model}")

    def _init_openai_client(self):
        """Initialize OpenAI client"""
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.config.api_key)
            logger.info("OpenAI client initialized")
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI client: {e}")

    def _init_anthropic_client(self):
        """Initialize Anthropic client"""
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.config.api_key)
            logger.info("Anthropic client initialized")
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
        except Exception as e:
            raise Exception(f"Failed to initialize Anthropic client: {e}")

    def _ensure_client(self):
        """Ensure LLM client is initialized"""
        if self.client is None:
            if self.config.provider == "openai":
                self._init_openai_client()
            elif self.config.provider == "anthropic":
                self._init_anthropic_client()
            else:
                raise ValueError(f"Unsupported provider: {self.config.provider}")

    def _translate_with_openai(self, text: str, context: Optional[str] = None) -> str:
        """Translate text using OpenAI"""
        prompt = self._build_translation_prompt(text, context)

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": f"You are a professional translator. Translate the following text to {self.config.target_language}. Preserve the meaning, tone, and style. Only return the translated text, nothing else."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()

    def _translate_with_anthropic(self, text: str, context: Optional[str] = None) -> str:
        """Translate text using Anthropic Claude"""
        prompt = self._build_translation_prompt(text, context)

        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": f"You are a professional translator. Translate the following text to {self.config.target_language}. Preserve the meaning, tone, and style. Only return the translated text, nothing else.\n\n{prompt}"}
            ],
            temperature=0.3
        )

        return response.content[0].text.strip()

    def _build_translation_prompt(self, text: str, context: Optional[str] = None) -> str:
        """Build translation prompt with optional context"""
        if context and self.config.context_aware:
            return f"Previous context:\n{context}\n\nTranslate this text:\n{text}"
        return text

    def translate_text(self, text: str, context: Optional[str] = None) -> str:
        """
        Translate a single text string

        Args:
            text: Text to translate
            context: Optional context from previous translations

        Returns:
            Translated text
        """
        self._ensure_client()

        logger.debug(f"Translating text: {text[:50]}...")

        if self.config.provider == "openai":
            return self._translate_with_openai(text, context)
        elif self.config.provider == "anthropic":
            return self._translate_with_anthropic(text, context)
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

    def translate_segments(self, segments: List[Dict]) -> List[Dict]:
        """
        Translate all segments with context awareness

        Args:
            segments: List of transcription segments

        Returns:
            List of translated segments
        """
        self._ensure_client()

        logger.info(f"Translating {len(segments)} segments to {self.config.target_language}")

        translated_segments = []
        context = ""

        for idx, segment in enumerate(segments, 1):
            original_text = segment['text'].strip()

            # Translate with context
            translated_text = self.translate_text(original_text, context if self.config.context_aware else None)

            # Update context for next segment
            if self.config.context_aware:
                context = f"{context}\n{translated_text}"[-500:]  # Keep last 500 chars

            # Create translated segment
            translated_segment = segment.copy()
            translated_segment['text'] = translated_text
            translated_segment['original_text'] = original_text

            translated_segments.append(translated_segment)

            logger.debug(f"Translated segment {idx}/{len(segments)}: {original_text[:30]}... -> {translated_text[:30]}...")

        logger.info(f"Translation complete: {len(translated_segments)} segments translated")
        return translated_segments

    def translate_batch(self, segments: List[Dict], batch_size: int = 10) -> List[Dict]:
        """
        Translate segments in batches for efficiency

        Args:
            segments: List of transcription segments
            batch_size: Number of segments to translate together

        Returns:
            List of translated segments
        """
        logger.info(f"Batch translating {len(segments)} segments (batch_size={batch_size})")

        translated_segments = []

        for i in range(0, len(segments), batch_size):
            batch = segments[i:i + batch_size]

            # Combine batch texts
            combined_text = "\n\n".join([f"[{j+1}] {seg['text'].strip()}" for j, seg in enumerate(batch)])

            # Translate batch
            translated_text = self.translate_text(combined_text)

            # Split translated text back into segments
            translated_lines = translated_text.split("\n\n")

            for j, segment in enumerate(batch):
                # Try to extract translated text for this segment
                if j < len(translated_lines):
                    # Remove segment number if present
                    translated = translated_lines[j]
                    if translated.startswith(f"[{j+1}]"):
                        translated = translated[len(f"[{j+1}]"):].strip()

                    translated_segment = segment.copy()
                    translated_segment['text'] = translated
                    translated_segment['original_text'] = segment['text'].strip()
                    translated_segments.append(translated_segment)
                else:
                    # Fallback: keep original
                    translated_segments.append(segment)

            logger.info(f"Batch {i//batch_size + 1} complete ({len(batch)} segments)")

        return translated_segments
