# Whisparr - AI Subtitles Generator

Whisparr is an automated subtitle generation tool powered by OpenAI's Whisper model. Named in the spirit of Sonarr/Radarr, it provides intelligent, automated subtitle generation for your video and audio files.

## Features

- **Automatic Transcription**: Uses OpenAI's Whisper model for accurate speech-to-text conversion
- **Multiple Subtitle Formats**: Generates SRT and WebVTT subtitle files
- **Batch Processing**: Process entire directories of video/audio files
- **Flexible Configuration**: JSON-based configuration with CLI overrides
- **Language Support**: Auto-detect or specify source language
- **Multiple Model Sizes**: Choose from tiny, base, small, medium, or large Whisper models
- **GPU Acceleration**: Optional CUDA support for faster processing

## Installation

### Prerequisites

- Python 3.8+
- FFmpeg (required by Whisper for audio processing)

### Install FFmpeg

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### Install Whisparr

```bash
# Clone the repository
git clone <repository-url>
cd whisparr

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Process a Single File

```bash
./whisparr.py file video.mp4
```

This will generate `video.srt` in the same directory.

### Process with Specific Options

```bash
# Use medium model with English language
./whisparr.py file video.mp4 --model medium --language en

# Generate WebVTT format
./whisparr.py file video.mp4 --format vtt

# Specify output path
./whisparr.py file video.mp4 -o subtitles/video.srt
```

### Process Entire Directory

```bash
# Process all videos in a directory
./whisparr.py directory /path/to/videos

# Process recursively including subdirectories
./whisparr.py directory /path/to/videos --recursive

# Overwrite existing subtitle files
./whisparr.py directory /path/to/videos --overwrite
```

## Configuration

### Generate Configuration File

```bash
./whisparr.py config generate -o config.json
```

### View Current Configuration

```bash
./whisparr.py config show
```

### Sample Configuration

```json
{
  "whisper": {
    "model_size": "base",
    "language": null,
    "task": "transcribe",
    "device": null,
    "compute_type": "float16"
  },
  "subtitle": {
    "format": "srt",
    "max_line_length": 42,
    "max_lines": 2
  },
  "processing": {
    "watch_directory": null,
    "output_directory": null,
    "video_extensions": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "audio_extensions": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"],
    "overwrite_existing": false,
    "auto_detect_language": true
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
```

### Use Configuration File

```bash
./whisparr.py file video.mp4 --config config.json
```

## CLI Reference

### Commands

#### `file` - Process a single file

```bash
whisparr.py file INPUT [OPTIONS]

Options:
  -o, --output PATH          Output subtitle file path
  -m, --model MODEL          Whisper model size (tiny|base|small|medium|large)
  -l, --language LANG        Source language code (e.g., en, es, fr)
  -f, --format FORMAT        Subtitle format (srt|vtt)
  -d, --device DEVICE        Device to use (cpu|cuda)
  -c, --config PATH          Configuration file path
  --log-level LEVEL          Logging level (DEBUG|INFO|WARNING|ERROR)
```

#### `directory` - Process all files in a directory

```bash
whisparr.py directory INPUT [OPTIONS]

Options:
  -o, --output PATH          Output directory
  -r, --recursive            Process subdirectories
  -m, --model MODEL          Whisper model size (tiny|base|small|medium|large)
  -l, --language LANG        Source language code (e.g., en, es, fr)
  -f, --format FORMAT        Subtitle format (srt|vtt)
  -d, --device DEVICE        Device to use (cpu|cuda)
  -c, --config PATH          Configuration file path
  --overwrite                Overwrite existing subtitle files
  --log-level LEVEL          Logging level (DEBUG|INFO|WARNING|ERROR)
```

#### `config` - Configuration management

```bash
whisparr.py config ACTION [OPTIONS]

Actions:
  generate                   Generate a default configuration file
  show                       Show current configuration

Options:
  -o, --output PATH          Output path for config file
  -c, --config PATH          Configuration file to show
```

## Whisper Model Sizes

| Model  | Parameters | Required VRAM | Relative Speed |
|--------|------------|---------------|----------------|
| tiny   | 39 M       | ~1 GB         | ~32x           |
| base   | 74 M       | ~1 GB         | ~16x           |
| small  | 244 M      | ~2 GB         | ~6x            |
| medium | 769 M      | ~5 GB         | ~2x            |
| large  | 1550 M     | ~10 GB        | 1x             |

**Recommendation**:
- `base` for balanced speed and accuracy
- `small` or `medium` for better accuracy
- `large` for maximum accuracy (requires GPU)

## Supported File Formats

### Video
- MP4, MKV, AVI, MOV, WMV, FLV, WebM

### Audio
- MP3, WAV, FLAC, AAC, M4A, OGG

## Examples

### Basic Usage

```bash
# Generate subtitles for a movie
./whisparr.py file movie.mp4

# Generate subtitles for multiple episodes
./whisparr.py directory /media/TV\ Shows/Season\ 1/ --recursive
```

### Advanced Usage

```bash
# High-accuracy transcription with medium model
./whisparr.py file interview.mp4 --model medium --language en

# Batch process with GPU acceleration
./whisparr.py directory /videos --device cuda --model small --recursive

# Generate WebVTT for web playback
./whisparr.py file presentation.mp4 --format vtt
```

## Architecture

```
whisparr/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── transcriber.py           # Whisper transcription logic
│   ├── subtitle_generator.py   # Subtitle file generation (SRT/VTT)
│   ├── config_loader.py         # Configuration management
│   └── processor.py             # File processing orchestration
├── config/                      # Configuration files
├── tests/                       # Unit tests
├── docs/                        # Additional documentation
├── whisparr.py                  # CLI entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Code Style

This project follows PEP 8 style guidelines.

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

## Troubleshooting

### FFmpeg Not Found

If you see an error about FFmpeg not being found:
```bash
sudo apt update && sudo apt install ffmpeg
```

### Out of Memory (CUDA)

If you encounter CUDA out-of-memory errors:
- Use a smaller model: `--model small` or `--model base`
- Use CPU instead: `--device cpu`

### Poor Transcription Quality

- Try a larger model: `--model medium` or `--model large`
- Specify the source language: `--language en`
- Ensure audio quality is good (clear speech, minimal background noise)

## Performance Tips

1. **Use GPU**: Add `--device cuda` for significantly faster processing
2. **Batch Processing**: Process multiple files at once using the `directory` command
3. **Model Selection**: Start with `base` model and only upgrade if accuracy is insufficient
4. **Language Specification**: Specify `--language` for faster processing (skips language detection)

## Future Enhancements

- [ ] Watch mode for automatic processing of new files
- [ ] Web interface for easier management
- [ ] Docker container for easy deployment
- [ ] Integration with media servers (Plex, Jellyfin)
- [ ] Translation support (generate subtitles in different languages)
- [ ] Speaker diarization (identify different speakers)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- OpenAI's Whisper for the excellent speech recognition model
- Inspired by the Sonarr/Radarr naming convention for automated media tools

## Support

For issues, questions, or feature requests, please open an issue on the project repository.
