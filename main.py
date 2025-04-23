import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL
from mega import Mega

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram bot token (note: this is visible in code — use env for production)
BOT_TOKEN = "7833312661:AAFKQ7xjG05gwEbRRtLY74uaVU_4qNqqXes"

# Download YouTube videos
def download_youtube(link):
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        return ydl.prepare_filename(info)

# Download Mega.nz files
def download_mega(link):
    mega = Mega()
    m = mega.login()
    file = m.download_url(link, dest_path='downloads')
    return file

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id
    try:
        if "youtu" in text:
            await update.message.reply_text("Downloading YouTube video...")
            file_path = download_youtube(text)
            await context.bot.send_video(chat_id=chat_id, video=open(file_path, 'rb'))
        elif "mega.nz" in text:
            await update.message.reply_text("Downloading from Mega.nz...")
            file_path = download_mega(text)
            await context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
        else:
            await update.message.reply_text("Please send a valid YouTube or Mega.nz link.")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text(f"Error: {str(e)}")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a YouTube or Mega.nz link to download.")

# Start bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    os.makedirs("downloads", exist_ok=True)
    app.run_polling()

if __name__ == '__main__':
    main()
  
