import io
import re
from contextlib import redirect_stdout
from yt_dlp import YoutubeDL


class yt_audio:
    def __init__(self, url: str = None):
        if url:
            self.URLS = [url]

    def download_audio(self):
        """
        Download audio and return as BytesIO buffer.
        """

        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            "outtmpl": "-",
            'logtostderr': True,
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }

        buffer = io.BytesIO()
        with redirect_stdout(buffer), YoutubeDL(ydl_opts) as ydl:
            ydl.download(self.URLS)

        return buffer

    def get_safe_filename(self, title: str):
        """Get a filename-safe version of the video title."""
        return re.sub(r'[^\w\s-]', '', title) + ".m4a"
