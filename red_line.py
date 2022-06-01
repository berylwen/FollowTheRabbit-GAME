#CE0000
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
    FlexSendMessage,
    VideoSendMessage
)
import flex_data
import os
from firebase_admin import storage, firestore
#Uf171df1115262137b6032675dc44c69b
def red_1(event, line_bot_api, user_db):   
    user_db.update({'red.progress':1})
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=flex_data.game_data('red', 'start','')
        )
    )
    
    string = '在「新能祭」的空間中，無論性別、年齡、種族、社會階級、性向或身體與心理的任何狀態，\n都享有各種做自己的表達方式與權利，也需要被合理且有效地尊重。\n希望你能好好享受這個 safe space ，在舞池中展現真實的自己。\n\n我先問問，現在手上有酒嗎？'
    data = flex_data.msg_data('red', string)
    data['footer'] =  {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "沒有🤷‍♂️",
              "text": "沒有"
            },
            "style": "primary",
            "margin": "none",
            "height": "sm",
            "color": "#FF7575"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "有！我正在喝🍻",
              "text": "有！我正在喝"
            },
            "style": "primary",
            "margin": "md",
            "height": "sm",
            "color": "#FF7575"
          }
        ]
    }
    line_bot_api.push_message(
        event.source.user_id,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=data
        )
    )

def red_1_5(event, line_bot_api, user_db):
    string = '那讓我請你喝一杯吧！現在至紅舞台拍張照片或影片。\n上傳到 Instagram Story，\n並 Tag @synergy.fest \n@budweiser.tw \n#真我至上。\n\n帶著發文去紅舞台的百威酒吧找百威工作人員即可兌換！\n\n（請點擊選單「遊戲現況」、\n往左滑，「領取你的百威啤酒」\n並由工作人員點擊兌換按鈕、進行兌換。）'
    
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=flex_data.msg_data('red', string)
        )
    )
    user_db.update({'red.progress':1.5})

def red_2(event, line_bot_api, user_db):
    user_db.update({'red.progress':2, 'red.video_send':1})
    string = '太好了，我要邀請你紀錄你的《第一杯與最後一杯酒》\n讓你未來可以回顧在新能祭的開心回憶！\n\n例如以下影片：'
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=flex_data.msg_data('red', string)
        )
    )
  
    line_bot_api.push_message(
        event.source.user_id,
        VideoSendMessage(
            original_content_url='https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2Ffirst%20drink_v.MP4?alt=media&token=8b07c7c3-4157-43b4-b459-4c2dc3b91001',
            preview_image_url='https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FFirst%20drink.jpg?alt=media&token=77c12e3b-81a2-45ae-9560-2666daa8922b'
        )
    )
    
    string = '任務指示：\n拍攝並回傳你的第一杯酒。\n當然，你有可能早已開喝，那就說說這是你的第幾杯吧！\n\n對著鏡頭說：\n「Hi，我是 ____，這是我在新能祭的第__杯酒。」'

    line_bot_api.push_message(
        event.source.user_id,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=flex_data.msg_data('red', string)
        )
    )
    

def red_clip(event, line_bot_api, user_db):
    doc = user_db.get().to_dict()
    if doc['red']['video_send'] == 1:
        if doc['red']['first_v'] == '':
            UserSendVideo = line_bot_api.get_message_content(event.message.id)
            path= 'video/'+ event.source.user_id + '_first.mp4'
            with open(path, 'wb') as fd:
                for chunk in UserSendVideo.iter_content():
                    fd.write(chunk)
                  
            bucket = storage.bucket()
            blob = bucket.blob(f'Video_first/{event.source.user_id}_f.mp4')
            blob.upload_from_filename(f'video/{event.source.user_id}_first.mp4')
            blob.make_public()
            os.remove(f'video/{event.source.user_id}_first.mp4')
            user_db.update({'red.video_send':0,'red.first_v':blob.public_url,'red.progress':3,'token':firestore.Increment(50)})
            string = '獲得任務獎勵：$50新能幣\n別忘了，今晚離開前分享你的最後一杯酒給我哦😊\n\n再來，我想邀請你想像自己新的可能。這個可能性可以天馬行空、不被拘束，是你 2022 年最想完成的目標。\n\n任務指示：請在此對話輸入你2022年最想完成的目標'
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='保持真我之道',
                    contents=flex_data.msg_data('red', string)
                )
            )
        else:
            UserSendVideo = line_bot_api.get_message_content(event.message.id)
            path= 'video/'+ event.source.user_id + '_last.mp4'
            with open(path, 'wb') as fd:
                for chunk in UserSendVideo.iter_content():
                    fd.write(chunk)
                  
            bucket = storage.bucket()
            blob = bucket.blob(f'Video_last/{event.source.user_id}_l.mp4')
            blob.upload_from_filename(f'video/{event.source.user_id}_last.mp4')
            blob.make_public()
            os.remove(f'video/{event.source.user_id}_last.mp4')
            user_db.update({'red.video_send':0,'red.last_v':blob.public_url,'red.progress':6})
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='保持真我之道',
                    contents=flex_data.game_data('red', 'end','')
                )
            )
            

            
    
def red_3(event, line_bot_api):
    string = '您已上傳您的第一杯酒\n別忘了，今晚離開前分享你的最後一杯酒給我哦😊\n\n再來，我想邀請你想像自己新的可能。\n這個可能性可以天馬行空、不被拘束，\n是你 2022 年最想完成的目標。\n\n任務指示：請在此對話輸入你2022年最想完成的目標'
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=flex_data.msg_data('red', string)
        )
    )

def red_4(event, line_bot_api, user_db):
    doc = user_db.get().to_dict()
    if doc['red']['progress'] < 4:
        user_db.update({'red.progress':4,'red.goal':event.message.text,'token':firestore.Increment(50)})
        string = '獲得任務獎勵：$50新能幣 \n我會在今年結束之前，關心你是否有實踐這個可能哦！\n\n\n有點微醺就可以開始跳舞了吧！\n新能紅舞台是個能讓你恣意舞動，不受旁人眼光拘束的自在空間\n請帶著你的真我進入舞台，好好享受音樂的流動吧！'
        
    else:
        string = '有點微醺就可以開始跳舞了吧！\n新能紅舞台是個能讓你恣意舞動，不受旁人眼光拘束的自在空間\n請帶著你的真我進入舞台，好好享受音樂的流動吧！'
    data = flex_data.msg_data('red', string)
    data['footer'] =  {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "進入紅舞台💃",
              "text": "進入紅舞台"
            },
            "style": "primary",
            "margin": "none",
            "height": "sm",
            "color": "#FF7575"
          }
        ]
    }
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=data
        )
    )

def red_4_5(event, line_bot_api, user_db):
    string = '對了！讓我請你喝一杯吧！\n請至紅舞台拍張照片或影片，\n上傳到 Instagram Story 並 Tag @synergy.fest @budweiser.tw #真我至上。\n帶著發文去紅舞台的百威酒吧找百威工作人員即可兌換！\n\n（請點擊選單「遊戲現況」、\n往左滑，「領取你的百威啤酒」\n並由工作人員點擊兌換按鈕、進行兌換。）'
    
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=flex_data.msg_data('red', string)
        )
    )
    user_db.update({'red.progress':4.5})

def red_5(event, line_bot_api, user_db):
    doc = user_db.get().to_dict()
    if doc['red']['progress'] < 5:       
        user_db.update({'red.progress':5,'token':firestore.Increment(50)})
        string = '希望你能在紅舞台盡情享受你的派對，\n別忘了在離開前，\n點擊紅色支線《保持真我之道》回傳你的最後一杯酒哦！'
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='保持真我之道',
                contents=flex_data.msg_data('red', string)
            )
        )
    else:
        string = '這是你的最後一杯酒了嗎？'
        data = flex_data.msg_data('red', string)
        data['footer'] = {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "⭕️",
                  "text": "YES"
                },
                "style": "primary",
                "margin": "none",
                "height": "sm",
                "color": "#FF7575"
              },
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "❌",
                  "text": "NO"
                },
                "style": "primary",
                "margin": "md",
                "height": "sm",
                "color": "#FF7575"
              }
            ]
        }

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='保持真我之道',
                contents=data
            )
        )

def red_55(event, line_bot_api, user_db, bool):
    if bool == 'YES' :
        user_db.update({'red.video_send':1})
        string = '請直接傳送『最後一杯酒』影片，\n並與我們簡單分享你今天的體驗！'
    else: 
        string = '歡迎繼續享受派對，\n別忘了要再來與我分享你的最後一杯酒🍺'
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=flex_data.msg_data('red', string)
        )
    )

    
def red_6(event, line_bot_api, user_db):
    user_db.update({'red.progress':6,'token':firestore.Increment(50)})
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=flex_data.game_data('red', 'end','')
        )
    )
    

def red_7(event, line_bot_api, user_db, bool):
    if bool == 'YES':
        user_db.update({'red.auth':1})
        string = '謝謝你的分享，晚點After Party見😇'
    else: 
        string = '還是謝謝你的分享，我會好好珍藏這個片段的！'
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='保持真我之道',
            contents=flex_data.msg_data('red', string)
        )
    )
    