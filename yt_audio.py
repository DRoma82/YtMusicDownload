import io
import re
from contextlib import redirect_stdout
from yt_dlp import YoutubeDL
import json


class yt_audio:
    def __init__(self, url: str):
        self.URL = url

    def download_audio(self):
        """
        Download audio and return as BytesIO buffer.
        """

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

        info_opts = {
            'quiet': True,
        }

        with YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(self.URL, download=False)

        filename = self.get_safe_filename(info['title'])
        return filename, buffer

    def get_safe_filename(self, title: str):
        """Get a filename-safe version of the video title."""
        return re.sub(r'[^\w\s-]', '', title) + ".m4a"
