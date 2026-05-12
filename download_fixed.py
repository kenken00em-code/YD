#!/usr/bin/env python3
"""
YouTube Downloader with anti-detection and multiple fallback methods
"""
import os
import sys
import subprocess
import random
import yt_dlp
from pathlib import Path

class YouTubeDownloader:
    def __init__(self):
        self.url = os.getenv('YOUTUBE_URL')
        self.download_type = os.getenv('DOWNLOAD_TYPE', 'video-720p')
        self.subtitles = os.getenv('SUBTITLES', 'false').lower() == 'true'
        self.sub_lang = os.getenv('SUB_LANG', 'en')
        self.embed_subs = os.getenv('EMBED_SUBS', 'false').lower() == 'true'
        self.thumbnail = os.getenv('THUMBNAIL', 'false').lower() == 'true'
        self.video_id = self.extract_video_id()
        self.methods = [
            self.method_stealth,
            self.method_mobile,
            self.method_basic,
            self.method_fallback,
        ]
    
    def extract_video_id(self):
        import re
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11})(?:[?&]|$)',
            r'youtu\.be\/([0-9A-Za-z_-]{11})',
            r'embed\/([0-9A-Za-z_-]{11})'
        ]
        for pattern in patterns:
            match = re.search(pattern, self.url)
            if match:
                return match.group(1)
        return "unknown"
    
    def parse_download_type(self):
        parts = self.download_type.split('-')
        media_type = parts[0]
        quality = '720'
        audio_quality = '192'
        if len(parts) > 1:
            if media_type == 'audio':
                audio_quality = parts[2] if len(parts) > 2 else '192'
            else:
                quality = parts[1].replace('p', '')
        return media_type, quality, audio_quality
    
    def get_random_user_agent(self):
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        ]
        return random.choice(agents)
    
    def create_cookies_file(self):
        cookies = """# Netscape HTTP Cookie File
.youtube.com	TRUE	/	FALSE	1786465200	CONSENT	YES+cb.20240226-15-p0.en+FX+900
.youtube.com	TRUE	/	FALSE	1786465200	VISITOR_INFO1_LIVE	tYQgLcHJq9o
.youtube.com	TRUE	/	FALSE	1786465200	GPS	1
.youtube.com	TRUE	/	FALSE	1786465200	YSC	fvMblcHJq9o
.youtube.com	TRUE	/	FALSE	1786465200	PREF	tz=America.New_York&f4=4000000
"""
        with open('/tmp/cookies.txt', 'w') as f:
            f.write(cookies)
    
    def method_stealth(self):
        print("\nMethod 1: Stealth mode with cookies and user agent rotation")
        print("-" * 50)
        try:
            media_type, quality, audio_quality = self.parse_download_type()
            self.create_cookies_file()
            
            ydl_opts = {
                'quiet': False,
                'no_warnings': False,
                'user_agent': self.get_random_user_agent(),
                'cookiefile': '/tmp/cookies.txt',
                'sleep_interval': random.randint(3, 7),
                'max_sleep_interval': 10,
                'sleep_interval_requests': random.randint(2, 5),
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'ios', 'web'],
                        'skip': ['hls', 'dash'],
                    }
                },
                'geo_bypass': True,
                'geo_bypass_country': 'US',
                'socket_timeout': 30,
            }
            
            if media_type == 'audio':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'outtmpl': 'downloads/audio/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                })
            else:
                format_str = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best'
                ydl_opts.update({
                    'format': format_str,
                    'merge_output_format': 'mp4',
                    'outtmpl': 'downloads/videos/%(title)s.%(ext)s',
                })
            
            if self.subtitles:
                ydl_opts.update({
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': [self.sub_lang],
                    'subtitlesformat': 'srt',
                    'embedsubtitles': self.embed_subs,
                })
            
            if self.thumbnail:
                ydl_opts['writethumbnail'] = True
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            print("Stealth method successful!")
            return True
        except Exception as e:
            print(f"Stealth method failed: {str(e)[:200]}")
            return False
    
    def method_mobile(self):
        print("\nMethod 2: Mobile device emulation")
        print("-" * 50)
        try:
            media_type, quality, audio_quality = self.parse_download_type()
            
            mobile_agents = [
                'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            ]
            
            ydl_opts = {
                'quiet': False,
                'no_warnings': False,
                'user_agent': random.choice(mobile_agents),
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'ios'],
                        'skip': ['web_safety_mode'],
                    }
                },
                'headers': {
                    'X-YouTube-Client-Name': '3',
                    'X-YouTube-Client-Version': '19.01.34',
                },
            }
            
            if media_type == 'audio':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'outtmpl': 'downloads/audio/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'best[height<=720]/best',
                    'outtmpl': 'downloads/videos/%(title)s.%(ext)s',
                })
            
            if self.subtitles:
                ydl_opts.update({
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': [self.sub_lang],
                })
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            print("Mobile method successful!")
            return True
        except Exception as e:
            print(f"Mobile method failed: {str(e)[:200]}")
            return False
    
    def method_basic(self):
        print("\nMethod 3: Basic download with retries")
        print("-" * 50)
        try:
            media_type, quality, audio_quality = self.parse_download_type()
            
            ydl_opts = {
                'quiet': False,
                'no_warnings': False,
                'extractor_retries': 10,
                'retries': 10,
                'fragment_retries': 10,
                'ignoreerrors': True,
                'user_agent': self.get_random_user_agent(),
            }
            
            if media_type == 'audio':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'outtmpl': 'downloads/audio/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                })
            else:
                ydl_opts.update({
                    'format': 'best[height<=480]/best',
                    'outtmpl': 'downloads/videos/%(title)s.%(ext)s',
                })
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            print("Basic method successful!")
            return True
        except Exception as e:
            print(f"Basic method failed: {str(e)[:200]}")
            return False
    
    def method_fallback(self):
        print("\nMethod 4: Command line fallback")
        print("-" * 50)
        try:
            cmd = [
                'yt-dlp',
                '--format', 'best[height<=480]',
                '--output', 'downloads/videos/%(title)s.%(ext)s',
                '--no-check-certificate',
                '--force-ipv4',
                '--geo-bypass',
                '--user-agent', self.get_random_user_agent(),
                '--extractor-retries', '10',
                '--retries', '10',
                self.url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Fallback method successful!")
                return True
            else:
                print(result.stderr[:500])
                return False
        except Exception as e:
            print(f"Fallback method failed: {str(e)[:200]}")
            return False
    
    def run(self):
        print("=" * 60)
        print("YOUTUBE DOWNLOADER WITH ANTI-DETECTION")
        print("=" * 60)
        print(f"URL: {self.url}")
        print(f"Video ID: {self.video_id}")
        print(f"Type: {self.download_type}")
        print(f"Subtitles: {'Yes' if self.subtitles else 'No'}")
        print(f"Thumbnail: {'Yes' if self.thumbnail else 'No'}")
        print("=" * 60)
        
        for i, method in enumerate(self.methods, 1):
            print(f"\nAttempt {i}/{len(self.methods)}")
            if method():
                print("\n" + "=" * 60)
                print("DOWNLOAD SUCCESSFUL!")
                print("=" * 60)
                return True
        
        print("\n" + "=" * 60)
        print("ALL METHODS FAILED")
        print("=" * 60)
        return False

if __name__ == "__main__":
    downloader = YouTubeDownloader()
    success = downloader.run()
    sys.exit(0 if success else 1)
