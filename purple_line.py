#BE77FF
import json
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
    TextMessage,
    FlexSendMessage
)
from firebase_admin import firestore
import flex_data
#Uf171df1115262137b6032675dc44c69b
def purple_1(event, line_bot_api, user_db):
    doc = user_db.get().to_dict()
    if doc['purple']['progress'] == 0:
        user_db.update({'purple.progress':1})
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='綻放新能之花',
                contents=flex_data.game_data('purple','start','')
            )
        )
        string = '請仔細閱讀以下訊息：\n\n總是在吧檯與朋友歡慶的正弦波；\n\n舞池中的精神小世界蘊藏著方形波的狂放能量；\n\n熱力四射的三角波登高一呼舒緩震盪的狂歡；\n\n無法被定義的鋸齒波尋覓來自月球的訊息'
        line_bot_api.push_message(
            event.source.user_id,
            FlexSendMessage(
                alt_text='綻放新能之花',
                contents=flex_data.msg_data('purple',string)
            )
        )
    else:
        string = '請仔細閱讀以下訊息：\n\n總是在吧檯與朋友歡慶的正弦波；\n\n舞池中的精神小世界蘊藏著方形波的狂放能量；\n\n熱力四射的三角波登高一呼舒緩震盪的狂歡；\n\n無法被定義的鋸齒波尋覓來自月球的訊息'
        
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='綻放新能之花',
                contents=flex_data.msg_data('purple',string)
            )
        )

        
        
def purple_2to4(id,line_bot_api, user_db, wave):
    doc = user_db.get().to_dict()
    waves = ''
    percent = 0
    if doc['purple']['sine'] == 1:
        waves = waves + '正弦波\n'
        percent = percent + 1
    if doc['purple']['square'] == 1:
        waves = waves + '方形波\n'
        percent = percent + 1
    if doc['purple']['triangle'] == 1:
        waves = waves + '三角波\n'
        percent = percent + 1
    if doc['purple']['sawtooth'] == 1:
        waves = waves + '鋸齒波\n'
        percent = percent + 1

    if wave == 'sine':
        string = f"不論成群結隊還是獨自一人，\n讓我們一起舉杯歡慶新能！\n\n您已收集：\n{waves}\n完成度{(percent/4)*100}%\n\n請繼續收集波形。"
        
    elif wave == 'square':
        string = f"蒐集完就快點加入人群跳舞吧！\n\n您已收集：\n{waves}\n完成度{(percent/4)*100}%\n\n請繼續收集波形。"
        
    elif wave == 'triangle':
        string = f"玩累了不妨回這裡躺一下回血，\n感受網子給你的支撐，感受周圍的聲波震盪，\n將感受打開，在不同的震動及流動中體驗這些物件及節奏組成的空間。\n\n您已收集：\n{waves}\n完成度{(percent/4)*100}%\n\n請繼續收集波形。"
        
    elif wave == 'sawtooth':
        string = f"你有聽過月兔吧？我跟他借了月球搬來了現場！\n整個月面會在新能祭落幕時剛好捲完！\n\n您已收集：\n{waves}\n完成度{(percent/4)*100}%\n\n請繼續收集波形。"
    else:
        string = f"您已收集：\n{waves}\n完成度{(percent/4)*100}%\n\n請繼續收集波形。"
        
    line_bot_api.push_message(
        id,
        FlexSendMessage(
            alt_text='綻放新能之花',
            contents=flex_data.msg_data('purple', string)
        )
    )
    

def purple_5(id, line_bot_api):
    line_bot_api.push_message(
        id,
        FlexSendMessage(
            alt_text='綻放新能之花',
            contents=flex_data.game_data('purple','end','')
        )
    )
    
    
    #新能之花 Image message
    

  
def purple_6(id,line_bot_api, user_db):
    user_db.update({'token':firestore.Increment(150)})
    string = '你獨特的波動滋養了種子，傳出陣陣美妙的電子音樂，新能姬終於綻放了新能之花。\n\n得到Bonus $150新能幣!'
    line_bot_api.push_message(
        id,
        FlexSendMessage(
            alt_text='綻放新能之花',
            contents=flex_data.msg_data('purple', string)
        )
    )