#!/bin/bash
# Helper script to copy "The King" movie from NAS
# Run this on your local machine or NAS

NAS_IP="192.168.1.200"
NAS_USER="peter"
NAS_PASS="nomansland"
DEST_SERVER="peter@$(hostname -I | awk '{print $1}')"
DEST_PATH="/home/peter/work/whisparr/test_media/"

echo "Searching for 'The King' movie on NAS..."

# Option 1: If running on NAS directly
if [ -d "/volume1" ]; then
    echo "Running on Synology NAS"
    MOVIE=$(find /volume1 -name "*King*" -type f \( -name "*.mkv" -or -name "*.mp4" -or -name "*.avi" \) 2>/dev/null | head -1)
    if [ -n "$MOVIE" ]; then
        echo "Found: $MOVIE"
        echo "Copying to $DEST_PATH..."
        cp "$MOVIE" /home/peter/work/whisparr/test_media/the_king.mkv
    fi
fi

# Option 2: If running from remote machine with smbclient
if command -v smbclient &> /dev/null; then
    echo "Using smbclient to browse shares..."
    smbclient -L //$NAS_IP -U $NAS_USER%$NAS_PASS
fi

echo ""
echo "=== Manual Instructions ==="
echo "1. Find 'The King' movie on your NAS"
echo "2. Copy it to: $DEST_PATH"
echo "3. Or run: scp /path/to/the_king.mp4 $DEST_SERVER:$DEST_PATH"
