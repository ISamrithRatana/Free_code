import logging
from pytube import YouTube
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler,CallbackContext
import re

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram bot token
TOKEN = ''

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome to the YouTube Downloader Bot! Send me a YouTube video URL to download it.")

async def download_video(update: Update, context) -> None:
    url = update.message.text
    if is_youtube_url(url):
        try:
            # Download the video
            youtube = YouTube(url)
            video = youtube.streams.get_highest_resolution()
            video_path = video.download()

            # Send the video file to the user
            with open(video_path, 'rb') as video_file:
                await context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)
                # Close the file
            # os.remove(video_path)
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            await update.message.reply_text("Sorry, something went wrong while downloading the video.")
    else:
        await update.message.reply_text("Please send a valid YouTube video URL.")

def is_youtube_url(url):
    # Simple check to see if the URL resembles a YouTube video URL
    return 'youtube.com' in url or 'youtu.be' in url

def is_youtube_url(url):
    # Regular expression to check if the URL is a YouTube link
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return youtube_regex.match(url)

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(callback=download_video, filters=None))
    application.run_polling()

if __name__ == '__main__':
    main()
