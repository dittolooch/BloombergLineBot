
from flask import Flask, request
from flask_restful import Resource, Api
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent
from Crawler.Database import Database
from ChatHandler import ChatHandler
app = Flask(__name__)
api = Api(app)
db = Database()
chatHandler = ChatHandler(db)
line_bot_api = LineBotApi(
    "3a4G473Gy2zFWCQw9Mu58QT+Vg9Mhs7x/fpNXBDDbTvY5/b+myM0pGVNyGY7H+Q1OHKd0HWO33FaBlxEER09oc3MEda+WbF/7q9/jr2FMQic1YgwBuGcC4uLoHzxKVj1Fd41WB2fhQtg45Z7mJDDegdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("45a4c6945c2a5ad282d2d82f231b5862")


@app.route('/line', methods=["POST"])
def webhook():
    try:
        print(request.headers)
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except InvalidSignatureError:
        messages = (
            "Invalid signature. Please check your channel access token/channel secret."
        )
        return messages, 200
    return "OK", 200


@app.route('/', methods=["GET"])
def index():
    return "OK", 200


@app.route('/api/<articleType>/articles/<articleDate>/<slug>', methods=["GET"])
def article(articleType, articleDate, slug):
    url = "/{}/articles/{}/{}".format(articleType, articleDate, slug)
    articleDict = db.getArticle(url)
    if articleDict:
        return """
      <!DOCTYPE html>
      {}
      """.format(articleDict[0]["html"]), 200
    return "Not Found", 200


@handler.add(PostbackEvent)
def handle_postback(event):
    chatHandler.handlePostback(line_bot_api, event)


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    chatHandler.handleMessageText(line_bot_api, event)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
