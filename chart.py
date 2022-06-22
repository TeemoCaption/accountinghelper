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
from matplotlib.font_manager import FontProperties
client = pymongo.MongoClient("mongodb+srv://Teemo:edwardmb0816@accounthelper.ul59p.mongodb.net/test")
db = client['LineBot_AccountHelper']
col=db['Images']
plt.rcParams['font.sans-serif'] = ['SimHei'] # 步驟一（替換sans-serif字型）
plt.rcParams['axes.unicode_minus'] = False  # 步驟二（解決座標軸負數的負號顯示問題）



def show_income(user_id):
    type_list=["銀行卡","生活費","出租","捐贈","股息","退款","薪水","買賣","獎金","優惠券","其他"]
    explodes=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    datas=find_income(user_id)
    money=[0 for i in range(11)]
    for i in range(len(datas)):
        for j in range(len(type_list)):
            if(datas[i][0]==type_list[j]):
                money[j]=datas[i][1]
                break
        
    plt.figure(figsize=(6,9))
    color=["#ef233c","#219ebc","#fca311","#2ec4b6","#fcbc00","#ef9cda","#b298dc","#f4d35e","#00c49a","#9381ff","#edf67d"]
    plt.pie(money,explode=explodes,labels=type_list,colors=color,labeldistance=1.2,autopct = "%2.2f%%",shadow=False,startangle=90,pctdistance=1.1)
    plt.axis('equal') 
    plt.title("本月收入", {"fontsize" : 28})
    plt.legend(loc = "best")   
    file_path="./images/"+str(user_id)+"_1.jpg"
    plt.savefig(file_path, dpi=300, bbox_inches='tight')     
    plt.close()
    
    img_title=user_id+"_income"
    im=pyimgur.Imgur(CLIENT_ID)
    upload_image=im.upload_image(file_path,title=img_title)
    
    col.update_one({"user_id":user_id}, {"$set":{"img1_name":file_path}})    
    
    message=ImageSendMessage(preview_image_url=upload_image.link,original_content_url=upload_image.link)
    return message   


def show_expenditure(user_id):
    type_list=["飲食","日常用品","交通","居家","汽機車","娛樂","醫療保健","教育","稅","電子產品","保險"]
    explodes=[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
    datas=find_expenditure(user_id)
    money=[0 for i in range(11)]
    for i in range(len(datas)):
        for j in range(len(type_list)):
            if(datas[i][0]==type_list[j]):
                money[j]=datas[i][1]
                break
        
    plt.figure(figsize=(6,9))
    color=["#ef233c","#219ebc","#fca311","#2ec4b6","#fcbc00","#ef9cda","#b298dc","#f4d35e","#00c49a","#9381ff","#edf67d"]
    plt.pie(money,explode=explodes,labels=type_list,colors=color,labeldistance=1.2,autopct = "%2.2f%%",shadow=False,startangle=90,pctdistance=1.1)
    plt.axis('equal') 
    plt.title("本月支出", {"fontsize" : 28})
    plt.legend(loc = "best")   
    file_path="./images/"+str(user_id)+"_2.jpg"
    plt.savefig(file_path, dpi=300, bbox_inches='tight')     
    plt.close()
    
    img_title=user_id+"_income"
    im=pyimgur.Imgur(CLIENT_ID)
    upload_image=im.upload_image(file_path,title=img_title)
    
    col.update_one({"user_id":user_id}, {"$set":{"img2_name":file_path}})    
    
    message=ImageSendMessage(preview_image_url=upload_image.link,original_content_url=upload_image.link)
    return message       