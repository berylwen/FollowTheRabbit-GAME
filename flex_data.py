import json
import firebase_admin
from firebase_admin import credentials, initialize_app, storage, firestore
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
    ImageSendMessage,
    FlexSendMessage
)

def status_data(event, doc, line_bot_api):

    with open('json/status_msg.json') as f:
        data = json.load(f)
    if doc['red']['progress'] > 0:
        with open('json/beer.json') as red:
            data_red = json.load(red)
            data['contents'].append(data_red)
            if doc['red']['prize'] == 0:
                data['contents'][2]['footer']['contents'][0]['action']['label'] = '已兌換'
                data['contents'][2]['footer']['contents'][0]['color'] = '#9D9D9D'
        
    #red
    if doc['red']['progress'] == 5:
        data['contents'][0]['body']['contents'][0]['contents'][1]['text']='99%'
        data['contents'][0]['body']['contents'][1]['contents'][0]['width']='99%'
    else:    
        data['contents'][0]['body']['contents'][0]['contents'][1]['text']=f"{int(doc['red']['progress']/6*100)}%"
        data['contents'][0]['body']['contents'][1]['contents'][0]['width']=f"{int(doc['red']['progress']/6*100)}%"

    #blue  
    data['contents'][0]['body']['contents'][2]['contents'][1]['text'] = f"{str(doc['blue']['score']['team_score'])} / 501分"
    data['contents'][0]['body']['contents'][3]['contents'][0]['width'] = f"{int(doc['blue']['score']['team_score']/501*100)}%"

    #green
    data['contents'][0]['body']['contents'][4]['contents'][1]['text'] = f"{int(doc['green']['progress']/7*100)}%"
    data['contents'][0]['body']['contents'][5]['contents'][0]['width'] = f"{int(doc['green']['progress']/7*100)}%"
    #purple
    data['contents'][0]['body']['contents'][6]['contents'][1]['text'] = f"{int(doc['purple']['progress']/5*100)}%"
    data['contents'][0]['body']['contents'][7]['contents'][0]['width'] = f"{int(doc['purple']['progress']/5*100)}%"
    #pic_qr
    data['contents'][1]['body']['contents'][0]['url'] = doc['id_qrcode']
    
    if doc['blue']['team_finish'] == 1:
        data['contents'][1]['footer']['contents'][0]['action']['label'] = '已完成組隊'
        data['contents'][1]['footer']['contents'][0]['color'] = '#9D9D9D'
    
    
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='任務狀態',
            contents=data
        )
    )
        
def wallet_data(event, doc, line_bot_api):

    with open('json/wallet.json') as f:
        data = json.load(f)
        data['contents'][0]['body']['contents'][0]['contents'][1]['text']= str(doc['token'])
        
        if doc['green']['prize'] != 0:
            p_data={
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "任務獎勵："
                },
                {
                  "type": "text",
                  "text": "野格Shot x1",
                  "weight": "bold",
                  "margin": "sm"
                }
              ],
              "margin": "xl"
            }
            data['contents'][0]['body']['contents'].append(p_data)

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='我的錢包',
                contents=data
            )
        )
      


        
def game_data(game, time, msg):
    with open('json/game_first.json') as f:
        data = json.load(f)
        if game == 'green':
            if time == 'start':
                string = '綠色，是獵人的顏色，\n我們生來便是個獵人，\n獵的便是人與人之間的連結。'
                url = 'https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FGreen_mission.png?alt=media&token=165f9bc0-5dcf-4038-95ea-551202adbac1'
            else:
                if time == 'finish':
                    string = '您已完成《狩獵大師之路》，請進行其他支線。\n\n\n*欲查看持有新能幣及可兌換品項，\n請點擊選單右下角「交易購買」。'
                else:
                    string = '恭喜完成《狩獵大師之路》，\n獲得$150新能幣。\n\n\n*欲查看持有新能幣及可兌換品項，\n請點擊選單右下角「交易購買」'
                url = 'https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FGreen_mission_completed.png?alt=media&token=d9120f82-aee6-4b83-9681-773b65df5f99'
        elif game == 'blue':
            if time == 'start':
                string = '歡迎來到元宇宙牛仔的拓荒任務\n ”501 the classic”'
                url = 'https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FBlue_mission.png?alt=media&token=bedda4f6-0ccc-4d1c-874a-0db501dc8ff4'
            else:
                if time == 'finish':
                    string = '您已完成《元宇宙拓荒牛仔》，請進行其他支線。\n\n\n*欲查看持有新能幣及可兌換品項，\n請點擊選單右下角「交易購買」。'
                else:
                    string = msg
                url = 'https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FBlue_mission_completed.png?alt=media&token=9717bf14-3586-426b-b1ca-1cd272cdbcb6'
        elif game == 'red':
            if time == 'start':
                string = '紅色，是真我的顏色，\n也是這場遊戲中最重要的角色，你\n\n歡迎來到新能祭，希望你能在這抽離身體，放開自己，\n我們相信，必須要先感覺自在，你才會玩得更盡興；'
                url = 'https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FRed_mission.png?alt=media&token=c712babf-8b42-4528-b97f-4c1ab2426e2f'
            else:
                if time == 'finish':
                    string = '您已完成《保持真我之道》，請進行其他支線。\n\n\n*欲查看持有新能幣及可兌換品項，\n請點擊選單右下角「交易購買」。'
                else:
                    string = '恭喜完成《保持真我之道》，獲得$50新能幣。\n\n*欲查看持有新能幣及可兌換品項，\n請點擊選單右下角「交易購買」。\n\n\n看起來你有個充實的一天😊\n最後，想問你是否願意授權我使用你的《第一杯及最後一杯酒》，\n讓我跟大家分享新能祭有多好玩呢？'
                url = 'https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FRed_mission_completed.png?alt=media&token=9db1df41-7015-4636-bf4d-45982a3947f4'
        elif game == 'purple':
            if time == 'start':
                string = '新能之花很奇怪，它要的不是水也不是陽光。\n要讓它綻放，除了要有源源不絕的音樂，\n還要有各種波形疊加後產生的獨特波動，\n收集這些音波的能量一起綻開新能之花。\n\n任務指令：\n於紅舞台之中，收集四種基本波形。\n\n(找到波形並掃描QR Code)'
                url = 'https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FPurple_mission.png?alt=media&token=90bd4909-3c6d-4703-b921-ec78add156fe'
            else: 
                if time == 'finish':
                    string = '您已完成《綻放新能之花》，請進行其他支線。\n\n\n*欲查看持有新能幣及可兌換品項，\n請點擊選單右下角「交易購買」。'
                else:
                    string = '你蒐集到四個基本波形。\n四種波形，分別代表了四種人格特質，也因為有了這些多樣性，豐富了新能祭，進而綻放新能之花。\n\n恭喜完成《綻放新能之花》\n並成功賺取 $200新能幣\n\n*欲查看持有新能幣及可兌換品項，\n請點擊選單右下角「交易購買」。\n\n另外，我們還準備了稀有的《新能種子》特調，\n去酒吧點嚐看看吧！聽說杯底有驚喜哦👀'
                url = 'https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FPurple_mission_completed.png?alt=media&token=2e3d55e5-fbaa-4f2d-992e-b29b61cc7fec'
          
        data['header']['contents'][0]['url']= url
        data['body']['contents'][0]['text']= string
        if (game=='red') and (time=='end'):
            data['footer'] = {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "好，我樂意分享",
                      "text": "好，我樂意分享"
                    },
                    "style": "primary",
                    "margin": "none",
                    "height": "sm",
                    "color": "#4F4F4F"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "否，留給你觀賞就好",
                      "text": "否，留給你觀賞就好"
                    },
                    "style": "primary",
                    "margin": "md",
                    "height": "sm",
                    "color": "#4F4F4F"
                  }
                ]
            }
        return data

def msg_data(game, msg):
    with open('json/Msg.json') as f:
        data = json.load(f)
        if game == 'green':
            data['header']['contents'][0]['text'] = '狩獵大師之路'
            data['body']['contents'][0]['text'] = msg
            data['styles']['header']['backgroundColor'] = '#01814A'
        elif game == 'blue':
            data['header']['contents'][0]['text'] = '元宇宙拓荒牛仔'
            data['body']['contents'][0]['text'] = msg
            data['styles']['header']['backgroundColor'] = '#005AB5'
        elif game == 'red':
            data['header']['contents'][0]['text'] = '保持真我之道'
            data['body']['contents'][0]['text'] = msg
            data['styles']['header']['backgroundColor'] = '#CE0000'
        elif game == 'purple':
            data['header']['contents'][0]['text'] = '綻放新能之花'
            data['body']['contents'][0]['text'] = msg
            data['styles']['header']['backgroundColor'] = '#BE77FF'
        elif game == 'intro':
            data['header']['contents'][0]['text'] = 'Follow the Rabbit'
            data['body']['contents'][0]['text'] = msg
            data['styles']['header']['backgroundColor'] = '#3A006F'
        elif game == 'beer':
            data['header']['contents'][0]['text'] = '保持真我之道'
            data['body']['contents'][0]['text'] = '您已成功兌換百威啤酒。\n\n請點擊按鈕繼續《保持真我之道》'
            data['styles']['header']['backgroundColor'] = '#CE0000'
            data['footer'] =  {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "我拿到酒了🍺",
                      "text": "我拿到酒了"
                    },
                    "style": "primary",
                    "margin": "none",
                    "height": "sm",
                    "color": "#FF7575"
                  }
                ]
            }
              
        return data