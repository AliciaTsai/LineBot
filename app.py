# encoding: utf-8

import os


##########################################
# Init db connection.
##########################################


conn = None


# Remove the comment notations. Make a connenction to real db. [TODO_DB]

"""
import psycopg2
import urllib.parse as urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
"""


##########################################
# Init bot.
##########################################

from DataManager import DataManager
data_manager = DataManager(conn)

from CianCianBot import CianCianBot
bot = CianCianBot(data_manager)


##########################################
# Init flask backend and linebot facility.
##########################################

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

channel_secret = 'd07d23b1fb9c10f9e2d638bf56856344'
channel_access_token = '6buiIgstKTe+PYLqN/jmy8MNjsn4qBSFr1IwYRLgb5x9BWtD6qPHLi/KVMCGB00ZbcSAJfjOByFezjQSL4IvdCb6wT12BwdbrZ+/zhDRthAsW967CMnh4W9zmntX2oYybmPjx4pk50e4dhnaTVUHHwdB04t89/1O/w1cDnyilFU='
handler = WebhookHandler(channel_secret)
line_bot_api = LineBotApi(channel_access_token)


@app.route('/')
def index():
    return "<p>Hello World!</p>"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)  # default
def handle_text_message(event):                  # default
    # User's message
    msg = event.message.text  # message from user

    # User's chatting window id, could be `user_id`, `room_id`, `group_id`.
    if event.source.type == "user":
        src_id = event.source.user_id
    elif event.source.type == "room":
        src_id = event.source.room_id
    elif event.source.type == "group":
        src_id = event.source.group_id
    else:
        src_id = "error"
    unique_id = str(event.source.type) + "_" + src_id

    # Responding algorithm
    bot_response = bot.respond(msg, unique_id)

    # Reply
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=bot_response)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
