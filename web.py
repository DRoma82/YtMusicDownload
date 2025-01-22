from flask import Flask, send_file
from yt_audio import yt_audio

app = Flask(__name__)


@app.route('/<path:url>')
def download_audio(url):

    try:
        yt = yt_audio(url)
        filename, audio_buffer = yt.download()

        return send_file(
            audio_buffer,
            mimetype="audio/m4a",
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error processing video: {str(e)}", 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8013, use_reloader=True)
