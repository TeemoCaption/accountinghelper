from cgitb import handler
from os import abort
from flask import Flask, jsonify, request, abort,render_template
import pymongo
from collections import defaultdict
import json
import datetime
#from app import *
#=======LineBot相關套件引入==========
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
line_bot_api = LineBotApi('此處放你的Channel access token')


# 要獲得mongodb網址，請至mongodb網站申請帳號進行資料庫建立，網址　https://www.mongodb.com/
# 獲取的網址方法之範例如圖： https://i.imgur.com/HLCk99r.png
client = pymongo.MongoClient("此處放你的資料庫連線")


#第一個db的建立
db = client['LineBot_AccountHelper']
col = db['AccountHelper']
col2=db['Record']


#print(client.database_names())#列出client中的資料庫名稱
#print(db.collection_names())#列出db中的集合名稱
print(col.count_documents({}))#計算col中的文檔(資料)數量


#判斷key是否在指定的dictionary當中，若有則return True
def dicMemberCheck(key, dicObj):
    if key in dicObj:
        return True
    else:
        return False


#寫入資料data是dictionary

def write_one_data(user,m_class,date,m_type,item,money,keep): 
    i=0
    while(True):
        if(col2.count_documents({"rid":i})!=0):
            i+=1
        elif(col2.count_documents({"rid":i})==0):
            col2.insert_one({"rid":i})
            break
            
    date=str(date).replace('T',' ')
    money=int(money)
    post={"rid":i,"user_id": user,"class":m_class,"date":date,"type":m_type,"item":item,"money":money,"keep":keep}
    col.insert_one(post)
    
    
  


#寫入多筆資料，data是一個由dictionary組成的list
def write_many_datas(data):
    col.insert_many(data)

#讀取所有符合日期的資料
def read_date(user,date):
    target_date="^"+str(date)
    data_list=[]
    for data in col.find({'user_id': user,'date':{'$regex':target_date}}):  # $regex正規表達式
        if(str(data.get('keep'))=='' or str(data.get('keep'))=='無'):
            null_str='無'
            data_list.append([str(data.get('rid')),str(data.get('user_id')),str(data.get('class')),str(data.get('type')),str(data.get('item')),str(data.get('money')),str(null_str)])
    return data_list



#刪除所有資料
def delete_all_data():
    data_list = []
    for x in col.find():
        data_list.append(x)   

    datas_len = len(data_list)

    col.delete_many({})

    if len(data_list)!=0:
        return f"資料刪除完畢，共{datas_len}筆"
    else:
        return "資料刪除出錯"

#找到最新的一筆資料
def col_find(key):
    for data in col.find({}).sort('_id',-1):
        if dicMemberCheck(key,data):
            data = data[key]
            break
    print(data)
    return data

def updateData(rid,m_class,date,m_type,item,money,keep):
    date=str(date).replace('T',' ')
    money=int(money)
    post={"$set":{"class":m_class,"date":date,"type":m_type,"item":item,"money":money,"keep":keep}}
    col.update_one({"rid":rid}, post,upsert=True)
    message="修改完成"
    return message

def find_income(user_id):
    today=datetime.date.today()
    date=str(today)[:7]
    data_list=[]
    for data in col.find({'user_id':user_id,"date":{'$regex':".*"+date+".*"},"class":"收入"}):
        data_list.append([str(data.get('type')),int(data.get('money')),str(data.get('user_id'))])
    return data_list


def find_expenditure(user_id):
    today=datetime.date.today()
    date=str(today)[:7]
    data_list=[]
    for data in col.find({'user_id':user_id,"date":{'$regex':".*"+date+".*"},"class":"支出"}):
        data_list.append([str(data.get('type')),int(data.get('money')),str(data.get('user_id'))])
    return data_list

def everyday(user_id):
    today=datetime.date.today()
    date=str(today)[:7]
    data_list=[]
    for data in col.find({'user_id':user_id,"date":{'$regex':".*"+date+".*"}}):
        data_list.append([str(data.get('class')),int(data.get('money')),str(data.get('user_id')),str(data.get('date'))])
    data_sorted=list()
    data_sorted=sorted(data_list,key=lambda s:s[3])
    return data_sorted

def delete_data(user,r):
    rid=int(r)
    col.delete_one({"user_id":user,"rid":rid})
    col2.delete_one({"rid":rid})
    message=TextSendMessage(text="刪除成功!!!")
    return message