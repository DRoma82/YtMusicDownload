from yt_audio import yt_audio
import argparse


def main():
    parser = argparse.ArgumentParser(description='Download audio from YouTube video')
    parser.add_argument('url', help='YouTube video URL')
    args = parser.parse_args()
    yt = yt_audio(args.url)

    filename, buffer = yt.download_audio()
    with open(filename, 'wb') as f:
        f.write(buffer.getvalue())

    print("Downloaded", filename)


if __name__ == "__main__":
    main()
