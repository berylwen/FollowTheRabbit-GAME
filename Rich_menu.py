import requests
import json
import os



token = os.environ["CHANNEL_ACCESS_TOKEN"]

Authorization_token = "Bearer " + token

headers = {"Authorization":Authorization_token, "Content-Type":"application/json"}
'''
body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "false",
    "name": "選單",
    "chatBarText": "SYNERGY",
    "areas":[
        {
          "bounds": {"x":50, "y": 50, "width": 1150, "height": 743},
          "action": {"type": "message", "text": "SYNERGY節目表"}
        },
        {
          "bounds": {"x": 1300, "y": 50, "width": 1150, "height": 743},
          "action": {"type": "message", "text": "現場地圖"}
        },
        {
          "bounds": {"x": 50, "y": 893, "width": 733, "height": 743},
          "action": {"type": "message", "text": "開啟任務"}
        },
        {
          "bounds": {"x": 883, "y": 893, "width": 733, "height": 743},
          "action": {"type": "message", "text": "遊戲現況"}
        },
        {
          "bounds": {"x": 1716, "y": 893, "width": 733, "height": 743},
          "action": {"type": "message", "text": "交易購買"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)
'''
#------------

from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi(token)
#line_bot_api.delete_rich_menu('richmenu-7b1ce22e54afbdd966670a9fb999c0e3')


rich_menu_id = "richmenu-67428aa9f8cff4f11ec47e75e0ec0294" # 設定成我們的 Rich Menu ID
'''
path = "./Menu.jpg" # 主選單的照片路徑

with open(path, 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)

'''
#------------


req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+rich_menu_id,
       headers=headers)
print(req.text)

rich_menu_list = line_bot_api.get_rich_menu_list()

