# -*- coding: utf-8 -*-
"""
API集

@author: 張仲威
"""
#爬網站資料需要
import json;
import requests;
#postgresql
import psycopg2;
#postgresql資料庫資訊
databases='ddr93dv9ort6eb';
users='gxtkhrtqoowrme';
passwords='c7602a59c8758ad0515037079e38be4e08cf7a7e44a42599e539359b2da9b9cb';
hosts='ec2-54-225-106-93.compute-1.amazonaws.com';
ports='5432';
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
    conn=psycopg2.connect(database="ddr93dv9ort6eb",user="gxtkhrtqoowrme",password="c7602a59c8758ad0515037079e38be4e08cf7a7e44a42599e539359b2da9b9cb",host="ec2-54-225-106-93.compute-1.amazonaws.com",port="5432");
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