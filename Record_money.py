#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

#消費紀錄訊息（確認介面訊息）
def AddRecord():
    message = TemplateSendMessage(
        alt_text='確認介面',
        template=ConfirmTemplate(
            text="你要新增一筆「收入」or「支出」?",
            actions=[
                MessageTemplateAction(
                    label="收入",
                    text="收入"
                ),
                MessageTemplateAction(
                    label="支出",
                    text="支出"
                )
            ]
        )
    )
    return message



