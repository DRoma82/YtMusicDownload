import io
import re
import yt_dlp


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
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(self.URLS)

    def get_safe_filename(self, title: str):
        """Get a filename-safe version of the video title."""
        return re.sub(r'[^\w\s-]', '', title) + ".mp3"
