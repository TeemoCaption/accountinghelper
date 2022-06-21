#=========Line Api套件
from linebot import LineBotApi
from linebot.models import *
from linebot.exceptions import LineBotApiError
line_bot_api = LineBotApi('Tnn7ruaJTFJSF065VRDLe7T5DqGpzXLKHlKdISIRzr3A1qyjB7UvgPve40QMHmWlPvDvvXFuoeyodR6wmn6fwIciyBL7uBDAsd2NjdjbuLVFSRO2oDjms4imFs8jz+PShjzYojdlWOd0eL8Z9SMyEAdB04t89/1O/w1cDnyilFU=')

#========Imgur Api==============
import pyimgur
import requests,json
CLIENT_ID="690045a99e48e85"

#=======檔案及套件引入
import matplotlib.pyplot as plt
from mongodb_function import *
client = pymongo.MongoClient("mongodb+srv://Teemo:edwardmb0816@accounthelper.ul59p.mongodb.net/test")
db = client['LineBot_AccountHelper']
col=db['Images']


def show_income(user_id):
    type_list=["銀行卡","生活費","出租","捐贈","股息","退款","薪水","買賣","獎金","優惠券","其他"]
    datas=find_income(user_id)
    money=[0 for i in range(12)]
    for i in range(len(datas)):
        for j in range(len(type_list)):
            if(datas[i][0]==type_list[j]):
                money[j]=datas[i][1]
                break
    
    
    message=TextSendMessage(text=str(money[1]))
    return message      