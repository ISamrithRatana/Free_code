import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters
from pdf2docx import parse
from typing import Tuple
import sys

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the bot token from environment variable or a secure place
TOKEN = ''

# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Give me a PDF and I'll give you a DOCX.")

# PDF to DOCX conversion function
def convert_pdf2docx(input_file: str, output_file: str, pages: Tuple = None):
    if pages:
        pages = [int(i) for i in list(pages) if i.isnumeric()]
    result = parse(pdf_file=input_file, docx_with_path=output_file, pages=pages)
    summary = {
        "File": input_file,
        "Pages": str(pages),
        "Output File": output_file
    }
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}: {}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return result

# Handle PDF file messages
async def handle_document(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    file = await context.bot.get_file(document.file_id)
    input_file = f"downloads/{document.file_name}"
    output_file = f"downloads/{document.file_name.rsplit('.', 1)[0]}.docx"
    
    # Download the file
    await file.download_to_drive(input_file)
    
    # Convert the file
    convert_pdf2docx(input_file, output_file)
    
    # Send the converted file back
    await update.message.reply_document(document=open(output_file, 'rb'))

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.PDF, handle_document))
    
    # Create downloads directory if not exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    application.run_polling()
