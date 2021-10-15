#coding=utf-8
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, PostbackEvent,
                            PostbackAction, ConfirmTemplate, TemplateSendMessage, CarouselTemplate,
                            CarouselColumn, URIAction)

import configparser
import Algorithm as alg
import json
import requests
import re

import modules


app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel-access-token'))
handler = WebhookHandler(config.get('line-bot', 'channel-secret'))

drink_confirm = ConfirmTemplate(text="飲料是必要條件嗎？", actions=[
        PostbackAction(label="Yes", data="飲料"),
        PostbackAction(label="No", data="None")
    ])
drink_confirm_template = TemplateSendMessage(alt_text="confirm alt text", template=drink_confirm)

aircon_confirm = ConfirmTemplate(text="冷氣是必要條件嗎？", actions=[
        PostbackAction(label="Yes", data="冷氣"),
        PostbackAction(label="No", data="不冷氣")
    ])
aircon_confirm_template = TemplateSendMessage(alt_text="confirm alt text", template=aircon_confirm)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    
    ##用 postman 實作 rich menu 的圖文選單
    ##用 圖文選單 點選的方式 請使用者輸入校區、移動方式、價位、其他attributes
    ##參考網址  https://www.letswrite.tw/line-bot-rich-menu/
    ##參考網址  https://www.postman.com/




    ##[法二] line developers 的選單功能 
    ##(缺點是 至多只有六個按鈕可以點，且不能客製化)
    #### 處理圖文選單提示 ####
    if text.find('測試') == 0:
        response = alg.algorithm(event.message.text, event.source.user_id)
        print(event.message.text)
    elif text.find('help') == 0 or text.find('Help') == 0 or text.find('HELP') == 0:
        response = '我們會根據您輸入的\n午餐時段\n校區位置\n移動方式\n價格\n其他attributes\n來為您推薦出適合的餐廳!!'
    elif text.find('午餐時段') == 0:
        response = '請輸入午餐時段\n11 12 13 14'
        print(event.message.text)
    elif text.find('校區位置') == 0:
        response = '請輸入所在校區位置\n 光復 成功 自強 勝利 力行 成杏 敬業 東寧 '
        print(event.message.text)
    elif text.find('移動方式') == 0:
        response = '請輸入移動方式\n走路 腳踏車 機車'
        print(event.message.text)
    elif text.find('價格') == 0:
        response = '請輸入可接受價格'
        print(event.message.text)
    elif text.find('attributes') == 0:
        response = '請輸入attributes\n食物類型 冷氣 飲料\n(類型有 義式 中港 健康 披薩 小吃 日韓 東南亞 異國 素食 美式 便當 咖哩 滷味 火鍋 炸機 粥湯 鐵板燒 餃子 麵 飯 歐式 漢堡)'
        print(event.message.text)


    #### 處理實際輸入 ####
    #### 處理午餐時段 ####  
    elif text.find('11') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'time')
    elif text.find('12') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'time')
    elif text.find('13') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'time')
    elif text.find('14') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'time')
    #### 處理校區位置 ####
    elif text.find('成功') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'campus')
    elif text.find('光復') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'campus')
    elif text.find('東寧') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'campus')
    elif text.find('自強') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'campus')
    elif text.find('勝利') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'campus')
    elif text.find('力行') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'campus')
    elif text.find('敬業') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'campus')
    elif text.find('成杏') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'campus')
    elif text.find('walking_time') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'Transportation')
    elif text.find('腳踏車') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'Transportation')
    elif text.find('機車') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'Transportation')
    #### 處理價格 #### 
    elif text.find('$') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'price')
    elif re.match('[\d]+',text):
        price = float(re.match('[\d]+',text).group())
        if price != 11 and price != 12 and price != 13 and price != 14:
            response = alg.Consolidate(event.message.text, event.source.user_id, 'price')
    #### 處理attributes ####
    elif text.find('冷氣') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'aircon')
    elif text.find('飲料') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'drinks')
    elif text.find('義式') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('東南亞') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('異國') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('素食') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('便當') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('美式') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('日韓') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('披薩') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('小吃') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('健康') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('中港') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('滷味') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('鐵板燒') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('粥湯') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('餃子') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('炸雞') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('火鍋') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('咖哩') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('飯') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('麵') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('歐式') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    elif text.find('漢堡') == 0:
        response = alg.Consolidate(event.message.text, event.source.user_id, 'attributes')
    else:
        response = '格式錯誤!'

    #### 處理搜尋 ####
    if text.find('開始搜尋') == 0 or text.find('搜尋') == 0 :
        response = alg.algorithm(event.message.text, event.source.user_id)

    # 回覆文字訊息
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))


@handler.add(PostbackEvent)
def handle_postback(event):
    # confirm message
    if event.postback.data == "不冷氣":
        alg.Consolidate("None", event.source.user_id, "aircon")
        response = "不需要冷氣"
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), drink_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "冷氣":
        alg.Consolidate(event.postback.data, event.source.user_id, "aircon")
        response = "需要冷氣"
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), drink_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "None":
        alg.Consolidate(event.postback.data, event.source.user_id, "drinks")
        response_req = "不需要飲料"
        if alg.get_prev_action(event.source.user_id) == "set all":
            response = "設定完成，按go開始推薦!"
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response_req), TextSendMessage(response)])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response_req))
    elif event.postback.data == "飲料":
        alg.Consolidate(event.postback.data, event.source.user_id, "drinks")
        response_req = "需要飲料"
        if alg.get_prev_action(event.source.user_id) == "set all":
            response = "設定完成，按go開始推薦!"
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response_req), TextSendMessage(response)])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response_req))

    # quick reply
    elif event.postback.data == "日韓":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "健康":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "咖哩":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "火鍋":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "餃子":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "小吃":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "鐵板燒":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "義式":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "東南亞":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "素食":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "便當":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "美式":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
    elif event.postback.data == "滷味":
        alg.Consolidate(event.postback.data, event.source.user_id, "attributes")
        response = event.postback.data
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(response), aircon_confirm_template])
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))

    # campus rich menu
    elif event.postback.data == "成功":
        alg.Consolidate(event.postback.data, event.source.user_id, "campus")
        response = "位置設定在成功校區!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-3c1b3afe40ccbe813d25802fed539e70")  # transportation
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "光復":
        alg.Consolidate(event.postback.data, event.source.user_id, "campus")
        response = "位置設定在光復校區!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-3c1b3afe40ccbe813d25802fed539e70")  # transportation
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "敬業":
        alg.Consolidate(event.postback.data, event.source.user_id, "campus")
        response = "位置設定在敬業校區!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-3c1b3afe40ccbe813d25802fed539e70")  # transportation
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "自強":
        alg.Consolidate(event.postback.data, event.source.user_id, "campus")
        response = "位置設定在自強校區!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-3c1b3afe40ccbe813d25802fed539e70")  # transportation
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "勝利":
        alg.Consolidate(event.postback.data, event.source.user_id, "campus")
        response = "位置設定在勝利校區!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-3c1b3afe40ccbe813d25802fed539e70")  # transportation
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "東寧":
        alg.Consolidate(event.postback.data, event.source.user_id, "campus")
        response = "位置設定在東寧校區!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-3c1b3afe40ccbe813d25802fed539e70")  # transportation
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "成杏":
        alg.Consolidate(event.postback.data, event.source.user_id, "campus")
        response = "位置設定在成杏校區!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-3c1b3afe40ccbe813d25802fed539e70")  # transportation
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "力行":
        alg.Consolidate(event.postback.data, event.source.user_id, "campus")
        response = "位置設定在力行校區!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-3c1b3afe40ccbe813d25802fed539e70")  # transportation
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)

    # transportation rich menu
    elif event.postback.data == "walking_time":
        alg.Consolidate(event.postback.data, event.source.user_id, "Transportation")
        response = "walking"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-fc9790d433049085d88283cfbd17c745")  # price
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "bicycling_time":
        alg.Consolidate(event.postback.data, event.source.user_id, "Transportation")
        response = "bicycling"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-fc9790d433049085d88283cfbd17c745")  # price
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "driving_time":
        alg.Consolidate(event.postback.data, event.source.user_id, "Transportation")
        response = "driving"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-fc9790d433049085d88283cfbd17c745")  # price
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)

    # time rich menu
    elif event.postback.data == "11":
        alg.Consolidate(event.postback.data, event.source.user_id, "time")
        response = "時間設定成11點到店!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-1a0ad6f37047374b1af6552451f22c49")  # campus
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "12":
        alg.Consolidate(event.postback.data, event.source.user_id, "time")
        response = "時間設定成12點到店!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-1a0ad6f37047374b1af6552451f22c49")  # campus
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "13":
        alg.Consolidate(event.postback.data, event.source.user_id, "time")
        response = "時間設定成13點到店!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-1a0ad6f37047374b1af6552451f22c49")  # campus
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    elif event.postback.data == "14":
        alg.Consolidate(event.postback.data, event.source.user_id, "time")
        response = "時間設定成14點到店!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-1a0ad6f37047374b1af6552451f22c49")  # campus
        else:
            line_bot_api.unlink_rich_menu_from_user(event.source.user_id)

    # price rich menu
    elif event.postback.data == "0":
        alg.Consolidate(event.postback.data, event.source.user_id, "price")
        line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text="reply food type", quick_reply=modules.food_type_reply))
    elif event.postback.data == "$":
        alg.Consolidate(event.postback.data, event.source.user_id, "price")
        line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text="reply food type", quick_reply=modules.food_type_reply))
    elif event.postback.data == "$$":
        alg.Consolidate(event.postback.data, event.source.user_id, "price")
        line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text="reply food type", quick_reply=modules.food_type_reply))
    elif event.postback.data == "$$$":
        alg.Consolidate(event.postback.data, event.source.user_id, "price")
        line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
        if alg.get_prev_action(event.source.user_id) == "set all":
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text="reply food type", quick_reply=modules.food_type_reply))

    # control rich menu
    elif event.postback.data == "set all":
        alg.write_prev_action(event.source.user_id, event.postback.data)
        line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-78dc1a5a3e1f3252dc5a495086f21b06")  # time
    elif event.postback.data == "set time":
        alg.write_prev_action(event.source.user_id, event.postback.data)
        line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-78dc1a5a3e1f3252dc5a495086f21b06")  # time
    elif event.postback.data == "set campus":
        alg.write_prev_action(event.source.user_id, event.postback.data)
        line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-1a0ad6f37047374b1af6552451f22c49")  # campus
    elif event.postback.data == "set transportation":
        alg.write_prev_action(event.source.user_id, event.postback.data)
        line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-3c1b3afe40ccbe813d25802fed539e70")  # transportation
    elif event.postback.data == "set price":
        alg.write_prev_action(event.source.user_id, event.postback.data)
        line_bot_api.link_rich_menu_to_user(event.source.user_id, "richmenu-fc9790d433049085d88283cfbd17c745")  # price
    elif event.postback.data == "set food":
        alg.write_prev_action(event.source.user_id, event.postback.data)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="reply food type", quick_reply=modules.food_type_reply))
    elif event.postback.data == "set aircon":
        alg.write_prev_action(event.source.user_id, event.postback.data)
        line_bot_api.reply_message(event.reply_token, aircon_confirm_template)
    elif event.postback.data == "set drink":
        alg.write_prev_action(event.source.user_id, event.postback.data)
        line_bot_api.reply_message(event.reply_token, drink_confirm_template)
    elif event.postback.data == "go":
        recommend_dict = alg.algorithm("開始搜尋", event.source.user_id)
        if str(type(recommend_dict)) == "<class 'str'>":
            response = recommend_dict
            line_bot_api.reply_message(event.reply_token, TextSendMessage(response))
        else:
            if len(recommend_dict) > 0:
                columns = []
                for rest in list(recommend_dict.keys()):
                    if len(rest) > 40:
                        name = rest[0:40]
                    else:
                        name = rest
                    tags = ""
                    for tag in recommend_dict[rest]["food_type"]:
                        tags += tag + " "
                    if alg.RepresentInt(recommend_dict[rest]["location"][0:3]):
                        column = CarouselColumn(
                            title=name,
                            text=tags,
                            actions=[
                                PostbackAction(
                                    label="contact",
                                    data=recommend_dict[rest]["contact"]
                                ),
                                URIAction(
                                    label="location",
                                    uri='https://www.google.com/maps/place/' + recommend_dict[rest]["location"]
                                )
                            ]
                        )
                    else:
                        column = CarouselColumn(
                            title=name,
                            text=tags,
                            actions=[
                                PostbackAction(
                                    label="contact",
                                    data=recommend_dict[rest]["contact"]
                                ),
                                PostbackAction(
                                    label="location",
                                    data=recommend_dict[rest]["google_site"]
                                )
                            ]
                        )
                    columns.append(column)
                response = TemplateSendMessage(
                    alt_text="result",
                    template=CarouselTemplate(columns)
                )
                line_bot_api.reply_message(event.reply_token, response)

            else:
                response = "sorry, the request is harder than solving an NP-complete problem"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
            alg.write_prev_action(event.source.user_id, event.postback.data)
    else:
        response = event.postback.data
        response = response.replace(" ", "")
        if response == "NA":
            response = "sorry, we have no data!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(response))


'''
#無法取得 userid
#push message to one user
line_bot_api.push_message('user_id', TextSendMessage(text='Hello World!'))
#push message to multiple users
line_bot_api.multicast(['user_id1', 'user_id2'], TextSendMessage(text='Hello World!'))
'''


if __name__ == "__main__":
    '''rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich in rich_menu_list:
        line_bot_api.delete_rich_menu(rich.rich_menu_id)'''
    
    rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list:
        print(rich_menu.rich_menu_id)
    app.run(debug=True)
    

