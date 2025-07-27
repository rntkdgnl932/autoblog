import time

import requests
import json
# import os
import sys
import variable as v_
from PyQt5.QtTest import *
sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')

send_own = "none"
send_cla = "none"
send_num = "none"

def kakao_to_me():
    print("111")
    url = 'https://kauth.kakao.com/oauth/token'
    client_id = 'e485b4ece1dfd26d6d17793412696d2a'
    redirect_uri = 'https://example.com/oauth'
    code = 'KjR9_BCW-tR1rXj4a5jx60885TGptDmtjz3AzPywKiDaFLnczbAAt3HIUDh6FVHbVnlKWwoqJU8AAAGGr6BAhw'

    data = {
        'grant_type':'authorization_code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code': code,
        }

    response = requests.post(url, data=data)
    tokens = response.json()

    #발행된 토큰 저장
    with open("token.json", "w") as kakao:
        json.dump(tokens, kakao)
    print("222")
    # 발행한 토큰 불러오기
    with open("token.json", "r") as kakao:
        tokens = json.load(kakao)
    print("333")
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": "Bearer " + tokens["access_token"]
    }

    data = {
        "template_object": json.dumps({"object_type": "text",
                                       "text": "뿌엥.",
                                       "link": {
                                           "web_url": "www.naver.com"
                                       }
                                       })
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))
    print("444")

def kakao_to_friend():
    # step1
    print("step1")
    client_id = '0b2c35b13a3fc144a72e7b37c1bb1579'
    redirect_uri = 'https://example.com/oauth'
    # 계속 갱신
    code = 'At0bprktGuWW5f9S4CrEzqv_A_w2vWWB8U8vm7fK1edsSD2WR8Iedi6fP4NEGB5hInI38gorDNIAAAGGr9zEqw'

    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "redirect_url": redirect_uri,
        "code": code
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)

    # step2
    print("step2")
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": tokens["refresh_token"]
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    # kakao_code.json 파일 저장
    with open("kakao_code.json", "w") as fp:
        json.dump(tokens, fp)

    # step3
    print("step3")
    with open("kakao_code.json", "r") as fp:
        tokens = json.load(fp)
    print(tokens["access_token"])

    # step4
    print("step4")
    url = "https://kapi.kakao.com/v1/api/talk/friends"  # 친구 목록 가져오기
    header = {"Authorization": 'Bearer ' + tokens["access_token"]}
    result = json.loads(requests.get(url, headers=header).text)
    print("list", requests.get(url, headers=header).text)
    friends_list = result.get("elements")
    print(friends_list)

    #step5
    print("step5")
    friend_id = friends_list[0].get("uuid")
    print(friend_id)

    #step6
    print("step6")
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    header = {"Authorization": 'Bearer ' + tokens["access_token"]}
    data = {
        'receiver_uuids': '["{}"]'.format(friend_id),
        "template_object": json.dumps({
            "object_type": "text",
            "text": "딥러닝 뉴스",
            "link": {
                "web_url": "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws",
                "mobile_web_url": "https://www.google.co.kr/search?q=deep+learning&source=lnms&tbm=nws"
            },
            "button_title": "뉴스 보기"
        })
    }
    response = requests.post(url, headers=header, data=data)
    response.status_code

def line_to_me(cla, why):
    print("line")
    import requests
    import os.path
    global send_own, send_cla, send_num
    try:
        print("cla", cla)
        print("why", why)
        dir_path = "C:\\my_games"
        file_path = dir_path + "\\line\\line.txt"

        isLine = False
        while isLine is False:
            if os.path.isfile(file_path) == True:
                with open(file_path, "r", encoding='utf-8-sig') as file:
                    read_ = file.read()
                if read_ == "":
                    print("empty")
                    line_data = "ccocco:뿌에에에에에엥"
                    with open(file_path, "w", encoding='utf-8-sig') as file:
                        file.write(line_data)
                else:
                    isLine = True
                    print("read_", read_)
            else:
                line_data = "ccocco:메롱메롱"
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write(line_data)

        read_result = read_.split(":")

        if send_own == str(read_result[0]) and send_cla == cla and send_num == str(read_result[1]):
            print("이미 발송한 상태")
        else:
            send_own = read_result[0]
            send_cla = cla
            send_num = read_result[1]

            if read_result[0] == "coob":
                # 라인
                my_token = "qwERHZyXhOvohyX0ONQcA0rsCh2aEur1djCC7zEplhH"

                # 텔레그램으로 보내기
                token = '7718169047:AAGSr-Uej5frwoFZwlJptTpafZuk9_cJxiE'
                chat_id = '2133333624'

                #

            elif read_result[0] == "ccocco":
                # 라인
                my_token = "hKXb6oosWTnH2JCrhtnchbVV5WN5WN3G3yMtZF4UTos"

                # 텔레그램으로 보내기
                token = '7000893833:AAEEecQWjeWV43C14BrkRsQI_JKnxNSkrXc'
                chat_id = '2139978875'

            elif read_result[0] == "suko":

                # 텔레그램으로 보내기
                token = '7849921174:AAEhgcjNJcVyM7sewlxCOgV-edRakA3gl7k'
                chat_id = '5933492731'
                #
            tele_massage = "\n" + v_.this_game + "\n" + str(read_result[0]) + "님\n" + str(
                read_result[1]) + " 컴퓨터\n[" + str(cla) + "클라] 확인 요망\n=> " + str(why)
            # https://api.telegram.org/bot7718169047:AAGSr-Uej5frwoFZwlJptTpafZuk9_cJxiE/getUpdates

            send_message(token, chat_id, tele_massage)
            #
            # v_.this_game
            # message = "\n" + v_.this_game + "\n" + str(read_result[0]) + "님\n" + str(read_result[1]) + " 컴퓨터\n[" + str(cla) + "클라] 확인 요망\n=> " + str(why)
            # TARGET_URL = 'https://notify-api.line.me/api/notify'
            # TOKEN = my_token  # 발급받은 토큰
            # headers = {'Authorization': 'Bearer ' + TOKEN}
            # data = {'message': message}
            #
            # response = requests.post(TARGET_URL, headers=headers, data=data)

    except Exception as ex:
        print(ex)

def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=payload)
    return response

def line_monitor(game, cla):
    print("line_monitor")
    import numpy as np
    import os.path
    import cv2
    from function_game import imgs_set, click_pos_reg
    import time
    from datetime import datetime, timedelta, date
    from server import server_get
    try:
        isLoop = False

        # v_.global_howcla
        while isLoop is False:

            # x같은 팝업창

            result_my_server_read = server_get()
            print("my_server_read", result_my_server_read)

            if result_my_server_read == 'start':

                # 블랙 스크린
                nowTime = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                print(nowTime)
                full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\monitor\\unreal_error_1.png"
                img_array = np.fromfile(full_path, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                imgs_ = imgs_set(0, 700, 960, 850, "one", img)
                if imgs_ is not None and imgs_ != False:
                    ms_ = str(game) + str(" 블랙스크린")
                    line_to_me("one", ms_)
                    click_pos_reg(imgs_.x, imgs_.y, cla)

                full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\monitor\\closewithoutsending.PNG"
                img_array = np.fromfile(full_path, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                imgs_ = imgs_set(0, 700, 960, 850, "one", img)
                if imgs_ is not None and imgs_ != False:
                    ms_ = str(game) + str(" 블랙스크린")
                    line_to_me("one", ms_)
                    click_pos_reg(imgs_.x, imgs_.y, cla)

                full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\monitor\\unreal_error_2.png"
                img_array = np.fromfile(full_path, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                imgs_ = imgs_set(0, 700, 960, 850, "two", img)
                if imgs_ is not None and imgs_ != False:
                    ms_ = str(game) + str(" 블랙스크린")
                    line_to_me("two", ms_)
                    click_pos_reg(imgs_.x, imgs_.y, cla)

                full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\monitor\\sendandrestart.PNG"
                img_array = np.fromfile(full_path, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                imgs_ = imgs_set(0, 700, 960, 850, "two", img)
                if imgs_ is not None and imgs_ != False:
                    ms_ = str(game) + str(" 블랙스크린")
                    line_to_me("two", ms_)
                    click_pos_reg(imgs_.x, imgs_.y, cla)






                # 장시간
                jangsigan = False


                if jangsigan == True:
                    ms_ = str(game) + str(" 죽어뿌따 ㅠㅅㅠ")
                    line_to_me(cla, ms_)




                # 날짜 갱신 체크 관련
                print("날짜 갱신 체크")
                # 닉네임 받아와서 전역변수 설정하기
                nowDay_ = datetime.today().strftime("%Y%m%d")
                nowDay = int(nowDay_)
                nowTime = int(datetime.today().strftime("%H"))
                yesterday_ = date.today() - timedelta(1)
                yesterday = int(yesterday_.strftime('%Y%m%d'))

                dir_path = "C:\\my_games\\" + str(v_.game_folder)
                file_path2 = dir_path + "\\mysettings\\refresh_time\\quest.txt"
                file_path13 = dir_path + "\\mysettings\\refresh_time\\refresh_time.txt"

                isRefresh = False
                while isRefresh is False:
                    if os.path.isfile(file_path13) == True:
                        with open(file_path13, "r", encoding='utf-8-sig') as file:
                            isRefresh = True
                            refresh_time = file.read()
                            print("refresh_time", refresh_time)
                    else:
                        with open(file_path13, "w", encoding='utf-8-sig') as file:
                            file.write(str(6))

                isNowday = False
                while isNowday is False:
                    if os.path.isfile(file_path2) == True:
                        with open(file_path2, "r", encoding='utf-8-sig') as file:
                            isNowday = True
                            lines2 = file.read().splitlines()
                            day_ = lines2[0].split(":")
                            print("day_", day_)
                    else:
                        with open(file_path2, "w", encoding='utf-8-sig') as file:
                            file.write(str(nowDay) + ":" + str(refresh_time) + "\n")

                if nowTime >= int(refresh_time) + 1:
                    if int(day_[0]) != nowDay:
                        print("day_[0]", day_[0])
                        print("nowDay", nowDay)
                        ms_ = str(game) + str(" 초기화 갱신 안되었다.")
                        line_to_me(cla, ms_)

            time.sleep(300)

    except Exception as ex:
        print(ex)