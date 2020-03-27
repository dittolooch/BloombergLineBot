
from flask import Flask, request
from flask_restful import Resource, Api
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
app = Flask(__name__)
api = Api(app)

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


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}


# api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
