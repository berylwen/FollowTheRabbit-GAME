#005AB5
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
import flex_data

from firebase_admin import firestore
#Uf171df1115262137b6032675dc44c69b
def blue_1(event, line_bot_api, user_db, doc):
    user_db.update({'blue.progress':1})
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=flex_data.game_data('blue', 'start','')
        )
    )
    string = '你的任務是找到2位志同道合的夥伴一起墾荒，尋找四散在各地的標靶，對著標靶掃QR code便會射下相對應標靶的積分。'
    line_bot_api.push_message(
        event.source.user_id,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=flex_data.msg_data('blue', string)
        )
    )
    
    string = '標靶分三種分數1/50/100 \n每人對同一個標靶只能累積一次積分\n總共需要射下501分，每個隊員掃一次標靶便會開始倒扣積分，剛剛好扣到0分即整隊完成任務，數學要算好，扣超過零分就回不來了。'
    data = flex_data.msg_data('blue', string)
    data['footer'] = {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "⏭",
              "text": "next"
            },
            "style": "primary",
            "margin": "none",
            "height": "sm",
            "color": "#6CA8E5"
          }
        ]
    }
  
    line_bot_api.push_message(
        event.source.user_id,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=data
        )
    )
        

def blue_2(event, line_bot_api, user_db):
    user_db.update({'blue.progress': 2})
    string = '請點擊按鈕，並掃描您欲組隊玩家的QR Code，完成組隊（隊伍需滿3人才能進行射擊）。 \n\n若您是「被組隊」玩家，請點選下方選單中「玩家資料」即可看到您的QR Code。'
    data = flex_data.msg_data('blue', string)
    data['footer'] = {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "前往組隊",
              "uri": "https://liff.line.me/1656942328-B5drm8nV"
            },
            "style": "primary",
            "margin": "none",
            "height": "sm",
            "color": "#6CA8E5"
          }
        ]
    }
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=data
        )
    )
    

def blue_2_yet(event, line_bot_api):
    string = '尚未完成組隊，請組成三人隊伍後，即可開始射擊。'
    data = flex_data.msg_data('blue', string)
    data['footer'] = {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "前往組隊",
              "uri": "https://liff.line.me/1656942328-B5drm8nV"
            },
            "style": "primary",
            "margin": "none",
            "height": "sm",
            "color": "#6CA8E5"
          }
        ]
    }
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=data
        )
    )
    

def blue_3_msg(event, line_bot_api):
    string = '已完成組隊，即刻起開始找尋標靶並掃描QR Code射擊。'
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=flex_data.msg_data('blue', string)
        )
    )
    
def blue_2_5(id, line_bot_api, teammate):
    string = '已加入隊員，尚差一位隊員，即可開始射擊。'
    data = flex_data.msg_data('blue', string)
    data['footer'] = {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "前往組隊",
              "uri": "https://liff.line.me/1656942328-B5drm8nV"
            },
            "style": "primary",
            "margin": "none",
            "height": "sm",
            "color": "#6CA8E5"
          }
        ]
    }
    line_bot_api.push_message(
        id,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=data
        )
    )
    string = '已被加入隊伍，隊伍尚差一位隊員，即可開始射擊。'
    data = flex_data.msg_data('blue', string)
    data['footer'] = {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "前往組隊",
              "uri": "https://liff.line.me/1656942328-B5drm8nV"
            },
            "style": "primary",
            "margin": "none",
            "height": "sm",
            "color": "#6CA8E5"
          }
        ]
    }
    line_bot_api.push_message(
        teammate,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=data
        )
    )
  

def blue_3(id, line_bot_api, teammate1, teammate2):
    string = '已完成組隊，即刻起開始至「紅舞台-遊戲兌換站」附近找尋標靶並掃描QR Code射擊。'
    line_bot_api.push_message(
        id,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=flex_data.msg_data('blue', string)
        )
    )
    line_bot_api.push_message(
        teammate1,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=flex_data.msg_data('blue', string)
        )
    )
    line_bot_api.push_message(
        teammate2,
        FlexSendMessage(
            alt_text='元宇宙拓荒牛仔',
            contents=flex_data.msg_data('blue', string)
        )
    )

def blue_boom(db, id, line_bot_api, score, collection, team):
    batch = db.batch()
    name = (collection.document(id).get().to_dict())['name']
    team = collection.where('blue.team','==',team).get()
    team_mate = []
    for doc in team:
        doc = collection.document(doc.id)
        team_mate.append((doc.get().to_dict())['id'])
        batch.update(doc,{'blue.score.team_score':0,'blue.score.one':0, 'blue.score.fifty_1':0,'blue.score.fifty_2':0, 'blue.score.hundred':0,'token':firestore.Increment(-50)})
    batch.commit()
    string = f"{name}射下{score}分，您的隊伍射擊超過501分，\n分數已歸零並損失$50新能幣，\n請重新開始射擊積分標靶。"
    for m in team_mate:
        line_bot_api.push_message(
            m,
            FlexSendMessage(
                alt_text='元宇宙拓荒牛仔',
                contents=flex_data.msg_data('blue', string)
            )
        )


def blue_4(db, id, line_bot_api, score, collection, team):
    batch = db.batch()
    name= (collection.document(id).get().to_dict())['name']
    team = collection.where('blue.team','==',team).get()
    team_mate = []
    tscore = (collection.document(id).get().to_dict())['blue']['score']['team_score']
    for doc in team:
        doc = collection.document(doc.id)
        team_mate.append((doc.get().to_dict())['id'])
        batch.update(doc,{'blue.score.team_score':firestore.Increment(score)})
      
    if tscore+score == 501:
        string = f'{name}射下{score}分，您的隊伍共取得501分。\n\n恭喜完成《元宇宙拓荒牛仔》，獲得$150新能幣獎勵。\n別忘了跟你的最佳隊友們擊掌！\n\n\n*欲查看持有新能幣及可兌換品項，\n請點擊選單右下角「交易購買」。'
        for m in team_mate:
            batch.update(collection.document(m),{'blue.progress':firestore.Increment(1),'token':firestore.Increment(150)})
            line_bot_api.push_message(
                m,
                FlexSendMessage(
                    alt_text='元宇宙拓荒牛仔',
                    contents=flex_data.game_data('blue', 'end', string)
                )
            )

            
    else: 
        string = f'{name}射下{score}分，您的隊伍共取得{tscore+score}分；剩{501-(tscore+score)}分需射擊。'
        for m in team_mate:
            line_bot_api.push_message(
                m,
                FlexSendMessage(
                    alt_text='元宇宙拓荒牛仔',
                    contents=flex_data.msg_data('blue', string)
                )
            )
    batch.commit()
  
