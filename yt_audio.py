import io
import re
import os
import json
from contextlib import redirect_stdout
from yt_dlp import YoutubeDL
from urllib.parse import parse_qs, urlparse


class yt_audio:
    def __init__(self, url: str):
        self.URL = url
        self.cache_dir = "cache"  # Directory to store cached files
        self.video_id = self._extract_video_id(url)

        if not self.video_id:
            raise ValueError("Invalid YouTube URL")

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _extract_video_id(self, url: str) -> str:
        """Extract YouTube video ID from URL."""
        parsed = urlparse(url)
        if parsed.hostname == 'youtu.be':
            return parsed.path[1:]
        if parsed.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed.path == '/watch':
                return parse_qs(parsed.query)['v'][0]
            if parsed.path[:7] == '/embed/':
                return parsed.path.split('/')[2]
            if parsed.path[:3] == '/v/':
                return parsed.path.split('/')[2]
        return None  # Invalid YouTube URL

    def download(self):
        return self._get_video_title(), self._download_audio()

    def _download_audio(self):
        cache_file = os.path.join(self.cache_dir, f"{self.video_id}.m4a")

        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return io.BytesIO(f.read())

        audio_dl_opts = {
            'format': 'm4a/bestaudio/best',
            "outtmpl": "-",
            'logtostderr': True,
            'quiet': True,
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }

        buffer = io.BytesIO()
        with redirect_stdout(buffer), YoutubeDL(audio_dl_opts) as ydl:
            ydl.download([self.URL])

        buffer.seek(0)
        with open(cache_file, 'wb') as f:
            f.write(buffer.read())

        buffer.seek(0)
        return buffer

    def _get_video_title(self):
        cache_file = os.path.join(self.cache_dir, f"{self.video_id}.json")

        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                info = json.load(f)
        else:
            info_opts = {
                'quiet': True,
            }

            with YoutubeDL(info_opts) as ydl:
                raw_info = ydl.extract_info(self.URL, download=False)
                info = ydl.sanitize_info(raw_info)

            with open(cache_file, 'w') as f:
                json.dump(info, f, indent=2)

        filename = self._get_safe_filename(info['title'])
        return filename

    def _get_safe_filename(self, title: str):
        """Get a filename-safe version of the video title."""
        return re.sub(r'[^\w\s-]', '', title) + ".m4a"
