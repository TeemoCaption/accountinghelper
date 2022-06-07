#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from typing import KeysView
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
#引入檔案
from mongodb_function import *


def select_date():
    content={
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
                        "type":"datetimepicker",
                        "label":"點我選擇日期",
                        "data":"editdate",
                        "mode":"date",
                        "max":"2100-12-31",
                        "min":"1900-01-01"
                    }
                }
                ]
            }
            }
        ]
    }
    
    message=FlexSendMessage(alt_text='修改紀錄-選擇日期',contents=content)
    return message


def find_date(user,date):
    data_dict=read_date(user,date)
    message=[]
    if(len(data_dict.keys())>0):
        for i in range(len(data_dict.keys())):
            t="n"+str(i+1)
            message.append(
                TemplateSendMessage(
                    alt_text='符合的紀錄',
                    template=ButtonsTemplate(
                        thumbnail_image_url="https://pic2.zhimg.com/v2-de4b8114e8408d5265503c8b41f59f85_b.jpg",
                        title="收入支出：%s \n 類別：%s \n 項目：%s".format(data_dict[t]['class'],data_dict[t]['type'],data_dict[t]["item"]),
                        text="金額："+data_dict[t]["money"],
                        actions=[
                            URITemplateAction(
                                label="點我修改紀錄",
                                uri=""
                            )
                        ]
                    )
                )
            )
    return message