import io
from pytube import YouTube, Search
from pydub import AudioSegment
import re
import ssl


class yt_audio:
    def __init__(self, url: str = None):
        ssl._create_default_https_context = ssl._create_unverified_context
        if url:
            self.yt = YouTube(url)

    def search(self, query):
        """Search for YouTube videos and return results."""
        videos_search = Search(query)
        return videos_search.results

    def _get_audio_streams(self):
        """Get available audio streams sorted by bitrate."""
        streams = set()
        for s in self.yt.streams:
            if s.type == "audio":
                streams.add(s)

        if not streams:
            raise ValueError("No audio streams found")

        return sorted(streams, key=lambda s: int(s.abr[:-4]), reverse=True)

    def download_audio(self, target_bitrate=None):
        """
        Download audio and return as BytesIO buffer.
        Optional target_bitrate in kbps (e.g. 128 for 128k).
        """
        streams = self._get_audio_streams()

        if target_bitrate:
            target_stream = next(
                (s for s in streams if int(s.abr[:-4]) == target_bitrate),
                None
            )
            audio_stream = target_stream if target_stream else streams[0]
        else:
            audio_stream = streams[0]

        audio_buffer = io.BytesIO()
        audio_stream.stream_to_buffer(audio_buffer)
        audio_buffer.seek(0)

        audio = AudioSegment.from_file(audio_buffer)

        mp3_buffer = io.BytesIO()
        bitrate = f"{target_bitrate}k" if target_bitrate else "192k"
        audio.export(mp3_buffer, format="mp3", bitrate=bitrate)
        mp3_buffer.seek(0)
        return mp3_buffer

    def get_safe_filename(self):
        """Get a filename-safe version of the video title."""
        return re.sub(r'[^\w\s-]', '', self.yt.title) + ".mp3"

    def __del__(self):
        """Clean up the httpx client when the object is destroyed."""
        if hasattr(self, 'client'):
            self.client.close()
