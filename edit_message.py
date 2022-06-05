#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

def select_date():
    content={
        {
            "type": "carousel",
            "contents": [
                {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_5_carousel.png"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": "你要修改哪一天的記帳紀錄?",
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                        "type": "uri",
                        "label": "點我選日期",
                        "uri": "https://linecorp.com"
                        }
                    }
                    ]
                }
                }
            ]
        }
    }
    message=FlexSendMessage(alt_text='修改紀錄-選擇日期',contents=content)
    return message