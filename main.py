import argparse
import io
from youtubesearchpython import VideosSearch
from pytube import YouTube
import ssl
from yt_audio import yt_audio


def main():
    parser = argparse.ArgumentParser(
        description="Download audio from YouTube video and convert to mp3")
    parser.add_argument("-q", "--query", help="Search query")
    args = parser.parse_args()

    while not args.query:
        args.query = input("Enter the search query: ")

    yt = yt_audio()
    searchResults = yt.search(args.query)

    if not searchResults:
        print("No search results found")
        return

    for i, result in enumerate(searchResults):
        print(f"{i + 1}. {result.title}")
        print(f"  Channel: {result.channel_id}")
        # print(f"  {result['viewCount']["short"]} views")
        print()

    selection = int(input("Select a video to download: ")) - 1
    yt = searchResults[selection]
    audio_buffer = yt.download_audio(target_bitrate=128)
    filename = yt.get_safe_filename()

    with open(filename, 'wb') as f:
        f.write(audio_buffer.getvalue())

    print("Downloaded", filename)


if __name__ == "__main__":
    main()
