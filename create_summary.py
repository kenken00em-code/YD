#!/usr/bin/env python3
"""
Generate download summary
"""
import os
from pathlib import Path
from datetime import datetime

def create_summary():
    download_dir = Path('downloads')
    split_dir = Path('split_files')
    
    video_size = 0
    audio_size = 0
    split_size = 0
    
    if (download_dir / 'videos').exists():
        for f in (download_dir / 'videos').rglob('*'):
            if f.is_file():
                video_size += f.stat().st_size
    
    if (download_dir / 'audio').exists():
        for f in (download_dir / 'audio').rglob('*'):
            if f.is_file():
                audio_size += f.stat().st_size
    
    if split_dir.exists():
        for f in split_dir.rglob('*'):
            if f.is_file():
                split_size += f.stat().st_size
    
    summary = "=" * 60 + "\n"
    summary += "DOWNLOAD SUMMARY\n"
    summary += "=" * 60 + "\n\n"
    summary += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    summary += f"Type: {os.getenv('DOWNLOAD_TYPE', 'N/A')}\n"
    summary += f"URL: {os.getenv('YOUTUBE_URL', 'N/A')}\n\n"
    summary += "FILE SIZES:\n"
    summary += "-" * 20 + "\n"
    summary += f"Videos: {video_size/(1024*1024):.2f} MB\n"
    summary += f"Audio: {audio_size/(1024*1024):.2f} MB\n"
    summary += f"Split Archives: {split_size/(1024*1024):.2f} MB\n\n"
    summary += "SETTINGS:\n"
    summary += "-" * 20 + "\n"
    summary += f"Subtitles: {os.getenv('SUBTITLES', 'No')}\n"
    summary += f"Embedded Subs: {os.getenv('EMBED_SUBS', 'No')}\n"
    summary += f"Thumbnail: {os.getenv('THUMBNAIL', 'No')}\n\n"
    summary += "Auto-split at 90MB\n"
    summary += "Downloaded via GitHub Actions\n"
    summary += "=" * 60 + "\n"
    
    with open('summary.md', 'w') as f:
        f.write(summary)
    
    print(summary)
    print("Summary saved to summary.md")

if __name__ == "__main__":
    create_summary()
