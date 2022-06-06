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

from oauth2client.service_account import ServiceAccountCredentials
import gspread

app = Flask(__name__)
app.debug = True

line_bot_api = LineBotApi('ZiTzDVajD8MZBmHtyuDI/t52SlTLxi+fPuNvQQoJrAFdJpQYirsPxa0WJNuovS+TuUgDH7a5deHT0dPdlNzix4S0bpxtOYkN2IsYSVfeGLGMX6w1o5IaSRlGGEAZLZqzkyF8o0ZfITSQw3ze6YtZjQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c30c448f5da2c4208b7eebf26bdda3a7')

scope = ['https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1h3jk5KxcPcY1Wt1qgwDOeXxRZz_h49MmIlz9Bs1KsEs/edit?usp=sharing")
worksheet = sheet.get_worksheet(0) # sheet index in spreadsheets

# print(worksheet.get_all_values())
# # worksheet.update_cell(1, 2, "BIDEN VOTES")
# worksheet.update("A8:C8", [["Texas", 5261485, 5261485]])
# worksheet.append_rows(values=[["Pennsylvania", 3458312, 3376499]])


@app.route("/test", methods=['POST'])
def test():
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

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    # print(body)
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    disname = line_bot_api.get_profile(id).display_name
    
    print('line_id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)
    
    reply(intent, text, reply_token, id, disname)
    
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    
def reply(intent, text, reply_token, id, disname):
    if intent == 'test':
        reply_text = 'ทดสอบสำเร็จ'
        worksheet.append_rows(values=[[text, reply_text]])
        text_message = TextSendMessage(text=reply_text)
        line_bot_api.reply_message(reply_token, text_message)
        
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run()