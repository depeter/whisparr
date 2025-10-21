#!/usr/bin/env python3
"""
Synology Share Downloader
Downloads files from Synology NAS sharing links
"""

import urllib.request
import urllib.parse
import json
import sys
import os

def download_from_synology_share(share_id, output_path, nas_ip="192.168.1.200", port=5000):
    """Download file from Synology sharing link"""

    base_url = f"http://{nas_ip}:{port}"

    print(f"Attempting to download from share: {share_id}")
    print(f"NAS: {base_url}")

    # Step 1: Get share info
    session_url = f"{base_url}/webapi/entry.cgi?api=SYNO.Core.Sharing.Session&version=1&method=get&sharing_id={share_id}"

    try:
        print("\n[1/3] Getting share information...")
        req = urllib.request.Request(session_url)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode()

            # Parse JavaScript response
            if "SYNO.SDS.ExtraSession" in content:
                # Extract filename from JavaScript object
                import re
                match = re.search(r'"filename"\s*:\s*"([^"]+)"', content)
                if match:
                    filename = match.group(1)
                    print(f"   Found file: {filename}")
                else:
                    print("   Error: Could not extract filename")
                    return False

                # Check if password protected
                status_match = re.search(r'"sharing_status"\s*:\s*"([^"]+)"', content)
                if status_match and status_match.group(1) != "none":
                    print(f"   Error: Share is password protected (status: {status_match.group(1)})")
                    return False
            else:
                print("   Error: Invalid share response")
                return False

    except Exception as e:
        print(f"   Error: {e}")
        return False

    # Step 2: Try download endpoint
    print("\n[2/3] Attempting download...")

    download_urls = [
        f"{base_url}/fbdownload/{share_id}",
        f"{base_url}/sharing/{share_id}/download",
        f"{base_url}/webapi/entry.cgi?api=SYNO.FileStation.Download&version=1&method=download&sharing_id={share_id}",
    ]

    for download_url in download_urls:
        try:
            print(f"   Trying: {download_url}")

            req = urllib.request.Request(download_url)
            req.add_header('User-Agent', 'Mozilla/5.0')

            with urllib.request.urlopen(req, timeout=10) as response:
                # Check if this is actually a file download
                content_type = response.headers.get('Content-Type', '')

                if 'application/json' in content_type:
                    data = response.read().decode()
                    print(f"   API Response: {data[:200]}")
                    continue

                # Looks like a file!
                total_size = int(response.headers.get('Content-Length', 0))
                if total_size > 0:
                    size_gb = total_size / (1024**3)
                    print(f"\n   File size: {size_gb:.2f} GB ({total_size:,} bytes)")

                    # Check disk space
                    import shutil
                    stat = shutil.disk_usage(os.path.dirname(output_path))
                    free_gb = stat.free / (1024**3)

                    print(f"   Available space: {free_gb:.2f} GB")

                    if total_size > stat.free * 0.9:
                        print(f"\n   ⚠️  WARNING: Not enough disk space!")
                        print(f"   Need: {size_gb:.2f} GB, Available: {free_gb:.2f} GB")
                        response = input("\n   Continue anyway? (yes/no): ")
                        if response.lower() != 'yes':
                            print("   Download cancelled.")
                            return False

                    # Download with progress
                    print(f"\n[3/3] Downloading to: {output_path}")

                    with open(output_path, 'wb') as f:
                        downloaded = 0
                        chunk_size = 1024 * 1024  # 1MB chunks

                        while True:
                            chunk = response.read(chunk_size)
                            if not chunk:
                                break

                            f.write(chunk)
                            downloaded += len(chunk)

                            if total_size > 0:
                                percent = (downloaded / total_size) * 100
                                print(f"\r   Progress: {percent:.1f}% ({downloaded/(1024**3):.2f} GB / {size_gb:.2f} GB)", end='', flush=True)

                    print("\n\n✓ Download complete!")
                    return True

        except Exception as e:
            print(f"   Error: {e}")
            continue

    print("\n✗ All download methods failed.")
    print("\nPlease download manually:")
    print(f"   1. Open: {base_url}/sharing/{share_id}")
    print(f"   2. Click download")
    print(f"   3. Save to: {output_path}")

    return False


if __name__ == "__main__":
    share_id = "0FzZVYtsg"
    output_path = "/home/peter/work/whisparr/test_media/The_King_2019.mkv"

    print("=" * 60)
    print("Synology Share Downloader")
    print("=" * 60)

    success = download_from_synology_share(share_id, output_path)

    if success:
        print(f"\nFile saved to: {output_path}")
        print("\nNext steps:")
        print("  cd /home/peter/work/whisparr")
        print(f"  ./run_whisparr.sh file {output_path}")
    else:
        print("\nManual download required.")
        print("See DOWNLOAD_THE_KING.sh for instructions.")

    sys.exit(0 if success else 1)
