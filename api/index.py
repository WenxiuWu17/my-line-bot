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

line_bot_api = LineBotApi('6kJHVCadZpkmgrQNHmkMWA9A7nraF2gPEFpRis9F2uHYjinXIN8KhG0Ay2USzHhVijm7jNaNNO1goxTPgmm1LYzsJMh2J7e8oaTstS+II8pyBsf92JHiF+bOjoPaJDZbSDo+moFgn8PBFIgsZ1HNOgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d8c4f7b1033abd303dee10c57b4e6dac')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()