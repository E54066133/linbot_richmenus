#coding=utf-8
import json
import time
import math
import Weather


#### 彙整資料 ####
def Consolidate(input, user_id, data_type):

    #### 建立user_data ####
    # template
    '''
        with open('./user_data.json') as f:
            j = json.load(f)

            user_dict = \                # 用戶資料格式
                {
                    user_id: {
                        "午餐時段": ,
                        "校區位置": ,
                        "移動方式": , // store walking_time, bicycling_time, driving_time
                        "價格": ,
                        "attributes": ,
                    }
                }

            j.update(user_dict)

        with open ('user_data.json','w') as f:
            json.dump(j,f)
    '''

    record = False
    with open('./user_data.json', 'r', encoding='utf-8') as f:
        j = json.load(f)
        if user_id in j:
            record = True

        if not record:                  # 若為新用戶，註冊新usre_id
            user_dict = \
                {
                    user_id: {
                        data_type: input
                    }
                }
            j.update(user_dict)
        else:                           # 更新用戶內的資料
            new_dict = \
                {
                    data_type: input
                }
            j[user_id].update(new_dict)
            temp_dict = \
                {
                    user_id: j[user_id]
                }
            del j[user_id]
            j.update(temp_dict)

    with open('./user_data.json', 'w', encoding='utf-8') as f:
        json.dump(j, f, ensure_ascii=False)

    return input


#### 演算推薦名單 ####
def algorithm(input, user_id):

    if input != "開始搜尋":       # 接收linebot"開始搜尋"按鈕
        return "指令錯誤!"

    #### to check if stores meet user's needs ####
    user_need = {}
    with open('./user_data.json', 'r', encoding='utf-8') as f:
        user_j = json.load(f)
        for users in user_j:
            if users == user_id:
                for needs in user_j[users]:
                    user_need[needs] = user_j[users][needs]

    with open('./final_0613.json', 'r', encoding='utf-8') as f:      # final_0613.json為 2021/06/13 爬蟲抓到的店家資料
        rest_j = json.load(f)
        temp_dict = rest_j

    if "attributes" not in user_need or "price" not in user_need or "drinks" not in user_need or "aircon" not in user_need \
            or "campus" not in user_need or "Transportation" not in user_need or "time" not in user_need:
        return "finish setting, plz!"        # 確認用戶必填資料是否完整

    food_type = user_need["attributes"]
    user_air = user_need["aircon"]
    user_drink = user_need["drinks"]
    if user_need["price"] == "0":            # 確認價格條件
        accept_price = 0
    else:
        accept_price = len(user_need["price"])
    for rest in list(temp_dict.keys()):
        flag = False
        for tags in temp_dict[rest]["food_type"]:     # 確認食物類型條件
            if tags == food_type:
                flag = True
                break
        if not flag:
            del temp_dict[rest]
            continue

        if len(temp_dict[rest]["price"]) > accept_price or temp_dict[rest]["price"] == "NA":
            del temp_dict[rest]
            continue

        if user_drink == "飲料" and temp_dict[rest]["drinks"] == "None":    # 確認飲料條件
            del temp_dict[rest]
            continue

        if user_air == "冷氣" and temp_dict[rest]["aircon"] == "None":      # 確認空調條件
            del temp_dict[rest]


    # check if the store is reachable
    now = time.time()
    result = time.localtime(now)  # 抓目前時間
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    search_day = weekdays[result.tm_wday]
    user_loc = user_need["campus"]             # 抓用戶地點(校園)資料
    user_mov = user_need["Transportation"]     # 抓用戶交通方式資料
    for rest in list(temp_dict.keys()):

        # delete those stores are not open
        if temp_dict[rest]["Time"][search_day] == "休息" or temp_dict[rest]["Time"][search_day] == "NA":
            del temp_dict[rest]
        elif temp_dict[rest][user_mov][user_loc][2:4] == "小時" or temp_dict[rest][user_mov][user_loc][3:5] == "小時" or temp_dict[rest][user_mov][user_loc][2] == "天":
            del temp_dict[rest]
        elif temp_dict[rest]["Time"][search_day] == "24 小時營業":
            continue

        # stores open, delete stores are not reachable   # 根據不同的交通方式計算到店時間，若超過用戶可接受時間就不推薦該間店
        else:
            setting_time = int(user_need["time"]) * 60
            if setting_time > int(temp_dict[rest][user_mov][user_loc][0:-3]) + 60 * int(result.tm_hour) + int(result.tm_min):
                arrive_time = setting_time
            else:
                arrive_time = int(temp_dict[rest][user_mov][user_loc][0:-3]) + 60 * int(result.tm_hour) + int(result.tm_min)
            closed_time = int(temp_dict[rest]["Time"][search_day][6:8]) * 60 + int(temp_dict[rest]["Time"][search_day][9:11])
            if arrive_time > closed_time:
                del temp_dict[rest]

    #### recommend restaurant ####
    rest_score_dict = {}
    env_condition = Weather.get_weather()         # 抓當天天氣資訊(網路爬蟲)
    temp = float(env_condition["temp"])
    rain = float(env_condition["rain"][0:-1])
    for rest in list(temp_dict.keys()):

        rating = float(temp_dict[rest]["rating"])
        temp_dict[rest]["reviews_count"] = temp_dict[rest]["reviews_count"].replace(",", "")    # 店家資料切割
        number_of_reviews = int(temp_dict[rest]["reviews_count"][0:-4])                         # 計算 Google Maps 評論數目
        distance = int(temp_dict[rest][user_mov][user_loc][0:-3])                               # 計算用戶與店家之間的道路距離
        if not temp_dict[rest]["Popular Times"][search_day] or temp_dict[rest]["Popular Times"][search_day][0] == ' 時的繁忙程度通常為 %。'\   #抓 Google Maps 店家繁忙與否
                or temp_dict[rest]["Popular Times"][search_day][int(user_need["time"]) - 6][14:-2] == '':
            busy = 0
        else:
            busy = int(temp_dict[rest]["Popular Times"][search_day][int(user_need["time"]) - 6][14:-2])

        review_point = math.log(number_of_reviews, 10)
        distance_point = 100 - (distance / 5) * 20
        if busy > 90:
            busy_point = 0
        elif busy > 80:
            busy_point = 25
        elif busy > 70:
            busy_point = 50
        elif busy > 60:
            busy_point = 75
        else:
            busy_point = 100

        # check the weather. if it is too hot or it rains heavily, make the weight of distance higher

        if temp < 30 and rain < 70:
            recommend_score = rating * 10 + 2 * review_point + 0.2 * distance_point + 0.2 * busy_point    # 計算推薦分數(晴天)
        else:
            recommend_score = rating * 9 + review_point + 0.35 * distance_point + 0.25 * busy_point       # 計算推薦分數(雨天)

        rest_score_dict[rest] = recommend_score    

    sorted_score_list = sorted(rest_score_dict.items(), key=lambda x: x[1], reverse=True)                 # sort 推薦分數list
    print(sorted_score_list)
    sorted_score_dict = {}
    count = 0
    for rest in sorted_score_list:
        if count >= 10:             # 只推薦最高分的十間
            break
        new_dict = \
            {
                rest[0]: {
                    "location": temp_dict[rest[0]]["location"],
                    "contact": temp_dict[rest[0]]["contact"],
                    "food_type": temp_dict[rest[0]]["food_type"],
                    "google_site": temp_dict[rest[0]]["google_site"]
                }
            }
        sorted_score_dict.update(new_dict)
        # sorted_score_dict[rest[0]] = temp_dict[rest[0]]
        count += 1
    print(sorted_score_dict)

    return sorted_score_dict


def write_prev_action(user_id, prev_action):                           # 建立用戶清單

    with open('./prev_action.json', 'r', encoding='utf-8') as f:
        j = json.load(f)
        prev_action_dict = \
            {
                user_id: prev_action
            }
        j.update(prev_action_dict)

    with open('./prev_action.json', 'w', encoding='utf-8') as f:
        json.dump(j, f, ensure_ascii=False)

    return


def get_prev_action(user_id):

    with open('./prev_action.json', 'r', encoding='utf-8') as f:
        j = json.load(f)
        prev_action = j[user_id]

    return prev_action


def RepresentInt(s):

    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    user_id = "E54062058"    # 測試
    algorithm('開始搜尋', user_id)
    write_prev_action(user_id, "set aircon")
    write_prev_action(user_id, 'set drink')
    print(get_prev_action(user_id))
    print(RepresentInt('b1'))
