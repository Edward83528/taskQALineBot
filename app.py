from flask import Flask, request, abort,render_template
from nlp.olami import Olami #用威聖電子API
import configparser #讀取設定檔
#import pickle

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

#創建一個falsk對象
app = Flask(__name__)
#讀取設定檔
config = configparser.ConfigParser()
config.read('config.ini')
# Channel Access Token
line_bot_api = LineBotApi(config['Line']['token'])
# Channel Secret
handler = WebhookHandler(config['Line']['Channe_SECRET'])
#載入分類模型(可替換)
#clf = pickle.load(open("pkl/classifier.pkl","rb"))

#跳轉首頁
@app.route("/")
def index():
    return render_template("index.html")

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
step=0
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #全域變數定義(為了實現多輪對話)
    global glasses;
    global air;
    global step;
    status=1;#訊息種類切換定義(1:文字 2:圖片)
    
    msg=event.message.text; #接收文字訊息

    if "垃圾車" in msg:
        txt=function.getrubbishtruck();
    elif "蠟筆小新" in msg:
        message=ImageSendMessage(original_content_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3fsAvfV91zePne1n1RzxuxhnKyQEXUSEVFvYvZAiHqzPJUhlIJQ&s',
                                 preview_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3fsAvfV91zePne1n1RzxuxhnKyQEXUSEVFvYvZAiHqzPJUhlIJQ&s');
        status=2; #切換圖片類型
    elif "眼鏡" in msg:
        glasses=1;
        txt=function.getproduct();
    elif "空氣" in msg:
        air=1;
        txt='請輸入一個地區名稱(例如:大里)';
    elif "評論" in msg:
        #txt=function.classify_review(msg,clf);
        txt='評論';
    #填表之後要用圖表選單致能，我先用關鍵字測試
    elif "填表" in msg:
        txt,step=function.downdoc(step,msg);
        step=step;
    elif "測試" in msg:
        txt=function.gettest();
        
    elif msg == '@使用說明' :
        txt=function.Description();
        
    else:
        if glasses==1:
            txt=function.getproduct(msg);
            glasses=0;
        elif air==1:
            txt=function.getOpenData_pm25(msg);
            air=0;
        elif step!=0:
            txt,step=function.downdoc(step,msg);
            if step==3:step=0
            step=step;
        else:
            #txt=function.getTextKey(msg); # 用字典的方式去抓關鍵字
            txt=function.get_answer(msg) #用微軟qnamaker
            if txt=='No good match found in KB.':
                txt=Olami().nli(msg) #用威聖電子API
        #txt=event.message.text;
    if status==1:
        message = TextSendMessage(text=txt);
    line_bot_api.reply_message(
        event.reply_token,
        message)

#引入自定義function
import function;
import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
