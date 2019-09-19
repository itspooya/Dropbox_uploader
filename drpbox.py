import dropbox
import os
from uplder import get_file_size, download, ERROR_DOWNLOADING_FILE, ERROR_FILE_SIZE
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
DROPBOX_TOKEN = ''
TELEGRAM_TOKEN = ''


def check_env():
    if os.getenv("DROPBOX_TOKEN") and os.getenv("TELEGRAM_TOKEN"):
        pass
    else:
        if os.path.isfile('.env'):
            from dotenv import load_dotenv
            load_dotenv()
        else:
            raise Exception("FILE DOESN'T EXIST")


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi This A bot To Upload Files to Telegram')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text("Downloading {}".format(update.message.text))
    try:
        size = get_file_size(update.message.text)
        update.message.reply_text("File Size Is {}".format(size))
    except(ERROR_FILE_SIZE):
        update.message.reply_text("There Was A Error Getting File Size")
    try:
        file = download(update.message.text)
        with open("{}".format(file), "rb") as f:
            dbx.files_upload(f.read(), "/telegram/{}".format(file), mute=True)
            result = dbx.files_get_temporary_link("/telegram/{}".format(file))
            update.message.reply_text("File Uploaded Successfully Link Is {}".format(result.link))
        os.remove(file)
    except(ERROR_DOWNLOADING_FILE):
        update.message.reply_text("There Was A Problem Downloading File")


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    check_env()
    DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    main()
