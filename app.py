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
line_bot_api = LineBotApi('58xsi39XnfzoMg+F45Et9YImICtIsCQ4q+XENgloI2lP6eX/C5UBvycT9VuvPHFT5WdMTPQH3zdBbZp6XEfNig/xjm1f1gru62E/RkWqj19edVFazU8YYiu22P+6lJBXdGAKR0YAvoSvL9L9fCkr4QdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a47997ec5d862f32608fe9b4fb55271c')

#抓垃圾車資訊
def getrubbishtruck():
    url="https://data.ntpc.gov.tw/od/data/api/28AB4122-60E1-4065-98E5-ABCCB69AACA6?$format=json";
    response=json.loads(requests.get(url).text);
    content="";
    for row in response:
        content+="垃圾車:"+row["car"]+"-"+row["location"]+"\n";
    return content;
#用字典的方式去抓關鍵字
def getTextKey(text):
    content={
            "中興":"一所很好的大學",
            "空污":"請輸入空氣品質抓取",
            };
    return content.get(text,"我也不知道");
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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global glasses;
    status=1;
    msg=event.message.text;
    
    if "垃圾車" in msg:
        txt=getrubbishtruck();
    elif "蠟筆小新" in msg:
        message=ImageSendMessage(original_content_url='https://i.ytimg.com/vi/7JU5KAgEHCY/maxresdefault.jpg',preview_image_url='https://i.ytimg.com/vi/7JU5KAgEHCY/maxresdefault.jpg');
        status=2;
    elif "眼鏡" in msg:
        glasses=1;
        txt=function.getproduct();
    elif "測試" in msg:
        txt=function.gettest();
    else:
         txt=getTextKey(msg);
        #txt=event.message.text;
    
    if status==1:
        if glasses==1:
            txt=function.getproduct(msg);
            glasses=0;

    message = TextSendMessage(text=txt);
        
    
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
import requests;
import json;
import function;
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
