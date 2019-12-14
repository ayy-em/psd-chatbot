import os
import telegram
import requests
import datetime
from google.cloud import storage
import webscraper as ws
import store_in_fire as storedata
import get_from_fire as getdata
import vice as v
import fireplotter
import reply


# get bot token and posidelki chat id from env vars
my_bot_token = os.environ["JHB_TOKEN"]
psdlk_id = os.environ["PSDLK_TG_CHAT_ID"]
# create a bot instance, using an API KEY
bot = telegram.Bot(token=my_bot_token)


# Entrypoint function GCF points to when it gets a request
def process_update(request):
    if request.method == "POST":
        process_telegram_update(request)
    elif request.method == "PUT":
        post_vice_news()
    elif request.method == "GET":
        post_posidelki()
        print(request)


# Processing Telegram update if POST request
def process_telegram_update(request):
    update_json = request.get_json(force=True)
    update = telegram.Update.de_json(update_json, bot)
    # Log the update in GCloud
    print('New update: ' + str(update))
    # if it's a message - de_json'd information if it's a new msg, not an edit
    if 'update_id' in update_json and 'edited_message' not in update_json:
        # where the msg came from, who wrote it, etc.
        chat_id = int(update.message.chat.id)
        isFromPosidelki = isFromChannel = isFromGroupChat = isFromPrivateChat = isNonText = False
        if update.message.chat.type == "private":
            first_name = update.message.chat.first_name
            last_name = update.message.chat.last_name
            username = update.message.chat.username
            isFromPrivateChat = True
        elif update.message.chat.type == "channel":
            isFromChannel = True
        elif update.message.chat.type == 'supergroup':
            isFromSuperGroup = True
            if str(update.message.chat.id) == str(psdlk_id):
                isFromPosidelki = True
        else:
            isFromGroupChat = True
        # get msg text if it has it
        if hasattr(update.message, 'text'):
            msg_text = update.message.text
        else:
            msg_text = 'non-text message'
            isNonText = True
        # get date and msg id
        date = update.message.date
        msg_id = int(update.message.message_id)
        # now we know everything about the message, let's reply
        if isFromPrivateChat:
            reply_to_private_message(chat_id, msg_text)
        # if from psdlk actions: store the data to firebase, ...
        if isFromPosidelki:
            storedata.store(update_json)


# Reply to Private message you send to the bot
def reply_to_private_message(conversation_id, incoming_text):
    if incoming_text == '/start':
        reply_text = reply.process_command('/start')
        bot.sendMessage(chat_id=conversation_id, text=reply_text)
    else:
        reply_text = str(reply.get_reply(incoming_text))
        bot.sendMessage(chat_id=conversation_id, text=reply_text, parse_mode='Markdown')


# Posting Vice News if PUT request
# Every day 1300 Amsterdam time (Cloud Scheduler)
def post_vice_news():
    vice_caption_and_image = v.get_caption_and_image()
    bot.sendPhoto(chat_id='@vice_news', photo=vice_caption_and_image[1], caption=vice_caption_and_image[0], parse_mode='Markdown', disable_notification=True)


# Posting Posidelki daily message if GET request
# Every day at 0845 Amsterdam time (Cloud Scheduler)
def post_posidelki():
    # get text - combination of webscraper and getdata
    bot_text = str(ws.get_daily_psdlk_msg()) + str(getdata.get_stats_msg())
    # and send that text to posidelki (id - global var)
    bot.sendMessage(chat_id=psdlk_id, text=bot_text, parse_mode='Markdown', disable_notification=True, disable_web_page_preview=True)
