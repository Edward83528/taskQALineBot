# -*- coding: utf-8 -*-
"""
新增QA資料表
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
createQuestion="create table if not exists question(id serial primary key,subject varchar(500),answer int)";
createAnswer="create table if not exists answer(id serial primary key,content varchar(500))";
cur=conn.cursor();
cur.execute(createQuestion);
cur.execute(createAnswer);
conn.commit();
conn.close();
print("create success");