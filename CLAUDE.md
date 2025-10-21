# CLAUDE.md - Whisparr Project

This file provides guidance to Claude Code when working with the Whisparr codebase.

## Project Overview

Whisparr is an AI-powered subtitle generation tool using OpenAI's Whisper model. It's designed in the spirit of Sonarr/Radarr for automated media management.

**Location**: `/home/peter/work/whisparr/`

## Architecture

### Core Components

```
src/
├── transcriber.py          # Whisper model integration and transcription
├── subtitle_generator.py   # SRT/VTT subtitle file generation
├── config_loader.py        # JSON-based configuration management
├── processor.py            # File/directory processing orchestration
└── __init__.py             # Package exports
```

### Data Flow

```
Input File → Transcriber (Whisper) → Segments → Subtitle Generator → Output File (.srt/.vtt)
```

## Key Classes

### `Transcriber` (src/transcriber.py)
- **Purpose**: Wraps OpenAI Whisper model for audio/video transcription
- **Key Methods**:
  - `load_model()`: Lazy-loads Whisper model
  - `transcribe(audio_path)`: Transcribes audio/video file
  - `get_segments(result)`: Extracts timestamped segments
  - `get_text(result)`: Extracts full text

### `SubtitleGenerator` (src/subtitle_generator.py)
- **Purpose**: Converts transcription segments to subtitle files
- **Key Methods**:
  - `generate_srt(segments, output_path)`: Creates SRT file
  - `generate_vtt(segments, output_path)`: Creates WebVTT file
  - `format_timestamp_srt(seconds)`: Formats time for SRT (HH:MM:SS,mmm)
  - `format_timestamp_vtt(seconds)`: Formats time for VTT (HH:MM:SS.mmm)

### `Config` (src/config_loader.py)
- **Purpose**: Manages application configuration with defaults
- **Key Methods**:
  - `load_config(config_path)`: Loads JSON config
  - `get(key_path, default)`: Gets value using dot notation (e.g., "whisper.model_size")
  - `set(key_path, value)`: Sets value using dot notation
  - `save(output_path)`: Saves config to JSON

### `FileProcessor` (src/processor.py)
- **Purpose**: Orchestrates file processing workflow
- **Key Methods**:
  - `process_file(input_path, output_path)`: Process single file
  - `process_directory(input_dir, output_dir, recursive)`: Batch process
  - `get_supported_extensions()`: Returns list of supported file types

## Configuration Schema

```json
{
  "whisper": {
    "model_size": "tiny|base|small|medium|large",
    "language": "en|es|fr|...|null (auto-detect)",
    "task": "transcribe|translate",
    "device": "cpu|cuda|null (auto)",
    "compute_type": "float16|int8|float32"
  },
  "subtitle": {
    "format": "srt|vtt",
    "max_line_length": 42,
    "max_lines": 2
  },
  "processing": {
    "watch_directory": null,
    "output_directory": null,
    "video_extensions": [...],
    "audio_extensions": [...],
    "overwrite_existing": false,
    "auto_detect_language": true
  },
  "logging": {
    "level": "DEBUG|INFO|WARNING|ERROR",
    "format": "%(asctime)s - ..."
  }
}
```

## CLI Interface

**Entry Point**: `whisparr.py`

### Commands

1. **file**: Process single file
   - Example: `./whisparr.py file video.mp4 --model medium --language en`

2. **directory**: Batch process directory
   - Example: `./whisparr.py directory /videos --recursive --overwrite`

3. **config**: Configuration management
   - Generate: `./whisparr.py config generate -o config.json`
   - Show: `./whisparr.py config show`

## Development Workflow

### Setup Environment

```bash
cd /home/peter/work/whisparr
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Testing Changes

```bash
# Test single file processing
./whisparr.py file test.mp4 --log-level DEBUG

# Test directory processing
./whisparr.py directory test_videos/ --log-level DEBUG

# Generate and inspect config
./whisparr.py config generate -o test-config.json
cat test-config.json
```

### Adding New Features

When adding features, follow this pattern:

1. **Core Logic**: Add to appropriate module in `src/`
2. **CLI Integration**: Update `whisparr.py` to expose new options
3. **Configuration**: Add config options to `Config.DEFAULT_CONFIG`
4. **Documentation**: Update README.md and this file

## Dependencies

### Core Dependencies (requirements.txt)
- `openai-whisper`: Whisper model
- `ffmpeg-python`: Audio extraction (requires system FFmpeg)

### Development Dependencies (requirements-dev.txt)
- `pytest`: Testing framework
- `black`: Code formatter
- `flake8`: Linter
- `pytest-cov`: Coverage reporting

## Common Tasks

### Add New Subtitle Format

1. Add format method to `SubtitleGenerator`:
   ```python
   def generate_xyz(self, segments, output_path):
       # Implementation
   ```

2. Update `generate()` method to support new format

3. Add format to CLI choices in `whisparr.py`

### Add New Configuration Option

1. Add to `Config.DEFAULT_CONFIG` in `config_loader.py`

2. Use in relevant module:
   ```python
   value = self.config.get("section.new_option", default)
   ```

3. Document in README.md configuration section

### Improve Transcription Accuracy

Options to consider:
- Increase model size (`model_size`)
- Specify language explicitly (`language`)
- Adjust Whisper parameters in `transcriber.py`

## File Format Support

### Video Formats
`.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`

### Audio Formats
`.mp3`, `.wav`, `.flac`, `.aac`, `.m4a`, `.ogg`

**Note**: FFmpeg must be installed system-wide for audio extraction.

## Error Handling

### Common Issues

1. **FFmpeg Not Found**
   - Solution: `sudo apt install ffmpeg`
   - Check: `ffmpeg -version`

2. **CUDA Out of Memory**
   - Use smaller model: `--model base`
   - Use CPU: `--device cpu`

3. **File Not Found**
   - Processor checks file existence before processing
   - Raises `FileNotFoundError` with clear message

4. **Existing Subtitles**
   - By default, skips if subtitle exists
   - Override with `--overwrite` or `overwrite_existing: true` in config

## Testing

### Unit Tests
```bash
pytest tests/ -v
```

### Test Coverage
```bash
pytest --cov=src tests/
```

### Manual Testing
```bash
# Create test video with speech
# Process with different models
./whisparr.py file test.mp4 --model tiny
./whisparr.py file test.mp4 --model base
./whisparr.py file test.mp4 --model medium

# Compare output quality
```

## Performance Considerations

### Model Loading
- Models are lazy-loaded (only when first transcription occurs)
- Models stay in memory for subsequent transcriptions
- Large models require significant RAM/VRAM

### Batch Processing
- Processes files sequentially (not parallel)
- Single model instance reused across files
- Progress logged for each file

### GPU Acceleration
- Significantly faster with CUDA
- Requires NVIDIA GPU with CUDA toolkit
- Specify with `--device cuda`

## Future Enhancements

### Planned Features
1. **Watch Mode**: Monitor directory for new files
2. **Web Interface**: Flask/FastAPI web UI
3. **Docker Support**: Containerized deployment
4. **Translation**: Multi-language subtitle generation
5. **Speaker Diarization**: Identify different speakers
6. **Plex/Jellyfin Integration**: Auto-add subtitles to media servers

### Implementation Notes

**Watch Mode**:
- Use `watchdog` library for file system monitoring
- Add `watch` command to CLI
- Process new files automatically

**Web Interface**:
- Flask backend with REST API
- Vue.js/React frontend
- Job queue for async processing (Celery/RQ)

**Docker**:
- Multi-stage build (builder + runtime)
- Include FFmpeg in image
- Volume mounts for input/output

## Code Style

- **PEP 8**: Follow Python style guide
- **Type Hints**: Use where beneficial
- **Docstrings**: Google-style docstrings for all public methods
- **Logging**: Use `logging` module (not print statements)

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add: Description of changes"

# Push and create PR
git push origin feature/new-feature
```

## Troubleshooting Development Issues

### Import Errors
- Ensure virtual environment is activated
- Check `requirements.txt` is installed
- Verify Python path includes project root

### Model Download Issues
- Whisper downloads models on first use
- Models cached in `~/.cache/whisper/`
- Check internet connection and disk space

### Permission Issues
- Ensure `whisparr.py` is executable: `chmod +x whisparr.py`
- Check read/write permissions on input/output directories

## Related Projects

- **Whisper**: https://github.com/openai/whisper
- **Sonarr**: https://sonarr.tv/ (TV show automation)
- **Radarr**: https://radarr.video/ (Movie automation)

## Support

For questions or issues specific to this codebase:
1. Check README.md for usage documentation
2. Review this file for architecture guidance
3. Check existing code comments and docstrings
4. Test changes thoroughly before committing
