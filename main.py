from yt_audio import yt_audio


def main():
    yt = yt_audio('https://www.youtube.com/watch?v=z3JhXn_onsw')

    buffer = yt.download_audio()
    filename = yt.get_safe_filename('test')
    with open(filename, 'wb') as f:
        f.write(buffer.getvalue())

    print("Downloaded", filename)


if __name__ == "__main__":
    main()
