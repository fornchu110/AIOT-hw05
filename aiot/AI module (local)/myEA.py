# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
debug =0

import os
os.getcwd()#看位置
from  pandas import DataFrame as df
import pandas as pd     # 引用套件並縮寫為 pd
import numpy as np
#from   sklearn import linear_model as lm
from sklearn.linear_model import LogisticRegression as LR
#import mysql.connector
#from sqlalchemy.types import NVARCHAR, Float, Integer
#from sqlalchemy import create_engine
#import sqlalchemy
from sklearn.svm import SVC #import SVC模型

#把資料庫用來做訓練集
myserver ="localhost"
myuser="test123"
mypassword="test123"
mydb="aiotdb"
 

#=================read Data=================#
#讀入csv作為訓練模型,要做SVM
#data=pd.read_csv("training.csv")        #載入traning.csv至data
data = pd.read_csv( "AI module (local)\\trainN.csv")

X=data['value'].values.reshape(-1,1)
Y=data['status'].values.reshape(-1,1)

#print(X.shape,type(X))

                   #將sY轉成Numpy的Array (tuple型態)
#=================read Data End=================#

#model=LR()#線性迴歸
model=SVC() #換成SVC
#model.fit(ndX,ndY)#訓練模型
model.fit(X,Y)
my_score=model.score(X,Y)
#print(my_score)
import pickle
import gzip
with gzip.GzipFile("mymodel.pgz", 'w') as f: #把模型存起來,之後資料庫可以直接抓不用重新訓練
    pickle.dump(model, f)

import pymysql.cursors

#訓練完要去pymysql測試
import pymysql.cursors
#db = mysql.connector.connect(host="140.120.15.45",user="toto321", passwd="12345678", db="lightdb")
#conn = mysql.connector.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)

c = conn.cursor()
if debug:
    input("pause.. conn.cursor() ok.......")

#====== 執行 MySQL 查詢指令 ======#
c.execute("SELECT * FROM sensors")

#====== 取回所有查詢結果 ======#
results = c.fetchall()
print(type(results))
print(results[:10])
if debug:
    input("pause ....select ok..........")

test_df = df(list(results),columns=['id','time','light','temp','humi','status'])

print(test_df.head(10))
if debug:
    input("pause..  show original one above (NOT correct).......")

testX=test_df['light'].values.reshape(-1,1)
testY=model.predict(testX)
print(model.score(testX,testY))

test_df['status']=testY
print(test_df.head(10))

if debug:
    input("pause.. now show correct one above.......")


#########################################
'''
##Example 1 ## write back mysql ###############
threshold =100
c.execute('update light set status=0 where light>'+str(threshold))
conn.commit()
#results = c.fetchall()
#print(type(results))
#print(results[:10])
input("pause ....update ok..........")
'''


##Example 2 ## write back mysql ###############
## make all status =0
c.execute('update sensors set status=0 where light>0')
#更新後動到資料要commit 
conn.commit() 

## choose status ==1 have their id available
id_list=list(test_df[test_df['status']==1].id)
print(id_list)
            
for _id in id_list:
    #print('update light set status=1 where id=='+str(_id))
    c.execute('update sensors set status=1 where id='+str(_id))

conn.commit()

if debug:
    input("pause ....update ok..........")




######### cursor close, conn close
c.close()
conn.close()

