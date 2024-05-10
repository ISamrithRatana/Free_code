from pytube import YouTube

def donwnload_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path="Downlaods")
        print(f"Download '{yt.title}' successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

donwnload_video('') #input url