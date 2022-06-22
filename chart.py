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
    explodes=[0,0,0,0,0,0,0,0,0,0,0]
    color=["#ef233c","#219ebc","#fca311","#2ec4b6","#fcbc00","#ef9cda","#b298dc","#f4d35e","#00c49a","#9381ff","#edf67d"]
    money=[0 for i in range(11)]
    money_list=list()
    types=list()
    colors=list()
    explode=list()
    
    datas=find_income(user_id)
    
    for i in range(len(datas)):
        for j in range(len(type_list)):
            if(datas[i][0]==type_list[j]):
                money[j]=datas[i][1]
                break
    for i in range(len(money)):
        if(money[i]!=0):
            money_list.append(money[i])
            types.append(type_list[i])
            colors.append(color[i])
            explode.append(0)
    
    plt.figure(figsize=(6,9))
    plt.pie(money_list,explode=explode,labels=types,colors=colors,labeldistance=1.2,autopct = "%2.2f%%",shadow=False,startangle=90,pctdistance=1.1)
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
    explodes=[0,0,0,0,0,0,0,0,0,0,0]
    color=["#ef233c","#219ebc","#fca311","#2ec4b6","#fcbc00","#ef9cda","#b298dc","#f4d35e","#00c49a","#9381ff","#edf67d"]
    money=[0 for i in range(11)]
    money_list=list()
    types=list()
    colors=list()
    explode=list()
    
    datas=find_expenditure(user_id)
    
    for i in range(len(datas)):
        for j in range(len(type_list)):
            if(datas[i][0]==type_list[j]):
                money[j]=datas[i][1]
                break
    for i in range(len(money)):
        if(money[i]!=0):
            money_list.append(money[i])
            types.append(type_list[i])
            colors.append(color[i])
            explode.append(0)
    
    plt.figure(figsize=(6,9))
    plt.pie(money_list,explode=explode,labels=types,colors=colors,labeldistance=1.2,autopct = "%2.2f%%",shadow=False,startangle=90,pctdistance=1.1)
    plt.axis('equal') 
    plt.title("本月支出", {"fontsize" : 28})
    plt.legend(loc = "best")   
    file_path="./images/"+str(user_id)+"_2.jpg"
    plt.savefig(file_path, dpi=300, bbox_inches='tight')     
    plt.close()
    
    img_title=user_id+"_expenditure"
    im=pyimgur.Imgur(CLIENT_ID)
    upload_image=im.upload_image(file_path,title=img_title)
    
    col.update_one({"user_id":user_id}, {"$set":{"img2_name":file_path}})    
    
    message=ImageSendMessage(preview_image_url=upload_image.link,original_content_url=upload_image.link)
    return message   


def line_chart(user_id):
    datas=everyday(user_id)
    date=list()
    date.append(str(datas[0][3])[:10])
    in_money=[0]
    out_money=[0]
    a=0
    for i in range(len(datas)):
        if(str(datas[i][3])[:10] in date):
            if(datas[i][0]=="收入"):
                in_money[a]+=datas[i][1]
                out_money[a]+=0
            elif(datas[i][0]=="支出"):
                out_money[a]+=datas[i][1]
                in_money[a]+=0
        elif(str(datas[i][3])[:10] not in date):
            date.append(datas[i][3])
            in_money.append(0)
            out_money.append(0)
            a+=1
            if(datas[i][0]=="收入"):
                in_money[a]+=datas[i][1]
                out_money[a]+=0
            elif(datas[i][0]=="支出"):
                out_money[a]+=datas[i][1]
                in_money[a]+=0
            
        
    plt.figure(figsize=(20,10),dpi=300,linewidth = 4)
    plt.plot(date,in_money,'o-',color = 'b', label="收入")
    plt.plot(date,out_money,'o-',color = 'r', label="支出")
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel("日", fontsize=30, labelpad = 15)  # 標示x軸(labelpad代表與圖片的距離)
    plt.ylabel("金額", fontsize=30, labelpad = 20)  # 標示y軸(labelpad代表與圖片的距離)
    plt.legend(loc = "best", fontsize=20)
    
    file_path="./images/"+str(user_id)+"_3.jpg"
    plt.savefig(file_path, dpi=300, bbox_inches='tight')     
    plt.close()
    
    
    img_title=user_id+"_everyday"
    im=pyimgur.Imgur(CLIENT_ID)
    upload_image=im.upload_image(file_path,title=img_title)
    
    col.update_one({"user_id":user_id}, {"$set":{"img3_name":file_path}})    
    
    message=ImageSendMessage(preview_image_url=upload_image.link,original_content_url=upload_image.link)
    return message   