# -*- coding: utf-8 -*-
"""
API集
@author: 張仲威
"""
import json; #爬網站資料格式需要
import requests; #爬網站資料需要
import numpy as np;
import configparser; #讀取設定檔
from vectorizer import vect;
import psycopg2; #postgresql

#讀取設定檔
config = configparser.ConfigParser()
config.read('config.ini')

#postgresql資料庫資訊
database=config['Postgresql']['database'];
user=config['Postgresql']['user'];
password=config['Postgresql']['password'];
host=config['Postgresql']['host'];
port=config['Postgresql']['port'];

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
    url = "https://taskudic.azurewebsites.net/qnamaker/knowledgebases/69d9a0dc-5394-40fb-9789-725a309e877f/generateAnswer"
    # 發送request到QnAMaker Endpoint要答案
    response = requests.post(
                   url,
                   json.dumps({'question': message_text}),
                   headers={
                       'Content-Type': 'application/json',
                       'Authorization': 'EndpointKey 6641f56a-7bae-4b95-b065-f44722b795a2'
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
        return "找答案過程發生錯誤"
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
#用字典的方式去抓關鍵字
def getTextKey(text):
    content={
            "中興":"一所很好的大學喔",
            "空污":"請輸入空氣品質抓取",
            };
    return content.get(text,"我也不知道");