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
    for data in datas:
        for i in range(len(type_list)):
            if(data[0]==type_list[i]):
                money[i]=money[i]+data[1]
                break
    total=0
    for i in range(12):
        total+=money[i]
    for i in range(12):
        money[i]=money[i]/total 
    plt.figure(figsize=(6,9))
    color=["#ef233c","#219ebc","#fca311","#2ec4b6","#fcbc00","#ef9cda","#b298dc","#f4d35e","#00c49a","#9381ff","#edf67d"]
    plt.pie(money,labels=type_list,pctdistance=0.6,colors=color,autopct = "%0.2f%%",textprops = {"fontsize" : 12},shadow=True)
    plt.axis('equal') 
    plt.title("本月收入", {"fontsize" : 18})
    plt.legend(loc = "best")   
    
    file_path="/images/"+str(user_id)+"_1.jpg"
    plt.savefig(file_path,bbox_inches='tight',pad_inches=0.0)     
    plt.close()
    
    img_title=user_id+"_income"
    im=pyimgur.Imgur(CLIENT_ID)
    upload_image=im.upload_image(file_path,title=img_title)
    
    col.update_one({"user_id":user_id}, {"$set":{"img1_name":file_path}})
    message=ImageSendMessage(original_content_url=upload_image.link)
    return message      