#!/bin/bash
# Whisparr Runner Script
# Makes it easy to run Whisparr with proper environment

cd "$(dirname "$0")"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Run: python3 -m venv venv"
    exit 1
fi

source venv/bin/activate

# Add ffmpeg to PATH
export PATH=~/bin:$PATH

# Check if ffmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: FFmpeg not found. Install it or add to PATH."
    exit 1
fi

# Run whisparr with all passed arguments
echo "Running Whisparr..."
echo "Command: ./whisparr.py $@"
echo ""

./whisparr.py "$@"
