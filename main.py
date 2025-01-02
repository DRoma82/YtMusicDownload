from yt_audio import yt_audio


def main():
    yt = yt_audio('https://www.youtube.com/watch?v=z3JhXn_onsw')

    filename, buffer = yt.download_audio()
    with open(filename, 'wb') as f:
        f.write(buffer.getvalue())

    print("Downloaded", filename)


if __name__ == "__main__":
    main()
