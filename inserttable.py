# -*- coding: utf-8 -*-
"""
新增QA資料
@author: Zhong-wei
"""
import psycopg2; #postgresql
import configparser; #讀取設定檔
#讀取設定檔
config = configparser.ConfigParser()
config.read('config.ini')

#postgresql資料庫資訊
database=config['Postgresql']['database'];
user=config['Postgresql']['user'];
password=config['Postgresql']['password'];
host=config['Postgresql']['host'];
port=config['Postgresql']['port'];

conn=psycopg2.connect(database=database,user=user,password=password,host=host,port=port);
insertsql="insert into  question(subject,answer)values('申請臨時道路',1)";
insertsql2="insert into  answer(content)values('至警局辦理'),('拿取表單')";
cur=conn.cursor();
cur.execute(insertsql);
cur.execute(insertsql2);
conn.commit();
conn.close();
