# -*- coding: utf-8 -*-
"""
API集
@author: Zhong-wei
"""
from linebot.models import ( MessageEvent, TextMessage, TextSendMessage, ImageSendMessage)
from linebot.models import ( QuickReply, QuickReplyButton, MessageAction )




from linebot import ( LineBotApi, WebhookHandler )
import configparser #讀取設定檔
#StickerSendMessage 
#LocationSendMessage

config = configparser.ConfigParser()    
config.read('config.ini')


line_bot_api = LineBotApi(config['Line']['token'])



import numpy as np;
import json; #爬網站資料格式需要
import requests; #爬網站資料需要
import configparser; #讀取設定檔
import psycopg2; #postgresql
import dropbox #透過dropbox上傳文件再回傳共享連結
import zipfile #壓縮檔案
import datetime #時間
from mailmerge import MailMerge #操作docx模板
#from vectorizer import vect;

#讀取設定檔
config = configparser.ConfigParser()
config.read('config.ini')

#postgresql資料庫資訊
database=config['Postgresql']['database'];
user=config['Postgresql']['user'];
password=config['Postgresql']['password'];
host=config['Postgresql']['host'];
port=config['Postgresql']['port'];

#模板填充變數
name=""
place=""

#模板1類別定義
class doc1():
    def __init__(self, name='初始姓名',place='初始位置'):
        self.name = name
        self.place = place
        
def downdoc(step,msg):
    txt=""
    global name;
    global place;
    if step==0:
        txt="開始填表，請依照流程填表,請先填寫您的姓名"
        step=step+1
    elif step==1:
        name=msg
        txt="請填寫發生地點:"
        step=step+1
    elif step==2:
        place=msg
        docclass = doc1(name,place)  #建立一個實體
        txt=docMerge(config['File']['intput'],config['File']['output'],docclass);
        step=step+1
    return txt,step
def getOpenData(url):
    return json.loads(requests.get(url,verify='False').text);
def getOpenData_pm25(area):
    url='http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json';
    #verify='False':遇https不驗證ssl
    response=json.loads(requests.get(url,verify='False').text);
    site=[];
    aqi=[];
    for stat in response:
        site.append(stat['SiteName']);
        aqi.append(stat['AQI']);
    #兩個串列併成一個字典(key value)
    data=dict(zip(site,aqi));
    score=data.get(area,"0");
    if score!='0':
        value=int(score);
        if value<=50:
            score="綠燈";
        elif value<=100:
            score="黃燈";
        elif value<=150:
            score="橘燈";
        else:
            score="紅燈";
    return score;
def Dateformat(str):
    return str[0:4]+"-"+ str[4:6]+"-"+ str[6:8];
def gettest():
    return '測試成功';
def getproduct(msg=1):
    conn=psycopg2.connect(database=database,user=user,password=password,host=host,port=port);
    cur=conn.cursor();
    if msg==1:
        print('a');
        cur.execute("select * from product");
    else:
        print('b');
        cur.execute("select name,price from product where name like '%{}%' ".format(msg));
    rows=cur.fetchall();
    content='';
    for r in rows:
        content=content+str(r[1])+"\n";
    conn.close();
    return content;
#抓垃圾車資訊
def getrubbishtruck():
    url="https://data.ntpc.gov.tw/od/data/api/28AB4122-60E1-4065-98E5-ABCCB69AACA6?$format=json";
    response=json.loads(requests.get(url).text);
    content="";
    for row in response:
        content+="垃圾車:"+row["car"]+"-"+row["location"]+"\n";
    return content;
#介接微軟qnamaker
def get_answer(message_text):
    url = config['Qnamaker']['url']
    # 發送request到QnAMaker Endpoint要答案
    response = requests.post(
                   url,
                   json.dumps({'question': message_text}),
                   headers={
                       'Content-Type': 'application/json',
                       'Authorization': config['Qnamaker']['Authorization']
                   }
               )
    data = response.json()
    try: 
        #我們使用免費service可能會超過限制（一秒可以發的request數）
        if "error" in data:
            return data["error"]["message"]
        #這裡我們預設取第一個答案
        answer = data['answers'][0]['answer']
        return answer
    except Exception:
        return "不好意思，系統發生錯誤，請稍後再試"
#獲取評論的分類結果
def classify_review(review,clf):
    label = {0:"negative",1:"positive"}
    #將評論轉成特徵向量
    X = vect.transform([review])
    #獲取評論整數類標
    Y = clf.predict(X)[0]
    #獲取評論字符串類標
    label_Y = label[Y]
    #獲取評論所屬類別概率
    proba = np.max(clf.predict_proba(X))
    #return Y,label_Y,proba
    return label_Y
#前置處理要將word加入域
#word欲插入處ctrl+F9>右鍵>編輯功能變數>類別:合併列印 功能變數名稱:MergeField 欄位名稱:變數名 格式:無
#word模板插入值
def docMerge(templatePath,outputPath,docClass):
    template = templatePath
    # 建立郵件合併文件並檢視所有欄位
    document = MailMerge(template)
    print("Fields included in {}: {}".format(template,document.get_merge_fields()))
    #替換變數值
    document.merge(
    name= docClass.name,
    place=docClass.place
    )
    document.write(outputPath)
    uploaddFileName=str(datetime.datetime.now())+'.docx'
    shareLink=put_file(outputPath,uploaddFileName) #上傳到drobox
    return "已成功填寫完本檔案並存取於警局檔案中,您可透過以下連結觀看填寫檔案"+shareLink
def put_file(path, upload_name):
    shareLink='';#drobox共享連結
    TOKEN = config['Dropbox']['TOKEN']
    dbx = dropbox.Dropbox(TOKEN)
    dbx.users_get_current_account()
    with open(path, "rb") as f:
        dbx.files_upload(f.read(), "/{}".format(upload_name))
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings('/'+upload_name)
        shareLink=shared_link_metadata.url
    return shareLink
def zip_file(file_path, zip_path):
    TOKEN = config['Dropbox']['TOKEN']
    dbx = dropbox.Dropbox(TOKEN)
    dbx.users_get_current_account()
    ziph = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
    ziph.write(file_path)
    ziph.close()
#用字典的方式去抓關鍵字
def getTextKey(text):
    content={
            "中興":"一所很好的大學喔",
            "空污":"請輸入空氣品質抓取",
            };
    return content.get(text,"我也不知道");


def Description():   #使用說明
    
    content =  '' ;
    content += "1.表單申請：\n\t貼心小幫手" + '"咪咪"' + "會協助您協助填寫表單資訊\n\n2.線上檢舉：\n\t協助檢舉交通違規等異常項目,以減少交通違規事項\n\n" +  \
                    "4.官網連結：\n\t連結台中市政府官方網站,了解更多即時消息\n\n5.位置訊息：\n\t快速搜尋距離最近的派出所";

    return content;
    
    
def sendQuickreply(event):  #快速選單(表單選擇)
    try:
        message = TextSendMessage(
            text='請選擇最喜歡的程式語言',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="Python", text="Python")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="Java", text="Java")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="C#", text="C#")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="Basic", text="Basic")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
#        txt = ''
#        txt = "錯誤";
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))    



    
    


