import telegram
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import logger
import json
import os.path

api_key = ""

if (os.path.exists("bot_api.txt")):
    f = open("bot_api.txt", "r")
    api_key = f.read()
    f.close
else:
    api_key = input("Enter the API key of your bot: ")
    with open("bot_api.txt", "w") as t:
        t.write(api_key)
    logger.makeLog("New API Key created")


bot = telegram.Bot(token = api_key)  
updater = Updater(api_key, use_context=True)


def start(update: Update, context: CallbackContext):
    username = update.message.chat.username
    update.message.reply_text("Greetings")
    logger.makeTelegramLog("Greetings",username)
  
def unknown(update: Update, context: CallbackContext):
    username = update.message.chat.username
    update.message.reply_text("'%s' is not a valid command" % update.message.text)
    logger.makeTelegramLog("Unvalid Command",username)
  
def unknown_text(update: Update, context: CallbackContext):
    username = update.message.chat.username
    update.message.reply_text("'%s' is invalid" % update.message.text)
    logger.makeTelegramLog("Invalid",username)

def ping(update: Update, context: CallbackContext):
    username = update.message.chat.username
    update.message.reply_text("Pong")
    logger.makeTelegramLog("Ping",username)


# Handlers
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("ping", ping))

# Error Handlers
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


# Brodcast
def broadcast(msg):
    f = open("users.json")
    user_data = json.load(f)
    for user in user_data:
        bot.send_message(chat_id = user_data[user], text = msg)
        logger.makeTelegramLog(msg, user)

# Start
updater.start_polling()
logger.makeLog("Successfull Start")