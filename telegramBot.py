import logging, sys, datetime
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
        CallbackQueryHandler, ConversationHandler, InlineQueryHandler, ChosenInlineResultHandler)
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.utils.helpers import escape_markdown
from boardGraphic import *
from database import *
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def addChat(bot, update):
    if(dbAddChat(update["message"]["chat"]["id"])):
        update.message.reply_text("Hat geklappt. Chat is registriert")
    else:
        update.message.reply_text("Hat net geklappt.")

def newGame(bot, update, args=""):
    user = update.message.from_user
    turn = dbNewGame(chatID=update["message"]["chat"]["id"])
    if(turn):
        bot.send_photo(update.message.chat.id, photo=goBoardPicture(turn.boardString))
        update.message.reply_text("Mache einen Zug, indem du eine Position angibst (zB. e14).")
    else:
        update.message.reply_text("Hat net geklappt.")

def coordsByString(string):
    string = string.strip().lower()
    try:
        x = 'abcdefghijklmnopqrs'.index(string[0]);
        y = int(string[1:]) if string[1:].isdigit() else None
        if x>=0 and x<19 and y>=0 and y<19: return (x,y)
        return False
    except Exception as e:
        return False

def turn(bot, update, args=""):
    xy = coordsByString(update["message"]["text"][6:])
    if not xy:
        update.message.reply_text("Ungültiger Spielzug.")
        return
    x,y = xy
    nextTurn = dbAddTurn(chatID=update["message"]["chat"]["id"], xy=xy)
    if nextTurn:
        bot.send_photo(update.message.chat.id, photo=goBoardPicture(nextTurn.boardString))
    else:
        update.message.reply_text("Hat net geklappt.")

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    global update_id
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("YOUR_TELEGRAM_API_KEY")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", addChat))
    dp.add_handler(CommandHandler("newGame", newGame))
    dp.add_handler(CommandHandler("turn", turn))
    #dp.add_handler(CommandHandler("back", back))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    if 'genDB' in sys.argv: createDB();
    main()
