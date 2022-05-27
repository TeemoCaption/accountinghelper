from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('Tnn7ruaJTFJSF065VRDLe7T5DqGpzXLKHlKdISIRzr3A1qyjB7UvgPve40QMHmWlPvDvvXFuoeyodR6wmn6fwIciyBL7uBDAsd2NjdjbuLVFSRO2oDjms4imFs8jz+PShjzYojdlWOd0eL8Z9SMyEAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a8ce48921e34d218c60bcbaf3cca1861')

uid="Udcc2be39b00c9186e7f98d6b9b6cb1f1"
def push_message():
    #tonow = datetime.datetime.now()
    message=TextMessage(text="你今天還沒有記帳歐!要記得記帳阿!")
    line_bot_api.push_message(uid,message)    #傳給指定用戶訊息
    #threading.Thread(target=push_message).start()

  
  
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
    message=TextSendMessage(
        text="Quick Reply",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="最新合作廠商",text=imagemap_message())),
                QuickReplyButton(action=MessageAction(label="最新活動訊息",text=buttons_message())),
                QuickReplyButton(action=MessageAction(label="註冊會員",text=Confirm_Template())),
                QuickReplyButton(action=MessageAction(label="旋轉木馬",text=Carousel_Template())),
                QuickReplyButton(action=MessageAction(label="圖片畫廊",text=test())),
                QuickReplyButton(action=MessageAction(label="功能列表",text=function_list())),
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


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
