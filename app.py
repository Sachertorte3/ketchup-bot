import os, random
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    ImageMessage,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackEvent
)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg == "よくある質問":
        line_bot_api.reply_message(event.reply_token, make_select_message())
    else:
        ret_msg = "ケチャップ画像を送って欲しいぜ"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ret_msg))

@handler.add(PostbackEvent)
def on_postback(line_event):
    data = line_event.postback.data
    
    line_bot_api.reply_message(line_event.reply_token, TextSendMessage(data))


def make_select_message():
    questions = {}
    with open('questions.txt') as f:
        lines = f.readlines()
        questions = {}
        for line in lines:
            questions[line.split(',')[0]] = line.split(',')[1]
        return TemplateSendMessage(
            alt_text="選択肢",
            template=ButtonsTemplate(
                title="よくある質問",
                text="下から該当するものを選んでください。",
                actions=[{
                        "type": "postback",
                        "data": f"Q:{question_Q}\nA:{question_A} ".replace('\n ', ' '),
                        "label": question_Q} for question_Q, question_A in questions.items()
                ]
            )
    )

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    res = random.randint(0,1)

    if res == 0:
        ret_msg = "大丈夫、まだイケるって"
    elif res == 1:
        ret_msg = "残念ですが、そのケチャップはもう空っぽですね\nhttps://www.amazon.co.jp/-/en/2803/dp/B00H2DC9MU\n新しいのを買いましょう！"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ret_msg))

if __name__ == "__main__":
    app.run()
