from crypt import methods
from email import message
from flask import Flask, jsonify, request, abort,render_template
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from liffpy import (
    LineFrontendFramework as LIFF,
    ErrorResponse
)

#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
from mongodb_function import *
from edit_message import select_date,find_date
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__,template_folder='templates')
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('Tnn7ruaJTFJSF065VRDLe7T5DqGpzXLKHlKdISIRzr3A1qyjB7UvgPve40QMHmWlPvDvvXFuoeyodR6wmn6fwIciyBL7uBDAsd2NjdjbuLVFSRO2oDjms4imFs8jz+PShjzYojdlWOd0eL8Z9SMyEAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a8ce48921e34d218c60bcbaf3cca1861')


#============LIFF API=================
liff_api = LIFF('Tnn7ruaJTFJSF065VRDLe7T5DqGpzXLKHlKdISIRzr3A1qyjB7UvgPve40QMHmWlPvDvvXFuoeyodR6wmn6fwIciyBL7uBDAsd2NjdjbuLVFSRO2oDjms4imFs8jz+PShjzYojdlWOd0eL8Z9SMyEAdB04t89/1O/w1cDnyilFU=')
user_id=""
edit_list=""

try:
    now_LIFF_APP_number = len(liff_api.get())
except:
    now_LIFF_APP_number = 0

target_LIFF_APP_number = 10
print(target_LIFF_APP_number,now_LIFF_APP_number)
if now_LIFF_APP_number < target_LIFF_APP_number:
    for i in range(target_LIFF_APP_number - now_LIFF_APP_number):
        liff_api.add(view_type="full",view_url="https://www.google.com")


@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST":
        m_class=request.form.get('class')
        date=str(request.form.get('date')).replace('T',' ')
        m_type=request.form.get('type')
        item=request.form.get('item')
        money=request.form.get('money')
        keep=request.form.get('keep')
        #Message={"class": m_class,"date": date,"type": m_type,"item": item,"money": money,"keep": keep}
        write_one_data(user_id,m_class,date,m_type,item,money,keep)
        message="你於"+date+"記了一筆"+m_class+"\n項目類別："+m_type+"\n項目名稱："+item+"\n金額是$"+money+"元"+"\n備註："+keep
        line_bot_api.push_message(user_id,TextSendMessage(text=message))
    return render_template("./liff.html")


@app.route("/edit_data/<num>",methods=["GET","POST"])
def edit_data(num):
    n=int(num)
    edit_data=edit_list[num]
    if request.method=="POST":
        m_class=request.form.get('class')
        date=str(request.form.get('date')).replace('T',' ')
        m_type=request.form.get('type')
        item=request.form.get('item')
        money=request.form.get('money')
        keep=request.form.get('keep')
        #message=str(data)
        updateData(edit_data[0], m_class, date, m_type, item, money, keep)
        message="紀錄更新完成"
        line_bot_api.push_message(edit_data[0],TextSendMessage(text=message))
    return render_template('./edit_data.html',data=edit_data,num=num)

    
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    global user_id
    user_id=event.source.user_id
    if '查看功能' ==msg:
        message = button_reply()
        line_bot_api.reply_message(event.reply_token, message)
    elif '我要記帳' ==msg:
        message=TextSendMessage(text="https://keepspending.herokuapp.com/")
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新合作廠商'  == msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' == msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' == msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' == msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' == msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '修改紀錄' == msg:
        message=select_date()
        line_bot_api.reply_message(event.reply_token, message)
    #elif '功能列表' in msg:
        #message = function_list()
        #line_bot_api.reply_message(event.reply_token, message)
    else:
        message = button_reply()
        line_bot_api.reply_message(event.reply_token, message)
        #TextSendMessage:傳送文字訊息     
        #ImageSendMessage:傳送圖片

@handler.add(PostbackEvent)
def get_dateData(event):
    data=event.postback.data
    date=event.postback.params['date']
    user=event.source.user_id
    message=[]
    if data=="editdate":
        message=find_date(user,date)
        global edit_list
        edit_list=read_date(user,date)
        line_bot_api.push_message(user, message)
    
    

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
