from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction,
    TextMessage
)

from firebase_admin import firestore

def trade(from_id, to_id, line_bot_api, amount):
    profile_from = line_bot_api.get_profile(from_id)
    profile_to = line_bot_api.get_profile(to_id)
    line_bot_api.push_message(
        from_id,
        TextSendMessage(text=f"您成功轉出{amount}新能幣給{profile_to.display_name}。")
    )
    line_bot_api.push_message(
        to_id,
        TextSendMessage(text=f"您收到來自{profile_from.display_name}的{amount}新能幣。")
    )
        

def buy(id, amount, product, line_bot_api, doc):
    line_bot_api.push_message(
        id,
        TextSendMessage(text=f"您成功使用{amount}新能幣兌換 《{product}》。")
    )
  


def prize(id, product, line_bot_api, doc):
    line_bot_api.push_message(
        id,
        TextSendMessage(text=f"您成功兌換任務獎勵 《{product}》。")
    )
  
    
        