# -*- coding: utf-8 -*-
"""
新增產品資料
@author: 張仲威
"""
import psycopg2;
conn=psycopg2.connect(database="ddr93dv9ort6eb",user="gxtkhrtqoowrme",password="c7602a59c8758ad0515037079e38be4e08cf7a7e44a42599e539359b2da9b9cb",host="ec2-54-225-106-93.compute-1.amazonaws.com",port="5432");
insertsql="insert into  product(name,price)values('運動眼鏡',1000)";
insertsql2="insert into  product(name,price)values('休閒眼鏡',800),('兒童眼鏡',300)";
cur=conn.cursor();
cur.execute(insertsql);
cur.execute(insertsql2);
conn.commit();
conn.close();
