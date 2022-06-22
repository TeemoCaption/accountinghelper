#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *


#快速回覆訊息
def button_reply():
    message=TextSendMessage(
        text="你需要什麼幫助?",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="我要記帳",text="我要記帳")),
                QuickReplyButton(action=MessageAction(label="圖表統計",text="圖表統計")),
                QuickReplyButton(action=MessageAction(label="修改紀錄",text="修改紀錄")),
                QuickReplyButton(action=MessageAction(label="刪除紀錄",text="刪除紀錄")),
            ]
        )
    )
    return message

def chart_button():
    message=TextSendMessage(
        text="請選擇收入或支出",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="本月收入",text="本月收入")),
                QuickReplyButton(action=MessageAction(label="本月支出",text="本月支出")),
                QuickReplyButton(action=MessageAction(label="每日收支",text="每日收支"))
            ]
        )
    )
    return message