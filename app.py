from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('l8sFNsaVP1oRQiHCGf7TESDov5PaIR/34JzmKLGj5D9jUZmbi+XE3JtqfCoI8MNK33mC3NH3RTjL/w7Zxvn2CmGJ+ie9+a17NAmNESzNIg9MErJ10OG/GZErXv5CDBxus7qwZyoLm5uKTEXevujn2wdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('fcf5a0840972af3aaeef71903221ef58')

# 監聽所有來自 /callback 的 Post Request
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

glasses=0;
air=0;
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global glasses;
    global air;
    status=1;
    msg=event.message.text;
    
    if "垃圾車" in msg:
        txt=getrubbishtruck();
    elif "蠟筆小新" in msg:
        message=ImageSendMessage(original_content_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3fsAvfV91zePne1n1RzxuxhnKyQEXUSEVFvYvZAiHqzPJUhlIJQ&s',preview_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3fsAvfV91zePne1n1RzxuxhnKyQEXUSEVFvYvZAiHqzPJUhlIJQ&s');
        status=2;
    elif "眼鏡" in msg:
        glasses=1;
        txt=function.getproduct();
    elif "空氣" in msg:
        air=1;
        txt='請輸入一個地區名稱(例如:大里)';
    elif "測試" in msg:
        txt=function.gettest();
    else:
        if glasses==1:
            txt=function.getproduct(msg);
            glasses=0;
        elif air==1:
            txt=function.getOpenData_pm25(msg);
            air=0;
        else:
            txt=getTextKey(msg);
        #txt=event.message.text;
    if status==1:
        message = TextSendMessage(text=txt);

    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
import requests;
import json;
#引入自定義function
import function;
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
