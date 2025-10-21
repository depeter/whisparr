# Whisparr Quick Start - Generate Subtitles for "The King"

## 🎬 Movie Found!

**File**: `The King (2019) WEBDL-2160p.mkv`
**Location**: http://192.168.1.200:5000/sharing/0FzZVYtsg
**Format**: 4K/2160p MKV (may be 10-50GB)

---

## 📥 Step 1: Download the Movie

###  RECOMMENDED: Manual Download (Easiest)

1. **Open in browser**: http://192.168.1.200:5000/sharing/0FzZVYtsg
2. **Click the download button**
3. **Save to**: `/home/peter/work/whisparr/test_media/`

### Alternative: Use Helper Script

```bash
cd /home/peter/work/whisparr
./DOWNLOAD_THE_KING.sh
```

This will show you all download options.

### Alternative: SSH to NAS

```bash
ssh peter@192.168.1.200
# Password: nomansland

# Find the file
find /volume1 -name "*King*2019*" -type f

# Copy to this server
scp "/volume1/path/to/The King (2019) WEBDL-2160p.mkv" \
    peter@$(cat /path/to/server/ip):/home/peter/work/whisparr/test_media/
```

---

## ⚠️ Important: Disk Space

Current available space: **14GB**
Movie size estimate: **10-50GB** (4K file)

### Option A: Free up space first
```bash
# Clean up Docker
docker system prune -af

# Check space
df -h /
```

### Option B: Use smaller sample (RECOMMENDED)
After downloading, extract just 5 minutes:

```bash
cd /home/peter/work/whisparr
export PATH=~/bin:$PATH

~/bin/ffmpeg -i "test_media/The King (2019) WEBDL-2160p.mkv" \
             -t 300 -c copy \
             "test_media/the_king_sample.mkv"
```

This creates a ~1-2GB sample perfect for testing!

---

## 🎙️ Step 2: Generate Subtitles

Once the file is in `test_media/`:

### Basic (English audio → English subtitles)

```bash
cd /home/peter/work/whisparr
./run_whisparr.sh file "test_media/The King (2019) WEBDL-2160p.mkv"
```

Or for the 5-minute sample:

```bash
./run_whisparr.sh file test_media/the_king_sample.mkv
```

### With Translation

If the audio is in another language, translate to English:

```bash
# Using OpenAI GPT-4
export OPENAI_API_KEY="sk-your-key-here"
./run_whisparr.sh file test_media/the_king_sample.mkv --translate English

# Using Anthropic Claude (better quality)
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
./run_whisparr.sh file test_media/the_king_sample.mkv \
    --translate English --translate-provider anthropic
```

### Custom Options

```bash
# Fast but less accurate (tiny model)
./run_whisparr.sh file test_media/the_king_sample.mkv --model tiny

# Slower but more accurate (medium model)
./run_whisparr.sh file test_media/the_king_sample.mkv --model medium

# Specify source language
./run_whisparr.sh file test_media/the_king_sample.mkv --language en

# Generate WebVTT instead of SRT
./run_whisparr.sh file test_media/the_king_sample.mkv --format vtt
```

---

## 📋 Step 3: Check Results

```bash
# View generated subtitles
cat test_media/the_king_sample.srt | head -50

# Or for full movie
cat "test_media/The King (2019) WEBDL-2160p.srt" | head -50
```

---

## Expected Output

You should see something like:

```
Running Whisparr...
Command: ./whisparr.py file test_media/the_king_sample.mkv

2025-10-22 - whisparr - INFO - Processing file: test_media/the_king_sample.mkv
2025-10-22 - transcriber - INFO - Loading Whisper model: base
2025-10-22 - transcriber - INFO - Model loaded successfully
2025-10-22 - transcriber - INFO - Transcribing: test_media/the_king_sample.mkv
2025-10-22 - transcriber - INFO - Transcription complete. Detected language: english
2025-10-22 - transcriber - INFO - Found 342 segments
2025-10-22 - subtitle_generator - INFO - Generating SRT file: test_media/the_king_sample.srt
2025-10-22 - subtitle_generator - INFO - SRT file generated with 342 entries
✓ Subtitle generated: test_media/the_king_sample.srt
```

---

## 🎯 Example SRT Output

```srt
1
00:00:00,000 --> 00:00:02,500
Your Majesty, the English have arrived.

2
00:00:02,500 --> 00:00:05,000
Send them away. I will not see them.

3
00:00:05,000 --> 00:00:07,800
But sire, they bring news from the battlefield.
```

---

## ⚡ Quick Test (If You Don't Have The King Yet)

Test Whisparr with any video:

```bash
cd /home/peter/work/whisparr

# Download a small sample (5 seconds)
curl -L "https://file-examples.com/wp-content/storage/2017/04/file_example_MP4_480_1_5MG.mp4" \
  -o test_media/test.mp4

# Generate subtitles
./run_whisparr.sh file test_media/test.mp4
```

---

## 🔧 Troubleshooting

### "FFmpeg not found"
```bash
export PATH=~/bin:$PATH
~/bin/ffmpeg -version
```

### "Virtual environment not activated"
The `run_whisparr.sh` script handles this automatically. But if needed:
```bash
source venv/bin/activate
```

### "Out of memory"
Use a smaller model:
```bash
./run_whisparr.sh file test_media/the_king_sample.mkv --model tiny
```

### "Download failed"
Manual download steps:
1. Open http://192.168.1.200:5000/sharing/0FzZVYtsg in browser
2. Login if needed (peter / nomansland)
3. Click download button
4. Move file to `/home/peter/work/whisparr/test_media/`

---

## 📊 System Status

- ✅ Whisparr installed
- ✅ PyTorch (CPU) ready
- ✅ OpenAI Whisper ready
- ✅ FFmpeg installed (~/bin/ffmpeg)
- ✅ Virtual environment created
- ✅ Movie file located
- ⚠️  14GB free space (recommend using 5-min sample)

---

## 🚀 Next: Batch Processing

Once you're happy with one movie, process your entire library:

```bash
# Process all movies in a directory
./run_whisparr.sh directory /path/to/movies --recursive

# With translation
export OPENAI_API_KEY="your-key"
./run_whisparr.sh directory /path/to/movies \
    --recursive --translate English --overwrite
```

---

## 📚 Full Documentation

- **Complete Guide**: `README.md`
- **Development Info**: `CLAUDE.md`
- **Testing Guide**: `TEST_THE_KING.md`
- **GitHub**: https://github.com/depeter/whisparr

---

**Life is good! Generate those subtitles! 🎬**
