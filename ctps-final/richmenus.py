from linebot import LineBotApi
import configparser
import json

from linebot.models import (RichMenu, RichMenuArea, RichMenuSize,
                            RichMenuBounds, PostbackAction)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel-access-token'))

control_rich_menu = RichMenu(
    size=RichMenuSize(width=2500, height=1686),
    selected=True,
    name="control all setting",
    chat_bar_text="Tap here",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=625, height=700),
        action=PostbackAction(label="start setting", data="set all")),
        RichMenuArea(
        bounds=RichMenuBounds(x=625, y=0, width=625, height=700),
        action=PostbackAction(label="time setting", data="set time")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1250, y=0, width=625, height=700),
        action=PostbackAction(label="campus setting", data="set campus")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1875, y=0, width=625, height=700),
        action=PostbackAction(label="transport setting", data="set transportation")),
        RichMenuArea(
        bounds=RichMenuBounds(x=0, y=700, width=625, height=700),
        action=PostbackAction(label="price setting", data="set price")),
        RichMenuArea(
        bounds=RichMenuBounds(x=625, y=700, width=625, height=700),
        action=PostbackAction(label="food setting", data="set food")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1250, y=700, width=625, height=700),
        action=PostbackAction(label="aircon setting", data="set aircon")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1875, y=700, width=625, height=700),
        action=PostbackAction(label="drink setting", data="set drink")),
        RichMenuArea(
        bounds=RichMenuBounds(x=0, y=1400, width=2500, height=286),
        action=PostbackAction(label="start search", data="go"))]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=control_rich_menu)
with open('./richmenu-template-guide-01_2.jpeg', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
print(rich_menu_id)
with open('./richmenus.json', 'r', encoding='utf-8') as f:
    j = json.load(f)
    rich_menu_dict = \
        {
            'control_rich_menu': rich_menu_id
        }
    j.update(rich_menu_dict)
with open('./richmenus.json', 'w', encoding='utf-8') as f:
    json.dump(j, f)
line_bot_api.set_default_rich_menu(rich_menu_id)


campus_rich_menu = RichMenu(
    size=RichMenuSize(width=2500, height=1686),
    selected=False,
    name="campus selecting",
    chat_bar_text="Tap here",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=843, width=625, height=843),
        action=PostbackAction(label="成功", data="成功")),
        RichMenuArea(
        bounds=RichMenuBounds(x=625, y=843, width=625, height=843),
        action=PostbackAction(label="光復", data="光復")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1250, y=843, width=625, height=843),
        action=PostbackAction(label="東寧", data="東寧")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1875, y=843, width=625, height=843),
        action=PostbackAction(label="自強", data="自強")),
        RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=625, height=843),
        action=PostbackAction(label="力行", data="力行")),
        RichMenuArea(
        bounds=RichMenuBounds(x=625, y=0, width=625, height=843),
        action=PostbackAction(label="勝利", data="勝利")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1250, y=0, width=625, height=843),
        action=PostbackAction(label="敬業", data="敬業")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1875, y=0, width=625, height=843),
        action=PostbackAction(label="成杏", data="成杏"))]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=campus_rich_menu)
with open('./richmenu-template-guide-02_2.jpeg', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
print(rich_menu_id)
with open('./richmenus.json', 'r', encoding='utf-8') as f:
    j = json.load(f)
    rich_menu_dict = \
        {
            'campus_rich_menu': rich_menu_id
        }
    j.update(rich_menu_dict)
with open('./richmenus.json', 'w', encoding='utf-8') as f:
    json.dump(j, f)

time_rich_menu = RichMenu(
    size=RichMenuSize(width=2500, height=843),
    selected=False,
    name="time selecting",
    chat_bar_text="Tap here",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=625, height=843),
        action=PostbackAction(label="11", data="11")),
        RichMenuArea(
        bounds=RichMenuBounds(x=625, y=0, width=625, height=843),
        action=PostbackAction(label="12", data="12")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1250, y=0, width=625, height=843),
        action=PostbackAction(label="13", data="13")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1875, y=0, width=625, height=843),
        action=PostbackAction(label="14", data="14"))]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=time_rich_menu)
with open('./richmenu-compact-template-guide-01.jpeg', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
print(rich_menu_id)
with open('./richmenus.json', 'r', encoding='utf-8') as f:
    j = json.load(f)
    rich_menu_dict = \
        {
            'time_rich_menu': rich_menu_id
        }
    j.update(rich_menu_dict)
with open('./richmenus.json', 'w', encoding='utf-8') as f:
    json.dump(j, f)

price_rich_menu = RichMenu(
    size=RichMenuSize(width=2500, height=843),
    selected=False,
    name="price selecting",
    chat_bar_text="Tap here",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=625, height=843),
        action=PostbackAction(label="0", data="0")),
        RichMenuArea(
        bounds=RichMenuBounds(x=625, y=0, width=625, height=843),
        action=PostbackAction(label="$", data="$")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1250, y=0, width=625, height=843),
        action=PostbackAction(label="$$", data="$$")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1875, y=0, width=625, height=843),
        action=PostbackAction(label="$$$", data="$$$"))]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=price_rich_menu)
with open('./richmenu-compact-template-guide-02.jpeg', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
print(rich_menu_id)
with open('./richmenus.json', 'r', encoding='utf-8') as f:
    j = json.load(f)
    rich_menu_dict = \
        {
            'price_rich_menu': rich_menu_id
        }
    j.update(rich_menu_dict)
with open('./richmenus.json', 'w', encoding='utf-8') as f:
    json.dump(j, f)


transportation_rich_menu = RichMenu(
    size=RichMenuSize(width=2500, height=843),
    selected=False,
    name="transportation selecting",
    chat_bar_text="Tap here",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
        action=PostbackAction(label="walk", data="walking_time")),
        RichMenuArea(
        bounds=RichMenuBounds(x=833, y=0, width=834, height=843),
        action=PostbackAction(label="bicycle", data="bicycling_time")),
        RichMenuArea(
        bounds=RichMenuBounds(x=1667, y=0, width=833, height=843),
        action=PostbackAction(label="drive", data="driving_time"))]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=transportation_rich_menu)
with open('./richmenu-compact-template-guide-03.jpeg', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
print(rich_menu_id)
with open('./richmenus.json', 'r', encoding='utf-8') as f:
    j = json.load(f)
    rich_menu_dict = \
        {
            'transportation_rich_menu': rich_menu_id
        }
    j.update(rich_menu_dict)
with open('./richmenus.json', 'w', encoding='utf-8') as f:
    json.dump(j, f)