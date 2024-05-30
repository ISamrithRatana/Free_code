from pytube import YouTube

def download_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path="Downloads")
        print(f"Downloaded '{yt.title}' successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

while True:
    url = input("Enter YouTube URL (or press Enter to exit): ")
    if not url:
        break
    download_video(url)
