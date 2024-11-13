from flask import Flask, send_file
from yt_audio import yt_audio

app = Flask(__name__)


@app.route('/<path:url>')
def download_audio(url):

    try:
        yt = yt_audio(url)
        audio_buffer = yt.download_audio(target_bitrate=128)
        filename = yt.get_safe_filename()

        return send_file(
            audio_buffer,
            mimetype="audio/mp3",
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error processing video: {str(e)}", 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8013)
