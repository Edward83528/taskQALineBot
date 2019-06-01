# -*- coding: utf-8 -*-
"""
Created on Sat May 18 19:35:53 2019

@author: User
"""
import json;
import requests;
import psycopg2;
databases='ddr93dv9ort6eb';
users='gxtkhrtqoowrme';
passwords='c7602a59c8758ad0515037079e38be4e08cf7a7e44a42599e539359b2da9b9cb';
hosts='ec2-54-225-106-93.compute-1.amazonaws.com';
ports='5432';
def getOpenData(url):
    return json.loads(requests.get(url).text);
def Dateformat(str):
    return str[0:4]+"-"+ str[4:6]+"-"+ str[6:8];
def gettest():
    return '測試成功';
def getproduct(msg='1'):
    conn=psycopg2.connect(database="ddr93dv9ort6eb",user="gxtkhrtqoowrme",password="c7602a59c8758ad0515037079e38be4e08cf7a7e44a42599e539359b2da9b9cb",host="ec2-54-225-106-93.compute-1.amazonaws.com",port="5432");
    cur=conn.cursor();
    if msg==1:
        print(msg);
        cur.execute("select * from product");
    else:
        print(msg);
        cur.execute("select name,price from product where name like '%{}%' ".format(msg));
    rows=cur.fetchall();
    content='2';
    for r in rows:
        content=content+str(r[1])+"\n";
    conn.close();
    return content;