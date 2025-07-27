import requests
import git
import time
import os
import sys
from PyQt5.QtTest import *
import variable as v_

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')

def game_start():
    try:
        play_game = False
        # 먼저 서버 파일 등 있는지 파악 후 없다면 생성 후 실행

        dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
        file_path = dir_path + "\\start.txt"

        isstart1 = False
        while isstart1 is False:
            if os.path.isdir(dir_path) == True:
                if os.path.isfile(file_path) == True:
                    with open(file_path, "r", encoding='utf-8-sig') as file:
                        start_get = file.read()
                        isstart1 = True
                else:
                    with open(file_path, "w", encoding='utf-8-sig') as file:
                        data = 'none'
                        file.write(str(data))
            else:
                os.makedirs(dir_path)


        # 게임 클라 선택 및 실행시 yes로 바뀌고, 정지 할 경우에만 no로 바뀜. 자동업데이트는 안바뀜. 수동 업데이트는 no로 바뀜.
        if start_get == "yes":

            result_my_server_read = server_get()
            print("my_server_read", result_my_server_read)

            if result_my_server_read == 'start':
                print("게임 gogo")
                play_game = True
            elif result_my_server_read == 'update':

                file_path = "C:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\mymodule\\version.txt"
                with open(file_path, "r", encoding='utf-8-sig') as file:
                    my_version = file.read()

                server_version = server_get_version()
                print("my_version", my_version)
                print("server_version", server_version)

                if str(my_version) != str(server_version):
                    print("버젼 달라서 업데이트")
                    my_repo = git.Repo()
                    my_repo.remotes.origin.pull()
                    time.sleep(1)
                    # 자동 업뎃 후 재시작 부분
                    os.execl(sys.executable, sys.executable, *sys.argv)

                else:
                    print("버젼 같아서 대기...")
        else:
            if v_.notification_count % 300 == 0:
                print("대기중...실행버튼을 눌러 실행해주세요.")
            v_.notification_count += 1
        return play_game
    except Exception as e:
        print(e)
        return 0

def server_get():
    try:
        url = "https://raw.githubusercontent.com/rntkdgnl932/server/master/" + str(v_.game_folder) + ".txt"

        response = requests.get(url, headers={'Cache-Control': 'no-cache'})
        # response = requests.get(url, headers={'Cache-Control': 'no-cache'})
        data = response.text

        print("server_get", str(v_.game_folder), data)
        return data
    except Exception as e:
        print(e)
        return 0

def server_get_version():
    try:
        url = "https://raw.githubusercontent.com/rntkdgnl932/" + str(v_.game_folder) + "/master/" + str(v_.data_folder) + "/mymodule/version.txt"

        response = requests.get(url, headers={'Cache-Control': 'no-cache'})
        # response = requests.get(url, headers={'Cache-Control': 'no-cache'})
        data = response.text

        print("server_get_version", data)
        return data
    except Exception as e:
        print(e)
        return 0