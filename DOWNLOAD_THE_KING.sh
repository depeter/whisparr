#!/bin/bash
# Script to download "The King" from Synology NAS
# Run this script to get the movie file for subtitle generation

SHARE_URL="http://192.168.1.200:5000/sharing/0FzZVYtsg"
FILENAME="The King (2019) WEBDL-2160p.mkv"
DEST_DIR="/home/peter/work/whisparr/test_media"

echo "========================================="
echo "The King Movie Download Helper"
echo "========================================="
echo ""
echo "File found: $FILENAME"
echo "Location: Synology NAS sharing link"
echo ""

# Check disk space
AVAIL=$(df -BG / | tail -1 | awk '{print $4}' | sed 's/G//')
echo "Available disk space: ${AVAIL}GB"
echo ""

if [ "$AVAIL" -lt "15" ]; then
    echo "⚠️  WARNING: Low disk space!"
    echo "   This is a 4K movie file which may be 10-50GB"
    echo "   You might need to free up more space first."
    echo ""
fi

echo "========================================="
echo "DOWNLOAD OPTIONS:"
echo "========================================="
echo ""

echo "Option 1: Download via Web Browser"
echo "-----------------------------------"
echo "1. Open: $SHARE_URL"
echo "2. Click the download button"
echo "3. Save to: $DEST_DIR/"
echo ""

echo "Option 2: Download on Synology NAS (SSH)"
echo "-----------------------------------------"
echo "If you have SSH access to your NAS:"
echo ""
echo "  ssh peter@192.168.1.200"
echo "  # Find the actual file path:"
echo "  find /volume1 -name '*King*2019*' -type f"
echo "  # Then copy directly to this server:"
echo "  scp \"/volume1/path/to/The.King.mkv\" peter@$(hostname -I | awk '{print $1}'):$DEST_DIR/"
echo ""

echo "Option 3: Mount SMB Share (if SMB client installed)"
echo "---------------------------------------------------"
echo "  sudo apt install -y smbclient cifs-utils"
echo "  sudo mkdir -p /mnt/nas"
echo "  sudo mount -t cifs //192.168.1.200/movies /mnt/nas -o username=peter,password=nomansland"
echo "  cp \"/mnt/nas/path/to/The King (2019) WEBDL-2160p.mkv\" $DEST_DIR/"
echo "  sudo umount /mnt/nas"
echo ""

echo "Option 4: Use Smaller Sample (RECOMMENDED FOR TESTING)"
echo "--------------------------------------------------------"
echo "  Since this is a 4K file, you might want to:"
echo "  1. Download just the first 5 minutes for testing"
echo "  2. Or use a smaller quality version if available"
echo ""
echo "  To extract first 5 minutes after downloading:"
echo "  ~/bin/ffmpeg -i \"$DEST_DIR/$FILENAME\" -t 300 -c copy \"$DEST_DIR/the_king_sample.mkv\""
echo ""

echo "========================================="
echo "AFTER DOWNLOADING:"
echo "========================================="
echo ""
echo "Once you have the file in $DEST_DIR/, run:"
echo ""
echo "  cd /home/peter/work/whisparr"
echo "  ./run_whisparr.sh file \"test_media/$FILENAME\""
echo ""
echo "Or for just a 5-minute sample:"
echo "  ./run_whisparr.sh file test_media/the_king_sample.mkv"
echo ""

# Try to open the sharing link info
echo "========================================="
echo "Checking share accessibility..."
echo "========================================="
curl -s "$SHARE_URL" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Share link is accessible"
    echo "  URL: $SHARE_URL"
else
    echo "✗ Cannot reach share link"
    echo "  Check your network connection"
fi
echo ""
