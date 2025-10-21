# Testing Whisparr with "The King" Movie

## Prerequisites

Whisparr is now set up and ready to use!

- ✅ Virtual environment created
- ✅ PyTorch (CPU) installed
- ✅ OpenAI Whisper installed
- ✅ FFmpeg installed (static build in ~/bin)

## Step 1: Get "The King" Movie File

### Option A: Copy from NAS via SMB (On your local machine)

```bash
# Install SMB client (one-time setup)
sudo apt install -y smbclient cifs-utils

# List shares on NAS
smbclient -L //192.168.1.200 -U peter%nomansland

# Browse movies share
smbclient //192.168.1.200/movies -U peter%nomansland

# Once you find the file, copy it using:
scp /path/to/The.King.2019.mkv peter@<this-server-ip>:/home/peter/work/whisparr/test_media/
```

### Option B: Direct Copy on NAS

If you have shell access to your Synology NAS:

```bash
# Find the movie
find /volume1 -name "*King*" -type f \( -name "*.mkv" -or -name "*.mp4" \) 2>/dev/null

# Copy to this server (replace with actual path)
scp "/volume1/path/to/The.King.2019.mkv" peter@<this-server-ip>:/home/peter/work/whisparr/test_media/
```

### Option C: Manual Copy

1. Access your NAS via File Station (http://192.168.1.200:5000)
2. Navigate to your Radarr movies folder
3. Find "The King" movie file
4. Download it locally
5. Upload to: `/home/peter/work/whisparr/test_media/`

## Step 2: Generate Subtitles

Once the movie file is in `test_media/`, run:

```bash
cd /home/peter/work/whisparr

# Activate virtual environment
source venv/bin/activate

# Add ffmpeg to PATH
export PATH=~/bin:$PATH

# Generate subtitles (basic - English audio)
./whisparr.py file test_media/the_king.mkv

# This will create: test_media/the_king.srt
```

## Step 3: Advanced Options

### With Translation (if audio is not in English)

```bash
# Set up API key (use one of these)
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Translate to English using OpenAI
./whisparr.py file test_media/the_king.mkv --translate English

# Or use Claude (Anthropic)
./whisparr.py file test_media/the_king.mkv --translate English --translate-provider anthropic
```

### Custom Model Size

```bash
# Use tiny model (fastest, less accurate)
./whisparr.py file test_media/the_king.mkv --model tiny

# Use base model (default, balanced)
./whisparr.py file test_media/the_king.mkv --model base

# Use medium model (slower, more accurate)
./whisparr.py file test_media/the_king.mkv --model medium
```

### Specify Language

```bash
# If you know the audio language
./whisparr.py file test_media/the_king.mkv --language en

# For French audio
./whisparr.py file test_media/the_king.mkv --language fr --translate English
```

## Step 4: Verify Subtitles

```bash
# View first 50 lines of generated subtitles
head -50 test_media/the_king.srt

# Or open in text editor
nano test_media/the_king.srt
```

## Expected Output

You'll see progress like this:

```
2025-10-22 - whisparr - INFO - Processing file: test_media/the_king.mkv
2025-10-22 - transcriber - INFO - Loading Whisper model: base
2025-10-22 - transcriber - INFO - Model loaded successfully
2025-10-22 - transcriber - INFO - Transcribing: test_media/the_king.mkv
2025-10-22 - transcriber - INFO - Transcription complete. Detected language: english
2025-10-22 - transcriber - INFO - Found 1234 segments
2025-10-22 - subtitle_generator - INFO - Generating SRT file: test_media/the_king.srt
2025-10-22 - subtitle_generator - INFO - SRT file generated with 1234 entries
✓ Subtitle generated: test_media/the_king.srt
```

## Troubleshooting

### "FFmpeg not found"
```bash
export PATH=~/bin:$PATH
```

### "Virtual environment not activated"
```bash
source venv/bin/activate
```

### "Out of memory"
```bash
# Use smaller model
./whisparr.py file test_media/the_king.mkv --model tiny
```

### Translation not working
```bash
# Make sure API key is set
echo $OPENAI_API_KEY

# If empty, set it:
export OPENAI_API_KEY="sk-..."
```

## Quick Test with Sample

If you don't have "The King" yet, test with any short video:

```bash
# Download a sample (10 seconds)
curl -L "https://file-examples.com/wp-content/storage/2017/04/file_example_MP4_480_1_5MG.mp4" \
  -o test_media/sample.mp4

# Generate subtitles
./whisparr.py file test_media/sample.mp4
```

## Current Status

- **Server IP**: Get it with `hostname -I | awk '{print $1}'`
- **Project Path**: `/home/peter/work/whisparr`
- **Test Media Folder**: `/home/peter/work/whisparr/test_media`
- **Virtual Env**: `/home/peter/work/whisparr/venv`
- **FFmpeg**: `/home/peter/bin/ffmpeg`

## Next Steps

1. Copy "The King" movie file to `test_media/`
2. Run Whisparr to generate subtitles
3. Enjoy automated subtitle generation!

For batch processing multiple movies:
```bash
./whisparr.py directory /path/to/movies --recursive --overwrite
```
