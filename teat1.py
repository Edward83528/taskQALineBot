# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 11:42:16 2019

@author: User
"""

import psycopg2;
conn=psycopg2.connect(database="ddr93dv9ort6eb",user="gxtkhrtqoowrme",password="c7602a59c8758ad0515037079e38be4e08cf7a7e44a42599e539359b2da9b9cb",host="ec2-54-225-106-93.compute-1.amazonaws.com",port="5432");
cur=conn.cursor();
print("連線成功");