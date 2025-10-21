#!/usr/bin/env python3
"""
Whisparr - AI Subtitles Generator CLI

Command-line interface for automated subtitle generation.
"""

import sys
import logging
import argparse
from pathlib import Path
from typing import Optional

from src import Config, FileProcessor, __version__


def setup_logging(level: str = "INFO"):
    """
    Setup logging configuration

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def process_file_command(args):
    """Handle the 'file' command"""
    config = Config(args.config) if args.config else Config()

    # Override config with CLI arguments
    if args.model:
        config.set("whisper.model_size", args.model)
    if args.language:
        config.set("whisper.language", args.language)
    if args.format:
        config.set("subtitle.format", args.format)
    if args.device:
        config.set("whisper.device", args.device)

    # Setup logging
    setup_logging(args.log_level or config.get("logging.level", "INFO"))

    processor = FileProcessor(config)

    try:
        subtitle_path = processor.process_file(
            args.input,
            args.output,
            subtitle_format=args.format
        )
        print(f"✓ Subtitle generated: {subtitle_path}")
        return 0
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return 1


def process_directory_command(args):
    """Handle the 'directory' command"""
    config = Config(args.config) if args.config else Config()

    # Override config with CLI arguments
    if args.model:
        config.set("whisper.model_size", args.model)
    if args.language:
        config.set("whisper.language", args.language)
    if args.format:
        config.set("subtitle.format", args.format)
    if args.device:
        config.set("whisper.device", args.device)
    if args.overwrite:
        config.set("processing.overwrite_existing", True)

    # Setup logging
    setup_logging(args.log_level or config.get("logging.level", "INFO"))

    processor = FileProcessor(config)

    try:
        subtitle_files = processor.process_directory(
            args.input,
            args.output,
            recursive=args.recursive
        )
        print(f"\n✓ Successfully processed {len(subtitle_files)} files")
        return 0
    except Exception as e:
        logging.error(f"Error processing directory: {e}")
        return 1


def config_command(args):
    """Handle the 'config' command"""
    if args.action == "generate":
        config = Config()
        output_path = args.output or "config.json"
        config.save(output_path)
        print(f"✓ Configuration file generated: {output_path}")
        return 0
    elif args.action == "show":
        config = Config(args.config) if args.config else Config()
        import json
        print(json.dumps(config.to_dict(), indent=2))
        return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Whisparr - AI Subtitles Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate subtitles for a single file
  whisparr.py file video.mp4

  # Generate subtitles with specific model and language
  whisparr.py file video.mp4 --model medium --language en

  # Process all videos in a directory
  whisparr.py directory /path/to/videos --recursive

  # Generate a configuration file
  whisparr.py config generate -o my-config.json

  # Show current configuration
  whisparr.py config show
        """
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'Whisparr {__version__}'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # File command
    file_parser = subparsers.add_parser('file', help='Process a single file')
    file_parser.add_argument('input', help='Input video/audio file')
    file_parser.add_argument('-o', '--output', help='Output subtitle file path')
    file_parser.add_argument('-m', '--model', choices=['tiny', 'base', 'small', 'medium', 'large'],
                            help='Whisper model size')
    file_parser.add_argument('-l', '--language', help='Source language code (e.g., en, es, fr)')
    file_parser.add_argument('-f', '--format', choices=['srt', 'vtt'], help='Subtitle format')
    file_parser.add_argument('-d', '--device', choices=['cpu', 'cuda'], help='Device to use')
    file_parser.add_argument('-c', '--config', help='Configuration file path')
    file_parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                            help='Logging level')
    file_parser.set_defaults(func=process_file_command)

    # Directory command
    dir_parser = subparsers.add_parser('directory', help='Process all files in a directory')
    dir_parser.add_argument('input', help='Input directory')
    dir_parser.add_argument('-o', '--output', help='Output directory')
    dir_parser.add_argument('-r', '--recursive', action='store_true', help='Process subdirectories')
    dir_parser.add_argument('-m', '--model', choices=['tiny', 'base', 'small', 'medium', 'large'],
                           help='Whisper model size')
    dir_parser.add_argument('-l', '--language', help='Source language code (e.g., en, es, fr)')
    dir_parser.add_argument('-f', '--format', choices=['srt', 'vtt'], help='Subtitle format')
    dir_parser.add_argument('-d', '--device', choices=['cpu', 'cuda'], help='Device to use')
    dir_parser.add_argument('-c', '--config', help='Configuration file path')
    dir_parser.add_argument('--overwrite', action='store_true', help='Overwrite existing subtitle files')
    dir_parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                           help='Logging level')
    dir_parser.set_defaults(func=process_directory_command)

    # Config command
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_parser.add_argument('action', choices=['generate', 'show'], help='Config action')
    config_parser.add_argument('-o', '--output', help='Output path for config file')
    config_parser.add_argument('-c', '--config', help='Configuration file to show')
    config_parser.set_defaults(func=config_command)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
