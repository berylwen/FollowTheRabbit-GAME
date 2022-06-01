from flask import Flask, request, abort, render_template
#import keep_alive

from threading import Thread
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
    VideoMessage,
    ImageSendMessage,
    FlexSendMessage
)
import os
import json
from liffpy import (
    LineFrontendFramework as LIFF,
    ErrorResponse
)
import qrcode

import green_line, blue_line, red_line, purple_line, token_use, flex_data
import firebase_admin
from firebase_admin import credentials, initialize_app, storage, firestore


app = Flask(__name__)

token = os.environ["CHANNEL_ACCESS_TOKEN"]
secret= os.environ["CHANNEL_SECRET"]
line_bot_api = LineBotApi(token)
handler = WebhookHandler(secret)
liff_api = LIFF(token)


cred = credentials.Certificate("synergy-34aeb-firebase-adminsdk-i4y1b-35613a5629.json")
firebase_admin.initialize_app(cred,{'storageBucket':'synergy-34aeb.appspot.com'})

db = firestore.client()
collection = db.collection('SYNERGY')


###GREEN
@app.route('/jager', methods=['POST','GET'])
def jager():
    if request.method=='POST':
        print('POST_j')
        id = request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['green']['progress'] < 4:
            user_db.update({'os':request.get_json()['os']})
            return 'EARLY'
        elif doc['green']['progress'] == 5:
            user_db.update({'os':request.get_json()['os'],'green.progress':6,'green.prize':0})
            green_line.green_6(id, line_bot_api)
            return str(doc['green']['progress'])
        elif doc['green']['progress'] == 7:
            return 'FINISH'
        else:
            return 'ALREADY'
    else:
        return render_template('Web_jager.html')
  
@app.route('/herb', methods=['POST','GET'])
def herb():
    if request.method=='POST':
        print('POST_h')
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['green']['progress'] < 3:
            return 'EARLY'
        elif doc['green']['progress'] == 7:
            return 'FINISH'
        else :
            if doc['green']['tools']['herb'] == 1:
                return 'ALREADY'
            if doc['green']['progress'] == 3:
                user_db.update({'green.progress':4,'green.tools.herb':1})
            elif doc['green']['progress'] == 4:
                user_db.update({'green.progress':5,'green.tools.herb':1,'green.prize':1})
            green_line.green_herb(id, line_bot_api, user_db)
            return str(doc['green']['progress'])
    else:
        return render_template('Web_herb.html')

@app.route('/boots',methods=['POST','GET'])
def boots():
    if request.method=='POST':
        print('POST_b')
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['green']['progress'] < 3:
            return 'EARLY'
        elif doc['green']['progress'] == 7:
            return 'FINISH'
        else :
            if doc['green']['tools']['boots'] == 1:
                return 'ALREADY'
            if doc['green']['progress'] == 3:
                user_db.update({'green.progress':4,'green.tools.boots':1})
            elif doc['green']['progress'] == 4:
                user_db.update({'green.progress':5,'green.tools.boots':1,'green.prize':1})
            green_line.green_boots(id, line_bot_api, user_db)
            return str(doc['green']['progress'])
    else:
        return render_template('Web_boots.html')
      
####BLUE
@app.route('/team', methods=['POST','GET'])
def team(): # 一隊幾人 -> progress
    if request.method=='POST':
        print('POST_team')
        id = request.get_json()['id']
        leader_id = request.get_json()['leader']
        mate_db = collection.document(id)
        leader_db = collection.document(leader_id)
        doc = mate_db.get().to_dict()
        doc_leader = leader_db.get().to_dict()
        if not mate_db.get().exists:
            return 'ERR'
        if doc['blue']['progress'] == 0:
            return 'EARLY'
        elif doc['blue']['progress'] == 4:
            return 'FINISH'
        if doc_leader['blue']['team_finish'] == 1:     
            return 'TEAM_FULL'
        if doc_leader['blue']['team'] == 0:
            if doc['blue']['team'] != 0:
                team_ref = collection.where('blue.team','==',doc['blue']['team']).get()
                if doc['blue']['team_finish'] == 0:
                    batch = db.batch()
                    batch.update(leader_db,{'blue.team':doc['blue']['team'],'blue.progress':3, 'blue.team_finish':1})
                    mate = []
                    for doc in team_ref:
                        doc_ = collection.document(doc.id)
                        mate.append(doc_.get().to_dict()['id'])
                        batch.update(doc_,{'blue.progress':3,'blue.team_finish':1})
                    batch.commit()
                    blue_line.blue_3(leader_id, line_bot_api, mate[0], mate[1])
                    return 'be_OK'
                else:
                    return 'be_ALREADY'
            else:
                batch = db.batch()
                sys_db = collection.document('System')
                batch.update(leader_db,{'blue.team':(sys_db.get().to_dict())['team_num']+1})
                batch.update(sys_db,{'team_num':firestore.Increment(1)})
                batch.commit()
                doc_leader = leader_db.get().to_dict()
        else:
            if doc['blue']['team'] != 0:
                return 'ALREADY'
            
        team_ref = collection.where('blue.team','==',doc_leader['blue']['team']).get()
        if len(team_ref) == 1:
            mate_db.update({'blue.team':doc_leader['blue']['team']})
            blue_line.blue_2_5(leader_id, line_bot_api, id)
            return str(doc['blue']['team']) 
        else:
            batch = db.batch()
            batch.update(mate_db,{'blue.team':doc_leader['blue']['team'],'blue.progress':3,'blue.team_finish':1})
            mate = []
            for doc in team_ref:
                doc_ = collection.document(doc.id)
                mate.append(doc_.get().to_dict()['id'])
                batch.update(doc_,{'blue.progress':3,'blue.team_finish':1})
            batch.commit()
            blue_line.blue_3(id, line_bot_api, mate[0], mate[1])
            return 'OK'   
 
    else:
        return render_template('Web_team.html')

@app.route('/score1', methods=['POST','GET'])
def score1():
    if request.method=='POST':
        print('POST_s_1')
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['blue']['progress'] < 3:
            return 'EARLY'
        elif doc['blue']['progress'] == 4:
            return 'FINISH'
        if doc['blue']['score']['one'] != 0:
            return 'ALREADY'
        if (501-doc['blue']['score']['team_score']) < 1:
            blue_line.blue_boom(db, id, line_bot_api, 1, collection, doc['blue']['team'])
            return 'BOOM'
        else:
            user_db.update({'blue.score.one':1})
            blue_line.blue_4(db, id, line_bot_api, 1, collection, doc['blue']['team'])
            return str(doc['blue']['progress'])
    else:
        return render_template('Web_score1.html')

@app.route('/score50_1', methods=['POST','GET'])
def score501():
    if request.method=='POST':
        print('POST_s_50')
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['blue']['progress'] < 3:
            return 'EARLY'
        elif doc['blue']['progress'] == 4:
            return 'FINISH'
        if doc['blue']['score']['fifty_1'] != 0:
            return 'ALREADY'
        if (501-doc['blue']['score']['team_score']) < 50:
            blue_line.blue_boom(db, id, line_bot_api, 50, collection, doc['blue']['team'])
            return 'BOOM'
        else:
            user_db.update({'blue.score.fifty_1':1})
            blue_line.blue_4(db, id, line_bot_api, 50, collection, doc['blue']['team'])
            return str(doc['blue']['progress'])
    else:
        return render_template('Web_score50_1.html')

@app.route('/score50_2', methods=['POST','GET'])
def score502():
    if request.method=='POST':
        print('POST_s_50_2')
        print()
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['blue']['progress'] < 3:
            return 'EARLY'
        elif doc['blue']['progress'] == 4:
            return 'FINISH'
        if doc['blue']['score']['fifty_2'] != 0:
            return 'ALREADY'
        if (501-doc['blue']['score']['team_score']) < 50:
            blue_line.blue_boom(db, id, line_bot_api, 50, collection, doc['blue']['team'])
            return 'BOOM'
        else:
            user_db.update({'blue.score.fifty_2':1})
            blue_line.blue_4(db, id, line_bot_api, 50, collection, doc['blue']['team'])
            return str(doc['blue']['progress'])
    else:
        return render_template('Web_score50_2.html')

@app.route('/score100', methods=['POST','GET'])
def score100():
    if request.method=='POST':
        print('POST_s_100')
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['blue']['progress'] < 3:
            return 'EARLY'
        elif doc['blue']['progress'] == 4:
            return 'FINISH'
        if doc['blue']['score']['hundred'] != 0:
            return 'ALREADY'
        if (501-doc['blue']['score']['team_score']) < 100:
            blue_line.blue_boom(db, id, line_bot_api, 100, collection, doc['blue']['team'])
            return 'BOOM'
        else:
            user_db.update({'blue.score.hundred':1})
            blue_line.blue_4(db, id, line_bot_api, 100, collection, doc['blue']['team'])
            return str(doc['blue']['progress'])
    else:
        return render_template('Web_score100.html')
      
###PURPLE
@app.route('/sine', methods=['POST','GET'])
def sine():
    if request.method=='POST':
        print('POST_s')
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['purple']['progress'] < 1:
            return 'EARLY'
        elif doc['purple']['progress'] == 5:
            return 'FINISH'
        if doc['purple']['sine'] == 1:
            return 'ALREADY'
        else:
            user_db.update({'purple.progress':firestore.Increment(1),'purple.sine':1,'token':firestore.Increment(50)})
            
            if doc['purple']['progress'] == 4:
                purple_line.purple_2to4(id, line_bot_api, user_db,'sine')            
                purple_line.purple_5(id, line_bot_api)
            else:
                purple_line.purple_2to4(id, line_bot_api, user_db,'sine')
            return str(doc['purple']['progress'])
    else:
        return render_template('Web_sine.html')

@app.route('/triangle', methods=['POST','GET'])
def triangle():
    if request.method=='POST':
        print('POST_triangle')
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['purple']['progress'] < 1:
            return 'EARLY'
        elif doc['purple']['progress'] == 5:
            return 'FINISH'
        if doc['purple']['triangle'] == 1:
            return 'ALREADY'
        else:
            user_db.update({'purple.progress':firestore.Increment(1),'purple.triangle':1,'token':firestore.Increment(50)})
            if doc['purple']['progress'] == 4:
                purple_line.purple_2to4(id, line_bot_api, user_db,'triangle')
                purple_line.purple_5(id, line_bot_api)
            else:
                purple_line.purple_2to4(id, line_bot_api, user_db,'triangle')
            return str(doc['purple']['progress'])
    else:
        return render_template('Web_triangle.html')

@app.route('/square', methods=['POST','GET'])
def square():
    if request.method=='POST':
        print('POST_sq')
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['purple']['progress'] < 1:
            return 'EARLY'
        elif doc['purple']['progress'] == 5:
            return 'FINISH'
          
        if doc['purple']['square'] == 1:
            return 'ALREADY'
        else:
            user_db.update({'purple.progress':firestore.Increment(1),'purple.square':1,'token':firestore.Increment(50)})
            if doc['purple']['progress'] == 4:
                purple_line.purple_2to4(id, line_bot_api, user_db,'square')
                purple_line.purple_5(id, line_bot_api)
            else:
                purple_line.purple_2to4(id, line_bot_api, user_db,'square')
            return str(doc['purple']['progress'])
    else:
        return render_template('Web_square.html')

@app.route('/sawtooth', methods=['POST','GET'])
def sawtooth():
    if request.method=='POST':
        print('POST_saw')
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['purple']['progress'] < 1:
            return 'EARLY'
        elif doc['purple']['progress'] == 5:
            return 'FINISH'
        if doc['purple']['sawtooth'] == 1:
            return 'ALREADY'
        else:
            user_db.update({'purple.progress':firestore.Increment(1),'purple.sawtooth':1,'token':firestore.Increment(50)})
            if doc['purple']['progress'] == 4:
                purple_line.purple_2to4(id, line_bot_api, user_db,'sawtooth')        
                purple_line.purple_5(id, line_bot_api)
            else:
                purple_line.purple_2to4(id, line_bot_api, user_db,'sawtooth')
            return str(doc['purple']['progress'])
    else:
        return render_template('Web_sawtooth.html')

@app.route('/synergy', methods=['POST','GET'])
def synergy():
    if request.method=='POST':
        print('POST_syn')
        id=request.get_json()['id']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if not user_db.get().exists:
            return 'YET'
        if doc['purple']['progress'] ==6:
            return 'ALREADY'
        elif doc['purple']['progress'] == 5:
            user_db.update({'purple.progress':6}) ###BONUS
            purple_line.purple_6(id, line_bot_api, user_db)
            return str(doc['purple']['progress'])
        else:
            return 'EARLY'
    else:
        return render_template('Web_synergy.html')
      
@app.route('/trade', methods=['POST','GET'])
def trade():
    if request.method=='POST':
        print('POST_trade')
        from_id = request.get_json()['from_id']
        to_id = request.get_json()['to_id']
        amount = int(request.get_json()['amount'])
        from_db = collection.document(from_id)
        to_db = collection.document(to_id)
        if not to_db.get().exists:
            return 'ERR'
        if amount > (from_db.get().to_dict())['token']:  
            return 'LESS'
        else:
            batch = db.batch()
            batch.update(from_db,{'token':firestore.Increment(-amount)})
            batch.update(to_db,{'token':firestore.Increment(amount)})
            batch.commit()
            token_use.trade(from_id, to_id, line_bot_api, amount)
            return 'OK'
    else:
        return render_template('Web_trade.html')
      
@app.route('/buy', methods=['POST','GET'])
def buy():
    if request.method=='POST':
        print('POST-buy')
        id = request.get_json()['id']
        amount = request.get_json()['amount']
        product = request.get_json()['product']
        user_db = collection.document(id)
        doc = user_db.get().to_dict()
        if product == '野格SHOT':
            if doc['green']['prize'] == 1:
                user_db.update({'green.prize':0})
                token_use.prize(id, product, line_bot_api, doc)
                return 'OK'
        if amount > (user_db.get().to_dict())['token']:  
            return 'LESS'
        else:
            user_db.update({'token':firestore.Increment(-amount)})
            token_use.buy(id, amount, product, line_bot_api, doc)
            return 'OK'
    else:
        return render_template('Web_buy.html')
      


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent,message=VideoMessage)
def handler_message_v(event):
    user_db = collection.document(event.source.user_id)
    red_line.red_clip(event, line_bot_api, user_db)
    

@handler.add(MessageEvent,message=TextMessage)
def handler_message(event):
    user_db = collection.document(event.source.user_id)
    doc = user_db.get().to_dict()
    profile = line_bot_api.get_profile(event.source.user_id)
    if event.message.text == '開啟任務':
        if not (user_db.get()).exists:  
            join(event, profile)
            intro(event, line_bot_api)
        else:   
            with open('json/game.json') as f:
                data = json.load(f)
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                        alt_text='開啟任務',
                        contents=data
                    )
                )
    elif event.message.text == '遊戲現況':
        if not user_db.get().exists:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請先從選單點擊「開啟任務」，開啟遊戲後才能確認任務狀態哦。')
            )  
        else:
            flex_data.status_data(event, doc, line_bot_api)
    elif event.message.text == '交易購買':
        if not user_db.get().exists:  
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請先從選單點擊「開啟任務」，開啟遊戲後才能交易哦。')
            )
    
        else:
            flex_data.wallet_data(event, doc, line_bot_api)
    elif event.message.text == 'SYNERGY節目表':
        line_bot_api.reply_message(
            event.reply_token,   
            ImageSendMessage(
              original_content_url='https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FTimetable%20D2.JPG?alt=media&token=82fca29e-3ff0-4ea1-8b85-0cdf7ab13fea', 
              preview_image_url='https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FTimetable%20D2.JPG?alt=media&token=82fca29e-3ff0-4ea1-8b85-0cdf7ab13fea')
            )
    elif event.message.text == '現場地圖':
        line_bot_api.reply_message(
            event.reply_token,   
            ImageSendMessage(
              original_content_url='https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FMap.jpg?alt=media&token=5b325a56-46c8-4ab0-aa8d-7c3bb623f889', 
              preview_image_url='https://firebasestorage.googleapis.com/v0/b/synergy-34aeb.appspot.com/o/Rabbit%2FMap.jpg?alt=media&token=5b325a56-46c8-4ab0-aa8d-7c3bb623f889')
            )
    elif event.message.text == '兌換百威':
        if doc['red']['prize'] == 1:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='保持真我之道',
                    contents=flex_data.msg_data('beer', 'text')
                )
            )
            user_db.update({'red.prize':0})
        else:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='保持真我之道',
                    contents=flex_data.msg_data('red', '您已兌換過百威啤酒。')
                )
            )
    elif event.message.text == 'Reset_G':
        user_db.update({'green':{'progress':0,'status':0,'tools':{'herb':0,'boots':0},'prize':0}})
    elif event.message.text == 'Reset_B':
        user_db.update({'blue':{'progress':0,'status':0,'team':0,'team_finish':0, 'score':{'one':0,'fifty_1':0, 'fifty_2':0, 'hundred':0,'team_score':0}}})
    elif event.message.text == 'Reset_Head':
        user_db.delete()
    elif event.message.text == 'Reset_P':
        user_db.update({'purple':{'progress':0,'status':0,'sine':0,'triangle':0,'square':0,'sawtooth':0}})
    elif event.message.text == 'Reset_R':
        user_db.update({'red':{'progress':0,'status':0,'video_send':0,'prize':1 ,'goal':'','first_v':'','last_v':'','auth':0}})
    elif event.message.text == 'GO':
        if (doc['green']['progress']==0) and (doc['red']['progress']==0) and (doc['blue']['progress']==0) and (doc['purple']['progress']==0):
            string = '下方選單列有五大功能：\nSYNERGY節目單\n\n現場地圖\n\n開啟任務：您將探索新能祭的四大主線任務。\n\n遊戲現況：供您查詢遊戲進度，以及組隊所需的玩家ID。\n\n交易購買：闖關所賺得的獎勵及新能幣，可透過掃描QR code，\n\n在紅舞台一進門的遊戲兌換站，兌換為實體物品。\n\n\n*本遊戲部分獎勵採限量供應，稀有物品若兌換完恕不補貨，請加快腳步。'
            data = flex_data.msg_data('intro', string)
            data['footer'] =  {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "開啟任務🐇",
                      "text": "開啟任務"
                    },
                    "style": "primary",
                    "margin": "none",
                    "height": "sm",
                    "color": "#3A006F"
                  }
                ]
            }
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='FOLLOW THE RABBIT',
                    contents=data
                )
            )
    elif event.message.text =='狩獵大師之路':
        if not user_db.get().exists:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='您尚未開啟遊戲，請點擊選單「開啟任務」。')
            )
        progress = doc['green']['progress']

        if progress == 7:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='狩獵大師之路',
                    contents=flex_data.game_data('green', 'finish','')
                )
            )  
        else:
            user_db.update({'green.status':1, 'blue.status':0, 'red.status':0, 'purple.status':0})
            if progress == 0:
                green_line.green_1(event, line_bot_api, user_db)
            elif progress == 1:
                green_line.green_1(event, line_bot_api, user_db)
            elif progress == 2:
                green_line.green_2(event, line_bot_api, user_db)
            elif progress == 3:
                green_line.green_3(event, line_bot_api, user_db)
            elif progress == 4:
                green_line.green_4(event, line_bot_api, user_db)
            elif progress == 5:
                green_line.green_5(event, line_bot_api)
            elif progress == 6:
                green_line.green_6(event, line_bot_api)
            
    elif event.message.text =='元宇宙拓荒牛仔':
        if not user_db.get().exists:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='您尚未開啟遊戲，請點擊選單「開啟任務」。')
            )
        progress = doc['blue']['progress']
        if progress == 4:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='元宇宙狩獵大師',
                    contents=flex_data.game_data('blue', 'finish','')
                )
            )  
        else:
            user_db.update({'green.status':0, 'blue.status':1, 'red.status':0, 'purple.status':0})
            if progress == 0:
                blue_line.blue_1(event, line_bot_api, user_db, doc)
            elif progress == 1:
                blue_line.blue_2(event, line_bot_api, user_db)
            elif progress == 2:
                blue_line.blue_2_yet(event, line_bot_api)
            elif progress == 3:
                blue_line.blue_3_msg(event, line_bot_api)
    
    elif event.message.text =='保持真我之道':
        if not user_db.get().exists:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='您尚未開啟遊戲，請點擊選單「開啟任務」。')
            )
        progress = doc['red']['progress']

        if progress == 6:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='保持真我之道',
                    contents=flex_data.game_data('red', 'finish','')
                )
            )  
        else:
            user_db.update({'green.status':0, 'blue.status':0, 'red.status':1, 'purple.status':0})
            if progress == 0:
                red_line.red_1(event, line_bot_api, user_db)
            elif progress == 1:
                red_line.red_1(event, line_bot_api, user_db)
            elif progress == 1.5:
                red_line.red_1_5(event, line_bot_api, user_db)
            elif progress == 2:
                red_line.red_2(event, line_bot_api, user_db)
            elif progress == 3:
                red_line.red_3(event, line_bot_api)
            elif progress == 4:
                red_line.red_4(event, line_bot_api,user_db)
            elif progress == 4.5:
                red_line.red_4_5(event, line_bot_api,user_db)
            elif progress == 5:
                red_line.red_5(event, line_bot_api, user_db)
                
    elif event.message.text =='綻放新能之花':
        if not user_db.get().exists:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='您尚未開啟遊戲，請點擊選單「開啟任務」。')
            )
        progress = doc['purple']['progress']
        if progress == 5:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='綻放新能之花',
                    contents=flex_data.game_data('purple', 'finish','')
                )
            )  
        else:
            user_db.update({'green.status':0, 'blue.status':0, 'red.status':0, 'purple.status':1})
            if progress < 2:
                purple_line.purple_1(event, line_bot_api, user_db)
            elif (progress > 1) and (progress < 5) :
                purple_line.purple_2to4(event, line_bot_api, user_db,'else')
    elif event.message.text == 'next':
        if doc['green']['status'] == 1:
            if doc['green']['progress'] == 1:
                green_line.green_2(event, line_bot_api, user_db)
            elif doc['green']['progress'] == 2:
                green_line.green_3(event, line_bot_api, user_db)                
        elif doc['blue']['status'] == 1:
            blue_line.blue_2(event, line_bot_api, user_db) 
    elif (event.message.text).lower() == '#save the night': 
        if doc['green']['progress'] < 6:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='請先從選單開啟《狩獵大師之路》，並取得獵人資格。')
            )  
        elif doc['green']['progress'] == 6:
            green_line.green_7(event, line_bot_api, user_db)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='狩獵大師之路',
                    contents=flex_data.game_data('green', 'finish','')
                )
            )
    elif doc['green']['status'] == 1:
        if event.message.text =='誰是聖·休伯特斯?':    
            green_line.green_saint(event, line_bot_api)
        elif event.message.text == '直接進行任務':
            if (doc['green']['status'] == 1) and (doc['green']['progress'] == 1):
                green_line.green_2(event, line_bot_api, user_db)

    elif doc['red']['status'] == 1:
        if event.message.text == '好，我樂意分享':
            if doc['red']['progress'] == 6:
                red_line.red_7(event, line_bot_api, user_db, 'YES') 
        elif event.message.text == '否，留給你觀賞就好':
            if doc['red']['progress'] == 6:
                red_line.red_7(event, line_bot_api, user_db, 'NO') 
        elif (event.message.text == 'YES') or (event.message.text == 'NO'):
            if doc['red']['progress'] == 5:
                red_line.red_55(event, line_bot_api, user_db, event.message.text)
        elif event.message.text == '沒有':
            if doc['red']['progress'] == 1:
                red_line.red_1_5(event, line_bot_api, user_db)
        elif event.message.text == '有！我正在喝':
            if doc['red']['progress'] == 1:
                red_line.red_2(event, line_bot_api, user_db)
        elif event.message.text == '我拿到酒了':
            if doc['red']['progress'] == 1.5:
                if doc['red']['prize'] == 0:
                    red_line.red_2(event, line_bot_api, user_db)
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text = '您尚未完成兌換，\n請點擊選單「遊戲現況」\n從「領取你的百威啤酒」進行兌換。')
                    )
            elif doc['red']['progress'] == 4.5:
                if doc['red']['prize'] == 0:
                    red_line.red_5(event, line_bot_api, user_db)
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text = '您尚未完成兌換，\n請點擊選單「遊戲現況」\n從「領取你的百威啤酒」進行兌換。')
                    )
        elif doc['red']['progress'] == 3:
            print('AFTER GOAL')
            red_line.red_4(event, line_bot_api, user_db)
        elif event.message.text == '進入紅舞台':
            if doc['red']['prize'] == 1:
                red_line.red_4_5(event, line_bot_api, user_db)
            else:
                red_line.red_5(event, line_bot_api, user_db)

          
    
    
def join(event, profile):
    doc = collection.document(event.source.user_id)
    img = qrcode.make(event.source.user_id)
    img.save(f'User_qrcodes/{event.source.user_id}.png')
    bucket = storage.bucket()
    blob = bucket.blob(f'User_qrcodes/{event.source.user_id}.png')
    blob.upload_from_filename(f'User_qrcodes/{event.source.user_id}.png')
    # Opt : if you want to make public access from the URL
    blob.make_public()
    os.remove(f'User_qrcodes/{event.source.user_id}.png')
    member = {'id':event.source.user_id,
              'id_qrcode':blob.public_url,
              'name':profile.display_name,
              'green':{'progress':0,'status':0, 'prize':0,'tools':{'herb':0,'boots':0}},
              'blue':{'progress':0,'status':0,'team':0,'team_finish':0,'score':{'one':0,'fifty_1':0, 'fifty_2':0, 'hundred':0,'team_score':0}},
              'red':{'progress':0,'status':0,'video_send':0,'prize':1 ,'goal':'','first_v':'','last_v':'','auth':0},
              'purple':{'progress':0,'status':0,'sine':0,'triangle':0,'square':0,'sawtooth':0}, 
              'token':0,
              'os':''
    }
    doc.set(member)

def intro(event, line_bot_api):
    with open('json/game.json') as f:
        data = json.load(f)
        data['body']['contents'][1]['text'] = '歡迎登入新能祭遊戲系統，\n我是你的領航員新能兔。\n\n《Follow The Rabbit 》\n現場限定遊戲將帶著你穿梭虛實，探索新能祭，\n還能破關領取獎勵與酒水，\n準備好的話就出發吧！'
        data['footer'] = {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "GO!",
                  "text": "GO"
                },
                "style": "primary",
                "margin": "none",
                "height": "sm",
                "color": "#3A006F"
              }
            ]
        }
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='開啟任務',
                contents=data
            )
        )
    
        
  

@app.route('/')
def main():
	return 'Bot is aLive!'

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

if __name__ == "__main__":
    keep_alive()
    #app.run(host='0.0.0.0', port=8080)

#host='0.0.0.0', port=8080

'''elif 'https' in event.message.text:
        try:
            print('TRY')
            #新增LIFF頁面到LINEBOT中
            liff_id = liff_api.add(
                view_type="tall",
                view_url='https://rabbit-line.rong012321.repl.co/boots')
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text = f'https://liff.line.me/{liff_id}'))
        except:
            print('Error')
'''

