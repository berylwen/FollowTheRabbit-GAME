#01814A
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
    LocationSendMessage,
    FlexSendMessage
)

from firebase_admin import firestore
import flex_data


#Uf171df1115262137b6032675dc44c69b
def green_1(event,line_bot_api, user_db):
    user_db.update({'green.progress':1})
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='狩獵大師之路',
            contents=flex_data.game_data('green','start','')
        )
    )
    string = '你將在這趟旅程中，穿梭虛實，體驗獵人在元宇宙之中的角色。\n我們狩獵，但取之有道，不強求他人，這是「狩獵大師」的精神，也是聖·休伯特斯作為守護聖者對於獵人們的期許。'
    data = flex_data.msg_data('green', string)
    data['footer'] =  {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "直接進行任務",
              "text": "直接進行任務"
            },
            "style": "primary",
            "margin": "none",
            "height": "sm",
            "color": "#4F9D9D"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "誰是聖·休伯特斯?",
              "text": "誰是聖·休伯特斯?"
            },
            "style": "primary",
            "margin": "md",
            "height": "sm",
            "color": "#4F9D9D"
          }
        ]
    }
    line_bot_api.push_message(
        event.source.user_id,
        FlexSendMessage(
            alt_text='狩獵大師之路',
            contents=data
        )
    )

def green_saint(event, line_bot_api):
    string = '在基督教的信仰體系中，有一類人被稱作守護聖者，這是對承認基督以及徹底實踐教義者的尊稱。被冊封爲守護聖者的人，通常都會在某些領域的代替禱告特別靈驗，相當於佛教上師替你開光。\n\n有一位叫Saint Hubertus（聖·休伯特斯）的人，就是德國神話傳說中獵人的守護聖者。靠著老爹是個公爵，休伯特斯在青年時代一度終日玩樂，不光如此，他還沉迷於狩獵並嗜殺成性。\n\n在一次日常的狩獵途中，休伯特斯遇到了生平從未見過的巨大雄鹿。他自然激動不已，尋著腳印一路追了上去，但就在休伯特斯準備給雄鹿致命一箭的時候，雄鹿突然轉頭開口說話了。\n\n「休伯特斯，快快放下你手中的箭矢，信仰主、服侍主，過聖潔的生活好好修行吧，否則你一定會下地獄的！！！」\n\n詭異的是，這頭雄鹿不僅會開口說話，頭上還頂著發光的十字架。眼前的種種景象嚇的休伯特斯屁滾尿流，連連下跪祈禱。\n雄鹿淡定的說道：「去找一位叫lande bertus的主教，他會指引罪惡的你通往天堂。（說完雄鹿就化作白光消失了）」\n\n此後，受過神跡洗禮的休伯特斯就選擇擁抱上帝，開始與主教lande bertus修行。他放棄了爵位，捐獻了一切財富，餘生致力於傳教。據說他曾徒步走到羅馬一路行善，幫人驅魔醫治百病，展現神跡無數。\n\n在他死後，休伯特斯被追封爲獵人的守護聖者，負責祝福並守護每一位獵人。\n休伯特斯的傳奇故事，一直是德國職業獵人心中的啓示錄。野格的創始人Curt Mast（庫爾特·馬斯特）亦是如此，馬斯特從小受到獵人父親的薰陶，自然也對這些故事奉爲圭臬。'
    data = flex_data.msg_data('green', string)
    data['footer'] =  {
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
            "color": "#4F9D9D"
          }
        ]
    }
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='狩獵大師之路',
            contents=data
        )
    )
def green_2(event, line_bot_api, user_db):
    user_db.update({'green.progress':2})
    string = '今天，我需要你的協助，解救一頭被監禁的聖鹿，\n因為祂的失蹤，導致祂所掌管的夜晚也一併失控了，事不宜遲請儘速出發。'
    data = flex_data.msg_data('green', string)
    data['footer'] =  {
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
            "color": "#4F9D9D"
          }
        ]
    }
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='狩獵大師之路',
            contents=data
        )
    )
    

def green_3(event, line_bot_api, user_db):
    user_db.update({'green.progress':3})
    string = '首先，我們要進行進入獵場的儀式：一杯壯膽的野格shot。\n\n任務指示：\n前往最近的酒吧，點一杯野格shot並掃描杯子上的QR Code。\n\n（請以您常用之QR Code掃瞄方式掃描即可。）'
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='狩獵大師之路',
            contents=flex_data.msg_data('green', string)
        )
    )
    
def green_4(id, line_bot_api):
    string = '恭喜完成儀式，接下來請你搜集兩項必備道具，\n方能進入最終的獵人小屋，找到聖鹿並解放它。\n\n任務指示：搜集獵人必備的藥草與獵靴。'

    line_bot_api.push_message(
        id,
        FlexSendMessage(
            alt_text='狩獵大師之路',
            contents=flex_data.msg_data('green', string)
        )
    )
  
    line_bot_api.push_message(
        id,
        LocationSendMessage(
            title='藥草座標',
            address='herb',
            latitude=25.0445867,
            longitude=121.5600796
        )
    ) 
  
    line_bot_api.push_message(
        id,
        LocationSendMessage(
            title='獵靴座標',
            address='boots',
            latitude=25.0443998,
            longitude=121.5601470
        )
    ) 
  
  
def green_herb(id, line_bot_api, user_db):
    doc = user_db.get().to_dict()
    if doc['green']['progress'] == 5:
        user_db.update({'token':firestore.Increment(50)})
        string = '取得：藥草 (搜集任務完成度1/2)\n並獲得$50新能幣獎勵\n\n請繼續搜集獵靴。'
        line_bot_api.push_message(
            id,
            FlexSendMessage(
                alt_text='狩獵大師之路',
                contents=flex_data.msg_data('green', string)
            )
        )
    else:
        user_db.update({'token':firestore.Increment(50)})
        
        string = '取得：藥草 (搜集任務完成度2/2)\n並獲得$50新能幣獎勵。\n\n\n已取得獵人身份，接下來請「藍舞台 - 獵人酒吧」找到密碼，並在此輸入「密碼」解救聖鹿。' 
      #https://hubs.mozilla.com/tjRBa38/synergy-virtual-art-gallery?openexternalbrowser=1
        data = flex_data.msg_data('green', string)
        
        line_bot_api.push_message(
            id,
            FlexSendMessage(
                alt_text='狩獵大師之路',
                contents=data
            )
        )
      
def green_boots(id, line_bot_api, user_db):
    doc = user_db.get().to_dict()
    if doc['green']['progress'] == 5:
        user_db.update({'token':firestore.Increment(50)})
        string = '取得：獵靴 (搜集任務完成度1/2)\n並獲得$50新能幣獎勵\n\n請繼續搜集藥草。'
        line_bot_api.push_message(
            id,
            FlexSendMessage(
                alt_text='狩獵大師之路',
                contents=flex_data.msg_data('green', string)
            )
        )
    else:
        user_db.update({'token':firestore.Increment(50)})
        string = '取得：獵靴 (搜集任務完成度2/2)\n並獲得$50新能幣獎勵。\n\n\n已取得獵人身份，接下來請「藍舞台 - 獵人酒吧」找到密碼，並在此輸入「密碼」解救聖鹿。' 
        data = flex_data.msg_data('green', string)
        
        line_bot_api.push_message(
            id,
            FlexSendMessage(
                alt_text='狩獵大師之路',
                contents=data
            )
        )
      
  
def green_5(event, line_bot_api, user_db):
    doc = user_db.get().to_dict()
    if doc['green']['tools']['herb'] == 1:
        string = '您已取得：藥草 (搜集任務完成度1/2)\n請繼續搜集獵靴。'
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='狩獵大師之路',
                contents=flex_data.msg_data('green', string)
            )
        )
      
    else:
        string = '您已取得：獵靴 (搜集任務完成度1/2)\n請繼續搜集藥草。'
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='狩獵大師之路',
                contents=flex_data.msg_data('green', string)
            )
        )


def green_6(event,line_bot_api):
    string = '已取得獵人身份，接下來請「藍舞台 - 獵人酒吧」找到密碼，並在此輸入「密碼」解救聖鹿。' 
    data = flex_data.msg_data('green', string)
    
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='狩獵大師之路',
            contents=data
        )
    )

def green_7(event, line_bot_api, user_db):
    user_db.update({'green.progress':7,'token':firestore.Increment(150),'green.prize':1})     
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='狩獵大師之路',
            contents=flex_data.game_data('green','end','')
        )
    )
    