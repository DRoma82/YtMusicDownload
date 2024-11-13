from flask import Flask, send_file, abort
import io
from pytube import YouTube
from pydub import AudioSegment
import re

app = Flask(__name__)


@app.route('/<path:url>')
def download_audio(url):

    try:
        yt = YouTube(url)

        streams = set()
        for s in yt.streams:
            if s.type == "audio":
                streams.add(s)

        if not streams:
            return "No audio streams found", 404

        streams = sorted(streams, key=lambda s: int(s.abr[:-4]), reverse=True)
        target_stream = next((s for s in streams if int(s.abr[:-4]) == 128), None)
        audioStream = target_stream if target_stream else list(streams)[0]

        audioBuffer = io.BytesIO()
        audioStream.stream_to_buffer(audioBuffer)
        audioBuffer.seek(0)

        audio = AudioSegment.from_file(audioBuffer)

        mp3_buffer = io.BytesIO()
        audio.export(mp3_buffer, format="mp3", bitrate="128k")
        mp3_buffer.seek(0)

        safe_title = re.sub(r'[^\w\s-]', '', yt.title)
        filename = f"{safe_title}.mp3"

        return send_file(
                mp3_buffer,
                mimetype="audio/mp3",
                as_attachment=True,
                download_name=filename
            )
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error processing video: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8013)
