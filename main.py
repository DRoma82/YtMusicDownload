from yt_audio import yt_audio


def main():
    yt = yt_audio('https://www.youtube.com/watch?v=z3JhXn_onsw')

    yt.download_audio()
    filename = yt.get_safe_filename('test')

    print("Downloaded", filename)


if __name__ == "__main__":
    main()
