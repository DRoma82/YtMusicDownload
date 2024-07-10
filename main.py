# main.py
import argparse
import io
from youtubesearchpython import VideosSearch
from pytube import YouTube
from pydub import AudioSegment


def main():
    parser = argparse.ArgumentParser(
        description="Download audio from YouTube video and convert to mp3")
    parser.add_argument("-q", "--query", help="Search query")
    args = parser.parse_args()

    while not args.query:
        args.query = input("Enter the search query: ")

    searchResults = VideosSearch(args.query, limit=3).result()["result"]

    if not searchResults:
        print("No search results found")
        return

    for i, result in enumerate(searchResults):
        print(f"{i + 1}. {result['title']} ({result['duration']})")
        print(f"  Channel: {result['channel']['name']}")
        print(f"  {result['viewCount']["short"]} views")
        print()

    selection = int(input("Select a video to download: ")) - 1
    url = searchResults[selection]["link"]

    yt = YouTube(url)

    streams = set()
    for s in yt.streams:
        if s.type == "audio":
            streams.add(s)

    if not streams:
        print("No audio streams found")
        return

    if len(streams) > 1:
        streams = sorted(streams, key=lambda s: int(s.abr[:-4]), reverse=True)
        for i, s in enumerate(streams):
            print(f"{i + 1}. {s.audio_codec} {s.abr} {s.mime_type}")
            print()

        selection = int(input("Select an audio stream to download: ")) - 1
        audioStream = list(streams)[selection]
    else:
        audioStream = list(streams)[0]

    audioBuffer = io.BytesIO()
    audioStream.stream_to_buffer(audioBuffer)
    audioBuffer.seek(0)

    audio = AudioSegment.from_file(audioBuffer)
    audio.export(yt.title + ".mp3", format="mp3")

    print("Downloaded audio from", yt.title)


if __name__ == "__main__":
    main()
