# * QTabWidget 탭에 다양한 위젯 추가
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QColor       #아이콘
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtTest import *

import sys

import variable as v_

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')
import os
import time
from datetime import datetime
import random
import os.path
from datetime import date, timedelta
import re
import git
from screeninfo import get_monitors

import cv2
# print(cv2.__version__)
# import matplotlib.pyplot as plt
from PIL import Image

import numpy
# 패키지 다운 필요
import pytesseract
# from pytesseract import image_to_string #
import pyautogui
import pydirectinput
import clipboard
# import keyboard
# 패키지 다운 불필요
import tkinter
import webbrowser
import colorthief

# 나의 모듈
# from function import imgs_set, imgs_set_, click_pos_2, random_int, text_check_get_3, int_put_, text_check_get, \
#     click_with_image, drag_pos, image_processing, get_region, click_pos_reg
from function_game import imgs_set, imgs_set_, click_pos_2, random_int, text_check_get_3, int_put_, text_check_get, click_with_image, drag_pos, image_processing, get_region, click_pos_reg, win_left_move, win_right_move


from massenger import line_monitor, line_to_me
from schedule import myQuest_play_check, myQuest_play_add
from life_tips import suggest_life_tip_topic

from stop_event18 import _stop_please

from test_ import go_test


from server import game_start
import variable as v_

sys.setrecursionlimit(10 ** 7)
# pyqt5 관련###################################################
rowcount = 0
colcount = 0
thisRow = 0
thisCol = 0
thisValue = "none"
table_datas = ""
#  onCollection= False
onCla = 'none'
onCharacter = 0
onRefresh_time = 0
onDunjeon_1 = "none"
onDunjeon_1_level = 0
onDunjeon_2 = "none"
onDunjeon_2_level = 0
onDunjeon_3 = "none"
onDunjeon_3_level = 0
onDunjeon_3_step = 0

onHunt = "none"
onHunt2 = "none"
onHunt3 = "none"
onHunt4 = "none"
onMaul = "none"

one_id = "none"
one_pw = "none"
two_id = "none"
two_pw = "none"

version = v_.version_

# 기존 오토모드 관련##############################################


pyautogui.FAILSAFE = False
####################################################################################################################
# pytesseract.pytesseract.tesseract_cmd = R'E:\workspace\pythonProject\Tesseract-OCR\tesseract'
pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract'


####################################################################################################################
####################################################################################################################
####################################################################################################################
#######pyqt5 관련####################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################


class MyApp(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)

        self.initUI()

    def initUI(self):
        tabs = QTabWidget()
        tabs.addTab(FirstTab(), '스케쥴')
        tabs.addTab(SecondTab(), '내 정보')
        tabs.addTab(ThirdTab(), '현재 컴퓨터 및 마우스 설정')

        # buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # buttonbox.accepted.connect(self.accept)
        # buttonbox.rejected.connect(self.reject)

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        # vbox.addWidget(buttonbox)

        self.setLayout(vbox)
        #
        # start_ready = game_Playing_Ready(self)
        # start_ready.start()

        self.my_title()

        # 풀버젼
        # git config --global --add safe.directory C:/my_games/mbng
        # auto_blog
        # data_basic
        # pyinstaller --hidden-import PyQt5 --hidden-import pyserial --hidden-import OpenAI --hidden-import feedparser --hidden-import requests --hidden-import chardet --add-data="C:\\my_games\\auto_blog\\data_basic;./data_basic" --add-data="C:\\my_games\\auto_blog\\mysettings;./mysettings" --name auto_blog -i="auto_blog.ico" --add-data="auto_blog.ico;./" --icon="auto_blog.ico" --paths "C:\my_games\auto_blog\.venv\Scripts\python.exe" main.py
        # 업데이트버젼
        # pyinstaller --hidden-import PyQt5 --hidden-import pyserial --hidden-import requests --hidden-import chardet --add-data="C:\\my_games\\game_folder\\data_game;./data_game" --name game_folder -i="game_folder_macro.ico" --add-data="game_folder_macro.ico;./" --icon="game_folder_macro.ico" --paths "C:\Users\1_S_3\AppData\Local\Programs\Python\Python311\Lib\site-packages\cv2" main.py

        dir_path = "C:\\my_games"
        file_path = dir_path + "\\line\\line.txt"

        if os.path.isdir(dir_path) == False:
            os.makedirs(dir_path)
        isFile = False
        while isFile is False:
            if os.path.isfile(file_path) == True:
                isFile = True
                # 파일 읽기
                with open(file_path, "r", encoding='utf-8-sig') as file:
                    line = file.read()
                    line_ = line.split(":")
                    print('line', line)
            else:
                print('line 파일 없당')
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write("ccocco:메롱")

        if line_[0] == "coob":
            x_reg = 960 * 2

        monitors = get_monitors()
        last_monitor_number = 0
        for idx, monitor in enumerate(monitors, start=1):
            last_monitor_number = idx

        if last_monitor_number == 1:
            x_reg = 0
        elif last_monitor_number == 2:
            x_reg = 960 * 2
        elif last_monitor_number == 3:
            x_reg = 960 * 4

        self.setGeometry(20, 200, 900, 700)
        self.show()
    def my_title(self):
        self.setWindowTitle(v_.this_game + "(ver " + version + ")")

class ThirdTab(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        # self.set_rand_int()

    def initUI(self):

        dir_path = "C:\\my_games"
        file_path = dir_path + "\\line\\line.txt"

        if os.path.isdir(dir_path) == False:
            os.makedirs(dir_path)
        isFile = False
        while isFile is False:
            if os.path.isfile(file_path) == True:
                isFile = True
                # 파일 읽기
                with open(file_path, "r", encoding='utf-8-sig') as file:
                    line = file.read()
                    line_ = line.split(":")
                    print('line', line)
            else:
                print('line 파일 없당')
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write("ccocco:메롱")

        file_path2 = dir_path + "\\mouse\\arduino.txt"

        isFile = False
        while isFile is False:
            if os.path.isfile(file_path2) == True:
                isFile = True
                # 파일 읽기
                with open(file_path2, "r", encoding='utf-8-sig') as file:
                    line2 = file.read()
                    v_.now_arduino = line2
                    print('line2', line2)
            else:
                print('line2 파일 없당')
                with open(file_path2, "w", encoding='utf-8-sig') as file:
                    file.write("on")

        dir_path2 = dir_path + "\\" + str(v_.game_folder) + "\\mysettings\\game_server"
        file_path3 = dir_path2 + "\\game_server.txt"

        isFile = False
        while isFile is False:
            if os.path.isdir(dir_path2) == True:
                if os.path.isfile(file_path3) == True:
                    isFile = True
                    # 파일 읽기
                    with open(file_path3, "r", encoding='utf-8-sig') as file:
                        line3 = file.read()
                        print('game server', line3)
                else:
                    print('game server 파일(line3) 없당')
                    with open(file_path3, "w", encoding='utf-8-sig') as file:
                        file.write("k0")
            else:
                os.makedirs(dir_path2)




        self.monitor = QGroupBox('My Cla Monitor & Arduino')

        self.own = QLabel("       현재 소유자 : " + line_[0] + "\n\n")
        self.computer = QLabel("       현재 컴퓨터 : " + line_[1] + " 컴퓨터\n\n")
        self.game_server = QLabel("       현재 게임서버 : " + line3 + "\n\n")
        self.mouse_arduino = QLabel("       현재 아두이노 활성화 상태 : " + line2 + "\n\n")

        self.own_in = QLineEdit(self)
        self.own_in.setText(line_[0])
        self.computer_in = QLineEdit(self)
        self.computer_in.setText(line_[1])
        self.game_server_in = QLineEdit(self)
        self.game_server_in.setText(line3)
        self.line_save = QPushButton("저장하기")
        self.line_save.clicked.connect(self.button_line_save)

        self.arduino_on = QPushButton("아두이노 on")
        self.arduino_on.clicked.connect(self.button_arduino_on)
        self.arduino_off = QPushButton("아두이노 off")
        self.arduino_off.clicked.connect(self.button_arduino_off)

        mo1_1 = QHBoxLayout()
        mo1_1.addWidget(self.own)

        mo1_2 = QHBoxLayout()
        mo1_2.addWidget(self.computer)

        mo1_5 = QHBoxLayout()
        mo1_5.addWidget(self.game_server)

        mo1_mouse = QHBoxLayout()
        mo1_mouse.addWidget(self.mouse_arduino)

        mo1_3 = QHBoxLayout()
        mo1_3.addStretch(1)
        mo1_3.addWidget(self.own_in)
        mo1_3.addWidget(self.computer_in)
        mo1_3.addWidget(self.game_server_in)
        mo1_3.addStretch(1)
        mo1_3.addWidget(self.line_save)
        mo1_3.addStretch(18)

        mo1_4 = QHBoxLayout()
        mo1_4.addWidget(self.arduino_on)
        mo1_4.addWidget(self.arduino_off)

        Mobox1 = QVBoxLayout()
        Mobox1.addStretch(1)
        Mobox1.addLayout(mo1_1)
        Mobox1.addLayout(mo1_2)
        Mobox1.addLayout(mo1_5)
        Mobox1.addLayout(mo1_mouse)
        Mobox1.addLayout(mo1_3)
        Mobox1.addStretch(3)
        Mobox1.addLayout(mo1_4)
        Mobox1.addStretch(3)

        self.monitor.setLayout(Mobox1)

        hbox_ = QHBoxLayout()
        hbox_.addWidget(self.monitor)

        Vbox_ = QVBoxLayout()
        Vbox_.addLayout(hbox_)

        self.setLayout(Vbox_)

    def button_line_save(self):
        own_ = self.own_in.text()  # line_edit text 값 가져오기
        computer_ = self.computer_in.text()
        game_server_ = self.game_server_in.text()
        print(own_)
        print(computer_)
        print(game_server_)

        self.own.setText("       현재 소유자 : " + own_ + "\n\n")
        self.computer.setText("       현재 컴퓨터 : " + computer_ + " 컴퓨터\n\n")
        self.game_server.setText("       현재 게임서버 : " + game_server_ + "\n\n")
        write_1 = own_ + ":" + computer_
        write_2 = game_server_
        dir_path = "C:\\my_games"
        file_path = dir_path + "\\line\\line.txt"
        file_path2 = dir_path + "\\" + str(v_.game_folder) + "\\mysettings\\game_server\\game_server.txt"

        with open(file_path, "w", encoding='utf-8-sig') as file:
            file.write(write_1)
        with open(file_path2, "w", encoding='utf-8-sig') as file:
            file.write(write_2)

    def button_arduino_on(self):
        print("arduino_on")
        file_path = "C:\\my_games\\mouse\\arduino.txt"
        with open(file_path, "w", encoding='utf-8-sig') as file:
            file.write("on")
        data = "on"
        self.mouse_arduino.setText("       현재 아두이노 활성화 상태 : " + data + "\n\n")
        v_.now_arduino = data



    def button_arduino_off(self):
        print("arduino_off")
        file_path = "C:\\my_games\\mouse\\arduino.txt"
        with open(file_path, "w", encoding='utf-8-sig') as file:
            file.write("off")
        data = "off"
        self.mouse_arduino.setText("       현재 아두이노 활성화 상태 : " + data + "\n\n")
        v_.now_arduino = data


class SecondTab(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        # self.set_rand_int()

    # onecla_openaiapi
    # my_google_custom_id
    def initUI(self):

        global one_id, one_pw, two_id, two_pw

        thismykey_one = "none"
        thismycategory_one = "none"
        thismytopic_one = "none"

        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path_one = dir_path + "\\mysettings\\idpw\\onecla.txt"
        file_path_two = dir_path + "\\mysettings\\idpw\\twocla.txt"
        file_path_topic = dir_path + "\\mysettings\\idpw\\onecla_topic.txt"
        file_path_openaiapi = dir_path + "\\mysettings\\idpw\\onecla_openaiapi.txt"
        file_path_google_custom = dir_path + "\\mysettings\\idpw\\onecla_google_custom.txt"
        file_path_topic_system = dir_path + "\\mysettings\\idpw\\topic_system.txt"
        file_path_topic_user = dir_path + "\\mysettings\\idpw\\topic_user.txt"

        for i in range(4):
            if os.path.isfile(file_path_one) == True:
                # 파일 읽기
                with open(file_path_one, "r", encoding='utf-8-sig') as file:
                    lines_one = file.read().split('\n')
                    if len(lines_one) > 3:
                        thismyid_one = lines_one[0]
                        v_.wd_id = thismyid_one
                        thismypw_one = lines_one[1]
                        v_.wd_pw = thismypw_one
                        thismyps_one = lines_one[2]
                        v_.domain_adress = thismyps_one
                        thismycategory_one = lines_one[3]
                        v_.my_category = thismycategory_one
                        break

                    else:
                        print("mysettings\\idpw\\onecla.txt 정보가 없다.")
            else:
                print('onecla 파일 없당')
                with open(file_path_one, "w", encoding='utf-8-sig') as file:
                    data = "none \n none \n none \n none"
                    file.write(data)
        for i in range(4):
            if os.path.isfile(file_path_openaiapi) == True:
                # 파일 읽기
                with open(file_path_openaiapi, "r", encoding='utf-8-sig') as file:
                    lines_one = file.read()

                    thismykey_one = lines_one
                    v_.api_key = thismykey_one
                    break
            else:
                print('onecla_openaiapi 파일 없당')
                with open(file_path_openaiapi, "w", encoding='utf-8-sig') as file:
                    data = "none"
                    file.write(data)
        for i in range(4):
            if os.path.isfile(file_path_google_custom) == True:
                # 파일 읽기
                with open(file_path_google_custom, "r", encoding='utf-8-sig') as file:
                    lines_one = file.read().split('\n')
                    if len(lines_one) > 1:
                        v_.my_google_custom_id = lines_one[0]
                        v_.my_google_custom_api = lines_one[1]
                        break

                    else:
                        print("mysettings\\idpw\\onecla_google_custom.txt 정보가 없다.")
            else:
                print('onecla_google_custom 파일 없당')
                with open(file_path_openaiapi, "w", encoding='utf-8-sig') as file:
                    data = "none \n none"
                    file.write(data)

        for i in range(3):
            if os.path.isfile(file_path_topic) == True:
                # 파일 읽기
                with open(file_path_topic, "r", encoding='utf-8-sig') as file:
                    thismytopic_one = file.read()
                    v_.my_topic = thismytopic_one
                    break


            else:
                with open(file_path_topic, "w", encoding='utf-8-sig') as file:
                    file.write("- 주제는 실생활에서 활용도 높은 세금, 지원금, 연금, 공과금, 부동산, 법률, 주식 등의 돈과 관련된 항목을 위주로 설정")

        for i in range(3):
            if os.path.isfile(file_path_topic_system) == True:
                # 파일 읽기
                with open(file_path_topic_system, "r", encoding='utf-8-sig') as file:
                    topic_system_one = file.read()
                    v_.my_topic_system = topic_system_one
                    break


            else:
                with open(file_path_topic_system, "w", encoding='utf-8-sig') as file:
                    file.write(
                        f"""
                    주요 독자는 정책·생활지원금·신청제도·절약팁 등 실질적 도움이 되는 콘텐츠를 찾는 일반 대중입니다.
                    **주의:** 제목에 '2025년 여름철', '이번 달' 등의 반복적 시점 표현은 제외하고, 정보 중심 키워드로 작성하세요."""
                    )

        for i in range(3):
            if os.path.isfile(file_path_topic_user) == True:
                # 파일 읽기
                with open(file_path_topic_user, "r", encoding='utf-8-sig') as file:
                    topic_user_one = file.read()
                    v_.my_topic_user = topic_user_one
                    break


            else:
                with open(file_path_topic_user, "w", encoding='utf-8-sig') as file:
                    file.write(
                        f"""
                        - 특히 아래 분야 우선 고려:
          - 부동산 정책, 금융 혜택, 세금 감면, 정부 지원금, 생활 신청제도, 에너지 절약, 소비자 혜택
"""
                    )

        if os.path.isfile(file_path_two) == True:
            # 파일 읽기
            with open(file_path_two, "r", encoding='utf-8-sig') as file:
                lines_two = file.read().split('\n')
                print('lines_two', lines_two)
                thismyid_two = lines_two[0]
                thismypw_two = lines_two[1]
                thismyps_two = lines_two[2]

                two_id = thismyid_two
                two_pw = thismypw_two
        else:
            print('two 파일 없당')
            thismyid_two = 'none'
            thismyps_two = 'none'

        # 111

        self.com_group1 = QGroupBox('One Cla')
        self.one_cla_id = QLabel("       WD_ID                ")
        self.one_cla_pw = QLabel("       WD_PW              ")
        self.one_cla_ps = QLabel("       도메인주소          ")
        self.one_cla_ca = QLabel("      등록할 카테고리    ")

        self.one_cla_key = QLabel("      OPENAI_API_KEY ")

        self.one_cla_google_custom = QLabel("      Google_Custom ")

        self.one_cla_topic = QLabel("      원하는 주제 선정   ")

        self.one_cla_id_now = QLabel("       워드프레스ID : " + thismyid_one + "\n\n")
        self.one_cla_ps_now = QLabel("       등록도메인주소 : " + thismyps_one)
        self.one_cla_ca_now = QLabel("       자동 카테고리명 : " + thismycategory_one)
        self.one_cla_topic_now = QLabel("       원하는 주제선정 : " + thismytopic_one)

        self.pushButton_login1 = QPushButton("로그인하기")
        self.pushButton_login1.clicked.connect(self.let_is_login_1)

        self.pushButton_copy_id_1 = QPushButton("현재 내 아이디 복사")
        self.pushButton_copy_id_1.clicked.connect(self.let_is_copy_id_1)

        self.pushButton_copy_pw_1 = QPushButton("패스워드 복사")
        self.pushButton_copy_pw_1.clicked.connect(self.let_is_copy_pw_1)

        self.pushButton_left = QPushButton("좌로 정렬")
        self.pushButton_left.clicked.connect(self.win_left)

        # self.one_cla_id_in = QLineEdit()
        self.one_cla_id_in = QLineEdit(self)
        self.one_cla_id_in.setText(thismyid_one)
        self.one_cla_pw_in = QLineEdit(self)
        self.one_cla_pw_in.setText("비밀번호를 입력하세요.")
        self.one_cla_ps_in = QLineEdit(self)
        self.one_cla_ps_in.setText(thismyps_one)
        self.one_cla_category_in = QLineEdit(self)
        self.one_cla_category_in.setText(thismycategory_one)

        self.pushButton_one = QPushButton("내 정보 저장하기")
        self.pushButton_one.clicked.connect(self.button_event1)

        self.one_cla_key_in = QLineEdit(self)
        self.one_cla_key_in.setText("key값을 입력하세요.")
        self.pushButton_one_openaiapi_key = QPushButton("openai api key 등록하기")
        self.pushButton_one_openaiapi_key.clicked.connect(self.button_event1_openaiapi)

        self.one_cla_google_custom_id_in = QLineEdit(self)
        self.one_cla_google_custom_id_in.setText("google_custom_id 값을 입력하세요.")
        self.one_cla_google_custom_pw_in = QLineEdit(self)
        self.one_cla_google_custom_pw_in.setText("google_custom_pw 값을 입력하세요.")
        self.pushButton_one_google_custom = QPushButton("google custom 등록하기")
        self.pushButton_one_google_custom.clicked.connect(self.button_event1_google_custom)

        self.one_cla_topic_in = QLineEdit(self)
        self.one_cla_topic_in.setText("")

        self.pushButton_one_topic = QPushButton("주제선정")
        self.pushButton_one_topic.clicked.connect(self.button_event1_1)

        vbox1_1 = QHBoxLayout()
        vbox1_1.addWidget(self.one_cla_id_now)

        vbox1_2 = QHBoxLayout()
        vbox1_2.addWidget(self.one_cla_ps_now)

        vbox1_22 = QHBoxLayout()
        vbox1_22.addWidget(self.one_cla_ca_now)

        vbox1_222 = QHBoxLayout()
        vbox1_222.addWidget(self.one_cla_topic_now)

        vbox1_log = QHBoxLayout()
        vbox1_log.addStretch(5)
        vbox1_log.addWidget(self.pushButton_login1)
        vbox1_log.addStretch(5)
        vbox1_log.addWidget(self.pushButton_copy_id_1)
        vbox1_log.addStretch(1)
        vbox1_log.addWidget(self.pushButton_copy_pw_1)
        vbox1_log.addStretch(5)

        vbox1_left = QHBoxLayout()
        vbox1_left.addStretch(15)
        vbox1_left.addWidget(self.pushButton_left)
        vbox1_left.addStretch(1)

        vbox1_3 = QHBoxLayout()
        vbox1_3.addWidget(self.one_cla_id)
        vbox1_3.addWidget(self.one_cla_id_in)

        vbox1_4 = QHBoxLayout()
        vbox1_4.addWidget(self.one_cla_pw)
        vbox1_4.addWidget(self.one_cla_pw_in)

        vbox1_5 = QHBoxLayout()
        vbox1_5.addWidget(self.one_cla_ps)
        vbox1_5.addWidget(self.one_cla_ps_in)

        vbox1_555 = QHBoxLayout()
        vbox1_555.addWidget(self.one_cla_ca)
        vbox1_555.addWidget(self.one_cla_category_in)

        vbox1_6 = QHBoxLayout()
        vbox1_6.addStretch(5)
        vbox1_6.addWidget(self.pushButton_one)

        vbox1_topic = QHBoxLayout()
        vbox1_topic.addWidget(self.one_cla_topic)
        vbox1_topic.addWidget(self.one_cla_topic_in)
        vbox1_topic_btn = QHBoxLayout()
        vbox1_topic_btn.addStretch(5)
        vbox1_topic_btn.addWidget(self.pushButton_one_topic)

        vbox1_7 = QHBoxLayout()
        vbox1_7.addWidget(self.one_cla_key)
        vbox1_7.addWidget(self.one_cla_key_in)

        vbox1_77 = QHBoxLayout()
        vbox1_77.addStretch(5)
        vbox1_77.addWidget(self.pushButton_one_openaiapi_key)

        vbox1_8 = QHBoxLayout()
        vbox1_8.addWidget(self.one_cla_google_custom)
        vbox1_8.addWidget(self.one_cla_google_custom_id_in)
        vbox1_8.addWidget(self.one_cla_google_custom_pw_in)

        vbox1_88 = QHBoxLayout()
        vbox1_88.addStretch(5)
        vbox1_88.addWidget(self.pushButton_one_google_custom)


        Vbox1 = QVBoxLayout()
        Vbox1.addStretch(1)
        Vbox1.addLayout(vbox1_1)
        Vbox1.addLayout(vbox1_2)
        Vbox1.addLayout(vbox1_22)
        Vbox1.addLayout(vbox1_222)
        Vbox1.addStretch(1)
        Vbox1.addLayout(vbox1_log)
        Vbox1.addStretch(5)
        Vbox1.addLayout(vbox1_left)
        Vbox1.addStretch(3)
        Vbox1.addLayout(vbox1_3)
        Vbox1.addLayout(vbox1_4)
        Vbox1.addLayout(vbox1_5)
        Vbox1.addLayout(vbox1_555)
        Vbox1.addLayout(vbox1_6)
        Vbox1.addLayout(vbox1_7)
        Vbox1.addLayout(vbox1_77)
        Vbox1.addLayout(vbox1_8)
        Vbox1.addLayout(vbox1_88)

        Vbox1.addLayout(vbox1_topic)
        Vbox1.addLayout(vbox1_topic_btn)

        Vbox1.addStretch(2)
        # maul_add = QPushButton('마을 의뢰 추가')
        # maul_add.clicked.connect(self.onActivated_maul_add)
        # vbox6.addWidget(maul_add)
        self.com_group1.setLayout(Vbox1)

        # 222
        self.com_group2 = QGroupBox('Two Cla')
        self.two_cla_id = QLabel("       ID          ")
        self.two_cla_pw = QLabel("       PW        ")
        self.two_cla_ps = QLabel("       참고사항 ")

        self.two_cla_id_now = QLabel("       현재 내 아이디 : " + thismyid_two + "\n\n")
        self.two_cla_ps_now = QLabel("       무슨 참고 사항을 적었나요? " + thismyps_two)

        self.pushButton_login2 = QPushButton("로그인하기")
        self.pushButton_login2.clicked.connect(self.let_is_login_2)

        self.pushButton_copy_id_2 = QPushButton("현재 내 아이디 복사")
        self.pushButton_copy_id_2.clicked.connect(self.let_is_copy_id_2)

        self.pushButton_copy_pw_2 = QPushButton("패스워드 복사")
        self.pushButton_copy_pw_2.clicked.connect(self.let_is_copy_pw_2)

        self.pushButton_right = QPushButton("우로 정렬")
        self.pushButton_right.clicked.connect(self.win_right)

        self.two_cla_id_in = QLineEdit(self)
        self.two_cla_id_in.setText(thismyid_two)
        self.two_cla_pw_in = QLineEdit(self)
        self.two_cla_pw_in.setText(thismypw_two)
        self.two_cla_ps_in = QLineEdit(self)
        self.two_cla_ps_in.setText(thismyps_two)
        self.pushButton_two = QPushButton("저장하기")
        self.pushButton_two.clicked.connect(self.button_event2)

        vbox2_1 = QHBoxLayout()
        vbox2_1.addWidget(self.two_cla_id_now)

        vbox2_2 = QHBoxLayout()
        vbox2_2.addWidget(self.two_cla_ps_now)

        vbox2_log = QHBoxLayout()
        vbox2_log.addStretch(5)
        vbox2_log.addWidget(self.pushButton_login2)
        vbox2_log.addStretch(5)
        vbox2_log.addWidget(self.pushButton_copy_id_2)
        vbox2_log.addStretch(1)
        vbox2_log.addWidget(self.pushButton_copy_pw_2)
        vbox2_log.addStretch(5)

        vbox2_right = QHBoxLayout()
        vbox2_right.addStretch(1)
        vbox2_right.addWidget(self.pushButton_right)
        vbox2_right.addStretch(15)

        vbox2_3 = QHBoxLayout()
        vbox2_3.addWidget(self.two_cla_id)
        vbox2_3.addWidget(self.two_cla_id_in)

        vbox2_4 = QHBoxLayout()
        vbox2_4.addWidget(self.two_cla_pw)
        vbox2_4.addWidget(self.two_cla_pw_in)

        vbox2_5 = QHBoxLayout()
        vbox2_5.addWidget(self.two_cla_ps)
        vbox2_5.addWidget(self.two_cla_ps_in)

        vbox2_6 = QHBoxLayout()
        vbox2_6.addStretch(5)
        vbox2_6.addWidget(self.pushButton_two)

        Vbox2 = QVBoxLayout()
        Vbox2.addStretch(1)
        Vbox2.addLayout(vbox2_1)
        Vbox2.addLayout(vbox2_2)
        Vbox2.addStretch(1)
        Vbox2.addLayout(vbox2_log)
        Vbox2.addStretch(5)
        Vbox2.addLayout(vbox2_right)
        Vbox2.addStretch(3)
        Vbox2.addLayout(vbox2_3)
        Vbox2.addLayout(vbox2_4)
        Vbox2.addLayout(vbox2_5)
        Vbox2.addLayout(vbox2_6)
        Vbox2.addStretch(2)
        # maul_add = QPushButton('마을 의뢰 추가')
        # maul_add.clicked.connect(self.onActivated_maul_add)
        # vbox6.addWidget(maul_add)
        self.com_group2.setLayout(Vbox2)

        ###
        hbox_ = QHBoxLayout()
        hbox_.addWidget(self.com_group2)

        Vbox_ = QVBoxLayout()
        Vbox_.addLayout(hbox_)

        ###
        hbox__ = QHBoxLayout()
        hbox__.addWidget(self.com_group1)
        hbox__.addLayout(Vbox_)

        ###
        vbox = QVBoxLayout()
        vbox.addLayout(hbox__)
        self.setLayout(vbox)

    def win_left(self):
        print("왼쪽으로 정렬 합니다.")
        pyautogui.keyDown('win')
        pyautogui.press('left')
        pyautogui.keyUp('win')

    def win_right(self):
        print("왼쪽으로 정렬 합니다.")
        pyautogui.keyDown('win')
        pyautogui.press('right')
        pyautogui.keyUp('win')

    def win_left_ex(self):
        print("왼쪽으로 정렬 합니다.")
        full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\check\\moonlight_title.PNG"
        img_array = np.fromfile(full_path, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        imgs_ = imgs_set_(960, 0, 1920, 1080, "three", img, 0.8)
        time.sleep(0.3)
        if imgs_ is not None and imgs_ != False:
            print("왼쪽 보여", imgs_)
            time.sleep(0.5)

            click_pos_reg(imgs_.x + 100, imgs_.y, "three")
            time.sleep(0.5)
            win_right_move("three")
            # pyautogui.keyDown('win')
            # pyautogui.press('right')
            # pyautogui.keyUp('win')
            time.sleep(0.3)
            full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\check\\moonlight_title.PNG"
            img_array = np.fromfile(full_path, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            imgs_ = imgs_set_(960, 0, 1920, 1080, "three", img, 0.8)
            if imgs_ is not None:
                click_pos_reg(imgs_.x + 100, imgs_.y, "three")

    def win_right_ex(self):
        print("오른쪽으로 정렬 합니다.")
        full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\check\\moonlight_title.PNG"
        img_array = np.fromfile(full_path, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        imgs_ = imgs_set_(960, 0, 1920, 1080, "four", img, 0.8)
        time.sleep(0.3)
        if imgs_ is not None and imgs_ != False:
            print("오른쪽 보여", imgs_)
            time.sleep(0.5)

            click_pos_reg(imgs_.x + 100, imgs_.y, "four")
            time.sleep(0.5)
            win_right_move("four")
            # pyautogui.keyDown('win')
            # pyautogui.press('right')
            # pyautogui.keyUp('win')
            time.sleep(0.3)
            full_path = "c:\\my_games\\" + str(v_.game_folder) + "\\" + str(v_.data_folder) + "\\imgs\\check\\moonlight_title.PNG"
            img_array = np.fromfile(full_path, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            imgs_ = imgs_set_(960, 0, 1920, 1080, "four", img, 0.8)
            if imgs_ is not None and imgs_ != False:
                click_pos_reg(imgs_.x + 100, imgs_.y, "four")

    def let_is_login_1(self):
        print("로그인1 버튼 입니다.")

    def let_is_login_2(self):
        print("로그인2 버튼 입니다.")

    def let_is_copy_id_1(self):
        print("let_is_copy_id_1", one_id)
        clipboard.copy(one_id)
        # 색상
        self.pushButton_copy_id_1.setDisabled(True)
        QTest.qWait(1500)
        self.pushButton_copy_id_1.setDisabled(False)

    def let_is_copy_pw_1(self):
        print("let_is_copy_pw_1", one_pw)
        clipboard.copy(one_pw)
        self.pushButton_copy_pw_1.setDisabled(True)
        QTest.qWait(1500)
        self.pushButton_copy_pw_1.setDisabled(False)

    def let_is_copy_id_2(self):
        print("let_is_copy_id_2", two_id)
        clipboard.copy(two_id)
        self.pushButton_copy_id_2.setDisabled(True)
        QTest.qWait(1500)
        self.pushButton_copy_id_2.setDisabled(False)

    def let_is_copy_pw_2(self):
        print("let_is_copy_pw_2", two_pw)
        clipboard.copy(two_pw)
        self.pushButton_copy_pw_2.setDisabled(True)
        QTest.qWait(1500)
        self.pushButton_copy_pw_2.setDisabled(False)

    def button_event1(self):
        one_cla_id_ = self.one_cla_id_in.text()  # line_edit text 값 가져오기
        one_cla_pw_ = self.one_cla_pw_in.text()
        one_cla_ps_ = self.one_cla_ps_in.text()
        one_cla_key_ = self.one_cla_key_in.text()
        one_cla_ca_ = self.one_cla_category_in.text()


        print(one_cla_id_)

        one_cla_id_result = "       워드프레스ID : " + one_cla_id_ + "\n\n"
        one_cla_ps_result = "       등록도메인주소 " + one_cla_ps_
        one_cla_ca_result = "       자동 카테고리명 " + one_cla_ca_
        self.one_cla_id_now.setText(one_cla_id_result)
        self.one_cla_ps_now.setText(one_cla_ps_result)
        self.one_cla_ca_now.setText(one_cla_ca_result)
        shcedule = one_cla_id_ + "\n" + one_cla_pw_ + "\n" + one_cla_ps_ + "\n" + one_cla_key_ + "\n" + one_cla_ca_
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path_one = dir_path + "\\mysettings\\idpw\\onecla.txt"
        with open(file_path_one, "w", encoding='utf-8-sig') as file:
            file.write(shcedule)

    def button_event1_openaiapi(self):
        one_cla_key_ = self.one_cla_key_in.text()



        shcedule = one_cla_key_
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path_one = dir_path + "\\mysettings\\idpw\\onecla_openaiapi.txt"
        with open(file_path_one, "w", encoding='utf-8-sig') as file:
            file.write(shcedule)

    def button_event1_google_custom(self):
        google_custom_id_in_ = self.one_cla_google_custom_id_in.text()
        google_custom_id_pw_ = self.one_cla_google_custom_pw_in.text()



        shcedule = google_custom_id_in_ + "\n" + google_custom_id_pw_
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path_one = dir_path + "\\mysettings\\idpw\\onecla_google_custom.txt"
        with open(file_path_one, "w", encoding='utf-8-sig') as file:
            file.write(shcedule)

    def button_event1_1(self):
        one_cla_to_ = self.one_cla_topic_in.text()

        one_cla_to__result = "       원하는 주제선정 : " + one_cla_to_
        self.one_cla_topic_now.setText(one_cla_to__result)
        shcedule = one_cla_to_
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path_one = dir_path + "\\mysettings\\idpw\\onecla_topic.txt"
        with open(file_path_one, "w", encoding='utf-8-sig') as file:
            file.write(shcedule)

    def button_event2(self):
        two_cla_id_ = self.two_cla_id_in.text()  # line_edit text 값 가져오기
        two_cla_pw_ = self.two_cla_pw_in.text()
        two_cla_ps_ = self.two_cla_ps_in.text()
        print(two_cla_id_)
        print(two_cla_pw_)

        two_cla_id_result = "       현재 내 아이디 : " + two_cla_id_ + "\n\n"
        two_cla_ps_result = "       무슨 참고 사항을 적었나요? " + two_cla_ps_
        self.two_cla_id_now.setText(two_cla_id_result)
        self.two_cla_ps_now.setText(two_cla_ps_result)
        shcedule = two_cla_id_ + "\n" + two_cla_pw_ + "\n" + two_cla_ps_
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path_two = dir_path + "\\mysettings\\idpw\\twocla.txt"
        with open(file_path_two, "w", encoding='utf-8-sig') as file:
            file.write(shcedule)

######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
class FirstTab(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.set_rand_int()

    def initUI(self):
        global rowcount, colcount

        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"

        if os.path.isfile(file_path) == True:
            # 파일 읽기
            with open(file_path, "r", encoding='utf-8-sig') as file:
                lines = file.read().split('\n')
        else:
            print('파일 없당')


        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(lines))

        self.tableWidget.setColumnCount(1)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setVisible(False)  # 행번호 안나오게 하는 코드
        self.tableWidget.setHorizontalHeaderLabels(["프롬프트"])

        self.label = QLabel('')

        ###
        self.tableWidget.cellClicked.connect(self.set_label)
        rowcount = self.tableWidget.rowCount()
        colcount = self.tableWidget.columnCount()


        # 각종 버튼

        # 위로

        self.up_btn = QPushButton('up')
        self.up_btn.clicked.connect(self.up_change)

        # 아래로

        self.down_btn = QPushButton('down')
        self.down_btn.clicked.connect(self.down_change)

        # 자동 발행 버튼
        self.auto_blog = QPushButton('자동 발행')
        self.auto_blog.clicked.connect(self.auto_blog_start)

        # 테스트 버튼
        self.mytestin = QPushButton('테스뚜')
        self.mytestin.clicked.connect(self.mytestin_)
        self.again_restart = QPushButton('업데이트')
        self.again_restart.clicked.connect(self.again_restart_game)

        # 프롬프트 선택 삭제
        self.del_ = QPushButton('삭제')
        self.del_.clicked.connect(self.prompt_del)
        # 프롬프트 초기화
        self.clear = QPushButton('초기화')
        self.clear.clicked.connect(self.prompt_refresh)
        # 프롬프트 완전 초기화
        self.clear_all = QPushButton('완전초기화')
        self.clear_all.clicked.connect(self.prompt_refresh_all)


        # 프롬프트 추가

        self.prompt_groupbox = QGroupBox('프롬프트 추가 및 변경하기')
        self.prompt_example = QLabel("프롬프트를 적어 아래 추가 및 변경 버튼 눌러주세요")
        self.require_prompt = QLineEdit(self)

        prompt_layout = QVBoxLayout()
        prompt_layout.addWidget(self.prompt_example)
        prompt_layout.addWidget(self.require_prompt)

        prompt_upload = QPushButton('프롬프트 추가')
        prompt_upload.clicked.connect(self.onActivated_prompt_upload)
        self.prompt_change_btn = QPushButton('프롬프트 변경')
        self.prompt_change_btn.clicked.connect(self.prompt_change_one)

        prompt_layout.addWidget(prompt_upload)
        prompt_layout.addWidget(self.prompt_change_btn)
        self.prompt_groupbox.setLayout(prompt_layout)


        # 임시글 발행

        self.temporary_groupbox = QGroupBox('임시 글 발행하기')
        self.temporary_example = QLabel("키워드 적어 아래 발행 버튼 눌러주세요")
        self.require_temporary= QLineEdit(self)

        temporary_layout = QVBoxLayout()
        temporary_layout.addWidget(self.temporary_example)
        temporary_layout.addWidget(self.require_temporary)
        temporary_upload = QPushButton('임시글 발행')
        temporary_upload.clicked.connect(self.onActivated_temporary_upload)
        temporary_layout.addWidget(temporary_upload)
        self.temporary_groupbox.setLayout(temporary_layout)

        # 레이아웃

        updown_btn_QV_1 = QVBoxLayout()
        updown_btn_QV_1.addWidget(self.up_btn)
        updown_btn_QV_1.addWidget(self.down_btn)


        top_btn_QH_1 = QHBoxLayout()
        top_btn_QH_1.addWidget(self.auto_blog)
        top_btn_QH_1.addStretch(4)
        top_btn_QH_1.addWidget(self.mytestin)
        top_btn_QH_1.addWidget(self.again_restart)
        top_btn_QH_1.addWidget(self.del_)
        top_btn_QH_1.addWidget(self.clear)
        top_btn_QH_1.addWidget(self.clear_all)



        top_btn_QH_2 = QHBoxLayout()
        top_btn_QH_2.addLayout(updown_btn_QV_1)
        top_btn_QH_2.addStretch(4)
        top_btn_QH_2.addStretch(4)
        top_btn_QH_2.addLayout(top_btn_QH_1)







        bottom_box_qv = QVBoxLayout()
        bottom_box_qv.addWidget(self.prompt_groupbox)
        bottom_box_qv.addWidget(self.temporary_groupbox)


        bottom_box_qh = QHBoxLayout()
        bottom_box_qh.addLayout(bottom_box_qv)

        all_box = QVBoxLayout()

        # self.tableWidget.resizeColumnsToContents()
        all_box.addWidget(self.tableWidget)
        all_box.addWidget(self.label)
        all_box.addLayout(top_btn_QH_2)
        all_box.addLayout(bottom_box_qh)
        self.setLayout(all_box)

    def auto_blog_start(self):

        start_ready = game_Playing_Ready(self)
        start_ready.start()

    def up_change(self):
        global rowcount, colcount, thisRow, thisCol
        print("up_change")

        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
        file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"

        try:
            ##############프롬프트 변경
            print("thisValue", thisValue)
            print("thisCol", thisCol)
            print("thisRow", thisRow)

            # myQuest_number_check('all', 'refresh')

            if thisRow < 2 or thisRow == "none":
                print("변경 불가능 합니다. 다시 선택해 주세요.")
            else:
                if os.path.isdir(dir_path) == False:
                    print('디렉토리 존재하지 않음')
                    os.makedirs(dir_path)

                ######################

                ######################

                with open(file_path, "r", encoding='utf-8-sig') as file:
                    lines = file.read().split('\n')
                    # lines = ' '.join(lines).split()

                    isSchedule_ = False
                    while isSchedule_ is False:
                        if lines == [] or lines == "":
                            print("스케쥴이 비었다 : myQuest_play_check")
                            with open(file_path3, "r", encoding='utf-8-sig') as file:
                                schedule_ready = file.read()
                            with open(file_path, "w", encoding='utf-8-sig') as file:
                                file.write(schedule_ready)
                            with open(file_path, "r", encoding='utf-8-sig') as file:
                                lines = file.read().split('\n')
                        else:
                            isSchedule_ = True
                    # 표 수정
                    reset_schedule_ = ""


                    contact_row = lines[thisRow - 1]

                    aim_row = lines[thisRow - 2]



                    for i in range(len(lines)):

                        if i == thisRow - 2:
                            reset_schedule_ += contact_row + "\n"
                        elif i == thisRow - 1:
                            reset_schedule_ += aim_row + "\n"
                        elif lines[i] == "":
                            reset_schedule_ += lines[i]
                        else:
                            reset_schedule_ += lines[i] + "\n"

                    print('reset_schedule_표 수정', reset_schedule_)
                    with open(file_path, "w", encoding='utf-8-sig') as file:
                        file.write(reset_schedule_)
                    with open(file_path3, "w", encoding='utf-8-sig') as file:
                        file.write(reset_schedule_)

                #######################################################



                with open(file_path, "r", encoding='utf-8-sig') as file:
                    lines = file.read()

                ############################################################




                self.set_rand_int()
            thisRow = thisRow - 1

        except Exception as e:
            print(e)
            return 0

    def down_change(self):
        global rowcount, colcount, thisRow
        print("down_change")

        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
        file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"

        try:
            ##############프롬프트 변경
            print("thisValue", thisValue)
            print("thisCol", thisCol)
            print("thisRow", thisRow)

            # myQuest_number_check('all', 'refresh')

            if thisRow > rowcount - 2 or thisRow == "none":
                print("변경 불가능 합니다. 다시 선택해 주세요.")
            else:
                if os.path.isdir(dir_path) == False:
                    print('디렉토리 존재하지 않음')
                    os.makedirs(dir_path)

                ######################

                ######################

                with open(file_path, "r", encoding='utf-8-sig') as file:
                    lines = file.read().split('\n')
                    # lines = ' '.join(lines).split()

                    isSchedule_ = False
                    while isSchedule_ is False:
                        if lines == [] or lines == "":
                            print("스케쥴이 비었다 : myQuest_play_check")
                            with open(file_path3, "r", encoding='utf-8-sig') as file:
                                schedule_ready = file.read()
                            with open(file_path, "w", encoding='utf-8-sig') as file:
                                file.write(schedule_ready)
                            with open(file_path, "r", encoding='utf-8-sig') as file:
                                lines = file.read().split('\n')
                        else:
                            isSchedule_ = True
                    # 표 수정
                    reset_schedule_ = ""

                    contact_row = lines[thisRow - 1]
                    aim_row = lines[thisRow]

                    for i in range(len(lines)):

                        if i == thisRow:
                            reset_schedule_ += contact_row + "\n"
                        elif i == thisRow - 1:
                            reset_schedule_ += aim_row + "\n"
                        elif lines[i] == "":
                            reset_schedule_ += lines[i]
                        else:
                            reset_schedule_ += lines[i] + "\n"

                    print('reset_schedule_표 수정', reset_schedule_)
                    with open(file_path, "w", encoding='utf-8-sig') as file:
                        file.write(reset_schedule_)
                    with open(file_path3, "w", encoding='utf-8-sig') as file:
                        file.write(reset_schedule_)

                #######################################################

                with open(file_path, "r", encoding='utf-8-sig') as file:
                    lines = file.read()

                ############################################################

                self.set_rand_int()
            thisRow = thisRow + 1
        except Exception as e:
            print(e)
            return 0


    def again_restart_game(self):

        # 업데이트

        self.again_restart.setText("업뎃 중")
        self.again_restart.setStyleSheet("color:black; background:blue")
        self.again_restart.setDisabled(True)
        QTest.qWait(1000)

        print("업데이트 후 재시작")
        # git pull 실행 부분
        # git_dir = '{https://github.com/rntkdgnl932/ncs.git}'
        # g = git.cmd.Git(git_dir)
        # g.pull()
        # Repo('여기 비워진것은 현재 실행되는 창의 위치란 뜻...현재 실행되는 창의 위치 기준...상대경로임...')
        dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
        file_path = dir_path + "\\start.txt"
        with open(file_path, "w", encoding='utf-8-sig') as file:
            data = 'no'
            file.write(str(data))

        my_repo = git.Repo()
        my_repo.remotes.origin.pull()
        time.sleep(1)
        # 실행 후 재시작 부분
        os.execl(sys.executable, sys.executable, *sys.argv)

        # self.game.isCheck = True
        # self.game.start()
        # self.again_restart_background()


    def onActivated_prompt_upload(self, text):
        # 프롬프트 추가
        from test_ import go_test
        print("onActivated_prompt_upload")
        is_prompt = "- " + self.require_prompt.text() + "\n"

        self.table_load()

        print("is_prompt", is_prompt)
        # self.tableWidget.removeRow(5)
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        row_add = self.tableWidget.rowCount()
        # row_add = self.tableWidget.rowCount() - 1
        data_ = re.sub("\n", "", is_prompt)
        datas = data_
        print("datas", datas)
        print(len(datas))
        print(range(colcount))
        print("test............")
        for i in range(len(datas)):
            self.tableWidget.setItem(row_add, i, QTableWidgetItem(datas[i]))

        print("test............")
        self.mySchedule_add(is_prompt)
        rowcount = self.tableWidget.rowCount()



    def onActivated_temporary_upload(self, text):

        x = temporary_upload(self)
        is_keyword = self.require_temporary.text()
        x.set_keyword(is_keyword)  # 키워드 전달
        x.start()











    def mystatus_refresh(self):
        print("현재상태 초기화")
        # 초기화 시간
        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path2 = dir_path + "\\mysettings\\refresh_time\\quest.txt"
        file_path13 = dir_path + "\\mysettings\\refresh_time\\refresh_time.txt"

        isRefresh = False
        while isRefresh is False:
            if os.path.isfile(file_path13) == True:
                with open(file_path13, "r", encoding='utf-8-sig') as file:
                    refresh_time = file.read()
                    refresh_time_bool = refresh_time.isdigit()
                    if refresh_time_bool == True:
                        isRefresh = True
                        print("refresh_time", refresh_time)
                    else:
                        with open(file_path13, "w", encoding='utf-8-sig') as file:
                            file.write(str(4))
            else:
                with open(file_path13, "w", encoding='utf-8-sig') as file:
                    file.write(str(4))

        if os.path.isfile(file_path2) == True:
            # 파일 읽기
            with open(file_path2, "r", encoding='utf-8-sig') as file:
                lines2 = file.read().split('\n')
                day_ = lines2[0].split(":")
                re_time_ = str(day_[0]) + " => " + str(day_[1] + "시")
                print("최근 초기화 시간 : ", re_time_)
        else:
            re_time_ = "아직 모름..."
        self.set_rand_int()

    def set_rand_int(self):
        try:
            dir_path = "C:\\my_games\\" + str(v_.game_folder)
            file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
            file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
            if os.path.isfile(file_path) == True:
                # 파일 읽기
                with open(file_path, "r", encoding='utf-8-sig') as file:
                    lines = file.read().split('\n')
                    print("최초 프롬프트", lines)

                    reset_schedule_ = ""


                    for i in range(len(lines)):

                        if lines[i] == "":
                            print("빈 공백")
                        else:
                            reset_schedule_ += lines[i] + "\n"

                    v_.my_prompt = reset_schedule_
                    # lines = ' '.join(lines).split()
                with open(file_path3, "r", encoding='utf-8-sig') as file:
                    shcedule = file.read().split('\n')
                    shcedule = ' '.join(shcedule).split()

            else:
                print('파일 없당')
                if os.path.isdir(dir_path) == True:
                    print('디렉토리 존재함')
                    with open(file_path3, "r", encoding='utf-8-sig') as file:
                        shcedule = file.read().split('\n')
                        with open(file_path, "w", encoding='utf-8-sig') as file:
                            file.write(str(shcedule))
                            with open(file_path, "r", encoding='utf-8-sig') as file:
                                lines = file.read().split('\n')
                else:
                    print('디렉토리 존재하지 않음')
                    os.makedirs(dir_path)
                    with open(file_path3, "r", encoding='utf-8-sig') as file:
                        shcedule = file.read().split('\n')
                        with open(file_path, "w", encoding='utf-8-sig') as file:
                            file.write(shcedule)
                            with open(file_path, "r", encoding='utf-8-sig') as file:
                                lines = file.read().split('\n')

            # print("ggggggggggggggggg", lines)

            # self.tableWidget.insertRow(self.tableWidget.rowCount(2))
            self.tableWidget.setColumnWidth(0, 800)
            # self.tableWidget.setColumnWidth(0, 50)
            # self.tableWidget.setColumnWidth(1, 40)
            # self.tableWidget.setColumnWidth(2, 240)
            # self.tableWidget.setColumnWidth(3, 80)
            # self.tableWidget.setColumnWidth(4, 50)
            # self.tableWidget.setColumnWidth(5, 40)
            # self.tableWidget.setColumnWidth(6, 240)
            # self.tableWidget.setColumnWidth(7, 80)

            self.tableWidget.setRowCount(0)

            row = 0
            for i in range(len(lines)):
                result = str(lines[i]).replace("\n", "")
                # result = str(lines[i]).strip()

                if not result:
                    continue

                self.tableWidget.insertRow(row)
                item = QTableWidgetItem(result)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.tableWidget.setItem(row , 0, item)
                row += 1
                    # self.tableWidget.resizeColumnsToContents()


        except Exception as e:
            print(e)
            return 0



    def set_label(self, row, column):
        global thisRow, thisCol, thisValue
        item = self.tableWidget.item(row, column)
        value = item.text()
        thisValue = value
        col = str(row + 1)
        col_ = int(col)
        col2 = str(column + 1)
        col_2 = int(col2)
        thisRow = col_
        thisCol = col_2
        print("0열 데이타", col_)  # good
        print("Row", str(row + 1))
        print("Column", str(column + 1))
        print("value", str(value))
        label_str = 'Row: ' + str(row + 1) + ', Column: ' + str(column + 1) + ', Value: ' + str(value)
        self.label.setText(label_str)

    # 스케쥴 수정 및 추가
    def sche_load_(self):
        global table_datas
        try:
            rowcount = self.tableWidget.rowCount()
            colcount = self.tableWidget.columnCount()
            print("schedule!!!", rowcount, colcount)
            datas = ""
            if rowcount != 0:
                for i in range(0, rowcount):
                    for j in range(0, colcount):
                        data = self.tableWidget.item(i, j)
                        if data is not None:
                            # if j + 1 == colcount:
                            datas += str(data.text()) + "\n"

                        else:
                            print("blank")
            table_datas = datas
            return table_datas
        except Exception as e:
            print(e)
            return 0

    def table_load(self):
        global rowcount, colcount
        print("table_load_rowcount", rowcount)
        print("table_load_colcount", colcount)
        if rowcount != 0:
            for i in range(0, rowcount):
                for j in range(0, colcount):
                    data = self.tableWidget.item(i, j)
                    if data is not None:
                        if j + 1 == colcount:
                            item = QTableWidgetItem()
                            item.setText(str(data.text()))
                            # datas += str(data.text()) + "\n"
                            self.tableWidget.setItem(i, j, item)
                        else:
                            item = QTableWidgetItem()
                            item.setText(str(data.text()))
                            # datas += str(data.text()) + ":"
                            self.tableWidget.setItem(i, j, item)

                    else:
                        print("blank")



    def prompt_del(self):
        global rowcount, colcount
        try:
            print("prompt_del")
            self.table_load()
            rowcount = self.tableWidget.rowCount()
            print("rowcount", rowcount)
            self.tableWidget.removeRow(thisRow - 1)
            rowcount = self.tableWidget.rowCount()
            print("rowcount!!!!!!!!!!!", rowcount)
            print("del")
            result = self.sche_load_()
            print("result prompt_del", result)
            how_ = "modify"
            self.mySchedule_change(how_, result)

            # 잠김
            self.del_mySchedule(thisRow - 1)
            self.mystatus_refresh()


        except Exception as e:
            print(e)
            return 0

    def del_mySchedule(self, is_row):
        try:

            print("is_row", is_row)

            if thisValue != "none":

                v_.one_cla_count = 0
                v_.two_cla_count = 0
                v_.one_cla_ing = 'check'
                v_.two_cla_ing = 'check'

                v_.dead_count = 0

                # myQuest_number_check('all', 'refresh')

                dir_path = "C:\\my_games\\" + str(v_.game_folder)
                file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
                file_path2 = dir_path + "\\mysettings\\refresh_time\\quest.txt"
                file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
                file_path13 = dir_path + "\\mysettings\\refresh_time\\refresh_time.txt"

                if os.path.isdir(dir_path) == False:
                    print('디렉토리 존재하지 않음')
                    os.makedirs(dir_path)

                ######################

                ######################

                with open(file_path3, "r", encoding='utf-8-sig') as file:
                    lines = file.read().split('\n')
                    # lines = ' '.join(lines).split()

                    isSchedule_ = False
                    while isSchedule_ is False:
                        if lines == [] or lines == "":
                            print("스케쥴이 비었다 : myQuest_play_check")
                            with open(file_path3, "r", encoding='utf-8-sig') as file:
                                schedule_ready = file.read()
                            with open(file_path, "w", encoding='utf-8-sig') as file:
                                file.write(schedule_ready)
                            with open(file_path, "r", encoding='utf-8-sig') as file:
                                lines = file.read().split('\n')
                                # lines = ' '.join(lines).split()
                        else:
                            isSchedule_ = True
                    # 표 수정
                    reset_schedule_ = ""
                    for i in range(len(lines)):
                        if i == is_row:
                            print("삭제된것")
                        else:
                            reset_schedule_ += lines[i] + "\n"

                    print('reset_schedule_표 수정', reset_schedule_)
                    with open(file_path3, "w", encoding='utf-8-sig') as file:
                        file.write(reset_schedule_)

                # with open(file_path3, "r", encoding='utf-8-sig') as file:
                #     lines = file.read().split('\n')
                #     lines = ' '.join(lines).split()
                #     # 백업 수정
                #     reset_schedule_ = ""
                #     for i in range(len(lines)):
                #         complete_ = lines[i].split(":")
                #         for j in range(len(complete_)):
                #             if j < 3:
                #                 reset_schedule_ += complete_[j] + ":"
                #             if j == 3:
                #                 reset_schedule_ += '대기중:'
                #             if 3 < j < 7:
                #                 reset_schedule_ += complete_[j] + ":"
                #             if j == 7:
                #                 reset_schedule_ += '대기중\n'
                #
                #     print('reset_schedule_백업 수정', reset_schedule_)
                #     with open(file_path3, "w", encoding='utf-8-sig') as file:
                #         file.write(reset_schedule_)

                #######################################################

                isRefresh = False
                while isRefresh is False:
                    if os.path.isfile(file_path13) == True:
                        with open(file_path13, "r", encoding='utf-8-sig') as file:
                            refresh_time = file.read()
                            refresh_time_bool = refresh_time.isdigit()
                            if refresh_time_bool == True:
                                isRefresh = True
                                print("refresh_time", refresh_time)
                            else:
                                with open(file_path13, "w", encoding='utf-8-sig') as file:
                                    file.write(str(4))
                    else:
                        with open(file_path13, "w", encoding='utf-8-sig') as file:
                            file.write(str(4))

                # with open(file_path3, "r", encoding='utf-8-sig') as file:
                #     lines = file.read()
                #     # lines = file.read().split('\n')
                #     print('line_refresh', lines)
                # with open(file_path, "w", encoding='utf-8-sig') as file:
                #     file.write(lines)

                with open(file_path, "r", encoding='utf-8-sig') as file:
                    lines = file.read()

                ############################################################

                nowDay_ = datetime.today().strftime("%Y%m%d")
                nowDay = int(nowDay_)
                nowTime = int(datetime.today().strftime("%H"))
                yesterday_ = date.today() - timedelta(1)
                yesterday = int(yesterday_.strftime('%Y%m%d'))

                if nowTime >= int(refresh_time):
                    nowDay = str(nowDay)
                else:
                    nowDay = yesterday
                    nowDay = str(nowDay)
                with open(file_path2, "w", encoding='utf-8-sig') as file:
                    file.write(str(nowDay) + ":" + str(refresh_time) + "\n")

                remove_ = self.tableWidget.rowCount()
                print("remove_", remove_)
                for i in range(remove_ - 1):
                    self.tableWidget.removeRow(0)

                refresh_result = lines.split("\n")
                rowcount = self.tableWidget.rowCount()
                print("refresh_rowcount", self.tableWidget.rowCount())
                count_ = len(refresh_result) - rowcount - 1
                for i in range(count_):
                    self.tableWidget.insertRow(self.tableWidget.rowCount())
                print("refresh_rowcount2", self.tableWidget.rowCount())
                self.set_rand_int()
            else:
                print("해당 스케쥴을 클릭해라")
        except Exception as e:
            print(e)
            return 0


    def prompt_refresh(self):
        try:
            ##############초기화

            v_.one_cla_count = 0
            v_.two_cla_count = 0
            v_.one_cla_ing = 'check'
            v_.two_cla_ing = 'check'

            v_.dead_count = 0

            # myQuest_number_check('all', 'refresh')

            dir_path = "C:\\my_games\\" + str(v_.game_folder)
            file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
            file_path2 = dir_path + "\\mysettings\\refresh_time\\quest.txt"
            file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
            file_path13 = dir_path + "\\mysettings\\refresh_time\\refresh_time.txt"

            if os.path.isdir(dir_path) == False:
                print('디렉토리 존재하지 않음')
                os.makedirs(dir_path)

            isRefresh = False
            while isRefresh is False:
                if os.path.isfile(file_path13) == True:
                    with open(file_path13, "r", encoding='utf-8-sig') as file:
                        refresh_time = file.read()
                        refresh_time_bool = refresh_time.isdigit()
                        if refresh_time_bool == True:
                            isRefresh = True
                            print("refresh_time", refresh_time)
                        else:
                            with open(file_path13, "w", encoding='utf-8-sig') as file:
                                file.write(str(4))
                else:
                    with open(file_path13, "w", encoding='utf-8-sig') as file:
                        file.write(str(4))

            with open(file_path3, "r", encoding='utf-8-sig') as file:
                lines = file.read()
                # lines = file.read().split('\n')
                print('line_refresh', lines)
            with open(file_path, "w", encoding='utf-8-sig') as file:
                file.write(lines)

            nowDay_ = datetime.today().strftime("%Y%m%d")
            nowDay = int(nowDay_)
            nowTime = int(datetime.today().strftime("%H"))
            yesterday_ = date.today() - timedelta(1)
            yesterday = int(yesterday_.strftime('%Y%m%d'))

            if nowTime >= int(refresh_time):
                nowDay = str(nowDay)
            else:
                nowDay = yesterday
                nowDay = str(nowDay)
            with open(file_path2, "w", encoding='utf-8-sig') as file:
                file.write(str(nowDay) + ":" + str(refresh_time) + "\n")

            remove_ = self.tableWidget.rowCount()
            print("remove_", remove_)
            for i in range(remove_ - 1):
                self.tableWidget.removeRow(0)

            refresh_result = lines.split("\n")
            rowcount = self.tableWidget.rowCount()
            print("refresh_result", refresh_result)
            print("len(refresh_result)", len(refresh_result))
            print("rowcount", rowcount)
            print("refresh_rowcount", self.tableWidget.rowCount())
            count_ = len(refresh_result) - rowcount - 1
            for i in range(count_):
                self.tableWidget.insertRow(self.tableWidget.rowCount())
            print("refresh_rowcount2", self.tableWidget.rowCount())
            self.set_rand_int()

        except Exception as e:
            print(e)
            return 0


    def prompt_refresh_all(self):
        try:
            ##############초기화

            v_.one_cla_count = 0
            v_.two_cla_count = 0
            v_.one_cla_ing = 'check'
            v_.two_cla_ing = 'check'

            v_.dead_count = 0

            # myQuest_number_check('all', 'refresh')

            dir_path = "C:\\my_games\\" + str(v_.game_folder)
            file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
            file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
            file_path_all = dir_path + "\\mysettings\\myschedule\\sta.txt"

            if os.path.isdir(dir_path) == False:
                print('디렉토리 존재하지 않음')
                os.makedirs(dir_path)


            with open(file_path_all, "r", encoding='utf-8-sig') as file:
                lines = file.read()
                print('line_refresh', lines)
                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write(lines)
                with open(file_path3, "w", encoding='utf-8-sig') as file:
                    file.write(lines)


            remove_ = self.tableWidget.rowCount()
            print("remove_", remove_)
            for i in range(remove_ - 1):
                self.tableWidget.removeRow(0)

            refresh_result = lines.split("\n")
            rowcount = self.tableWidget.rowCount()
            print("refresh_result", refresh_result)
            print("len(refresh_result)", len(refresh_result))
            print("rowcount", rowcount)
            print("refresh_rowcount", self.tableWidget.rowCount())
            count_ = len(refresh_result) - rowcount - 1
            for i in range(count_):
                self.tableWidget.insertRow(self.tableWidget.rowCount())
            print("refresh_rowcount2", self.tableWidget.rowCount())
            self.set_rand_int()

        except Exception as e:
            print(e)
            return 0


    def prompt_change_one(self, text):

        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
        file_path2 = dir_path + "\\mysettings\\refresh_time\\quest.txt"
        file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
        file_path13 = dir_path + "\\mysettings\\refresh_time\\refresh_time.txt"

        try:
            ##############프롬프트 변경
            print("thisValue", thisValue)
            print("thisCol", thisCol)
            print("thisRow", thisRow)

            is_prompt = "- " + self.require_prompt.text() + "\n"

            if thisValue != "none":



                v_.one_cla_count = 0
                v_.two_cla_count = 0
                v_.one_cla_ing = 'check'
                v_.two_cla_ing = 'check'

                v_.dead_count = 0

                # myQuest_number_check('all', 'refresh')



                if os.path.isdir(dir_path) == False:
                    print('디렉토리 존재하지 않음')
                    os.makedirs(dir_path)

                ######################

                ######################

                with open(file_path, "r", encoding='utf-8-sig') as file:
                    lines = file.read().split('\n')
                    # lines = ' '.join(lines).split()

                    isSchedule_ = False
                    while isSchedule_ is False:
                        if lines == [] or lines == "":
                            print("스케쥴이 비었다 : myQuest_play_check")
                            with open(file_path3, "r", encoding='utf-8-sig') as file:
                                schedule_ready = file.read()
                            with open(file_path, "w", encoding='utf-8-sig') as file:
                                file.write(schedule_ready)
                            with open(file_path, "r", encoding='utf-8-sig') as file:
                                lines = file.read().split('\n')
                        else:
                            isSchedule_ = True
                    # 표 수정
                    reset_schedule_ = ""


                    for i in range(len(lines)):

                        if i == thisRow - 1:
                            reset_schedule_ += is_prompt
                        elif lines[i] == "":
                            reset_schedule_ += lines[i]
                        else:
                            reset_schedule_ += lines[i] + "\n"



                    print('reset_schedule_표 수정', reset_schedule_)
                    with open(file_path, "w", encoding='utf-8-sig') as file:
                        file.write(reset_schedule_)
                    with open(file_path3, "w", encoding='utf-8-sig') as file:
                        file.write(reset_schedule_)



                #######################################################

                isRefresh = False
                while isRefresh is False:
                    if os.path.isfile(file_path13) == True:
                        with open(file_path13, "r", encoding='utf-8-sig') as file:
                            refresh_time = file.read()
                            refresh_time_bool = refresh_time.isdigit()
                            if refresh_time_bool == True:
                                isRefresh = True
                                print("refresh_time", refresh_time)
                            else:
                                with open(file_path13, "w", encoding='utf-8-sig') as file:
                                    file.write(str(4))
                    else:
                        with open(file_path13, "w", encoding='utf-8-sig') as file:
                            file.write(str(4))

                with open(file_path, "r", encoding='utf-8-sig') as file:
                    lines = file.read()

                ############################################################

                nowDay_ = datetime.today().strftime("%Y%m%d")
                nowDay = int(nowDay_)
                nowTime = int(datetime.today().strftime("%H"))
                yesterday_ = date.today() - timedelta(1)
                yesterday = int(yesterday_.strftime('%Y%m%d'))

                if nowTime >= int(refresh_time):
                    nowDay = str(nowDay)
                else:
                    nowDay = yesterday
                    nowDay = str(nowDay)
                with open(file_path2, "w", encoding='utf-8-sig') as file:
                    file.write(str(nowDay) + ":" + str(refresh_time) + "\n")

                remove_ = self.tableWidget.rowCount()
                print("remove_", remove_)
                for i in range(remove_ - 1):
                    self.tableWidget.removeRow(0)

                refresh_result = lines.split("\n")
                rowcount = self.tableWidget.rowCount()
                print("refresh_rowcount", self.tableWidget.rowCount())
                count_ = len(refresh_result) - rowcount - 1
                for i in range(count_):
                    self.tableWidget.insertRow(self.tableWidget.rowCount())
                print("refresh_rowcount2", self.tableWidget.rowCount())
                self.set_rand_int()
            else:
                print("해당 스케쥴을 클릭해라")
        except Exception as e:
            print(e)
            return 0


    def mySchedule_add(self, data):
        try:
            print("...........mySchedule_add...........", data)
            schedule_add = False
            how_ = 'add'
            datas = str(data)
            result = self.mySchedule_change(how_, datas)
            result = self.mySchedule_change2(how_, datas)
            print("added_", result)
            if result == True:
                schedule_add = True
                self.mystatus_refresh()
                print('스케쥴 추가 됨')

            return schedule_add
        except Exception as e:
            print(e)
            return 0

    def mySchedule_change(self, how_, datas):
        try:
            print("mySchedule_change", datas)
            ishow_ = False
            dir_path = "C:\\my_games\\" + str(v_.game_folder)
            file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
            file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"
            print(os.path.isfile(file_path))
            print(os.path.isdir(dir_path))

            if os.path.isdir(dir_path) == True:
                print('디렉토리 존재')
            else:
                os.makedirs(dir_path)

            print("how_", how_)
            if how_ == "add":
                with open(file_path, "a", encoding='utf-8-sig') as file:
                    print("mySchedule_change_add????", datas)
                    file.write(datas)
                    ishow_ = True
                self.set_rand_int()

            elif how_ == "modify":

                with open(file_path, "w", encoding='utf-8-sig') as file:
                    file.write(datas)

                    ishow_ = True
                self.set_rand_int()

            return ishow_
        except Exception as e:
            print(e)
            return 0

    def mySchedule_change2(self, how_, datas):
        # row:

        dir_path = "C:\\my_games\\" + str(v_.game_folder)
        file_path = dir_path + "\\mysettings\\myschedule\\schedule.txt"
        file_path3 = dir_path + "\\mysettings\\myschedule\\schedule2.txt"

        try:
            print("mySchedule_change2", datas)
            ishow_ = False

            print(os.path.isfile(file_path))
            print(os.path.isdir(dir_path))

            if os.path.isdir(dir_path) == True:
                print('디렉토리 존재')
            else:
                os.makedirs(dir_path)

            print("mySchedule_change2 : how_", how_)
            if how_ == "add":
                with open(file_path3, "a", encoding='utf-8-sig') as file:
                    print("mySchedule_change2_add????", datas)
                    file.write(datas)
                    ishow_ = True

                self.set_rand_int()

            elif how_ == "modify":

                # 잠김

                with open(file_path3, "w", encoding='utf-8-sig') as file:
                    file.write(datas)
                    ishow_ = True

                self.set_rand_int()

            return ishow_
        except Exception as e:
            print(e)
            return 0


    def hello2(self):
        print("hello!!!!!!!!!!")

    def mytestin_(self):
        try:
            x = Test_check(self)
            # self.mytestin.setText("GootEvening")
            # self.mytestin.setDisabled(True)
            x.start()
        except Exception as e:
            print(e)
            return 0

    # def keyPressEvent(self, e):
    #     if e.key() == Qt.Key_Escape:
    #         self.close()
    #     elif e.key() == Qt.Key_F:
    #         self.showFullScreen()
    #     elif e.key() == Qt.Key_N:
    #         self.showNormal()


######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################


###########BackGround(백그라운드) 관련############################nowtest


class Test_check(QThread):

    # parent = MainWidget을 상속 받음.
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        # self.parent.hello2()

        # cla = "one"

        print("여긴 테스트 모드(ver " + version + ")")
        go_test(v_.keyword)






class temporary_upload(QThread):



    # parent = MainWidget을 상속 받음.
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.keyword = None  # 전달 받을 키워드 변수

    def set_keyword(self, keyword):
        self.keyword = keyword

    def run(self):
        from life_tips import life_tips_keyword

        print("임시블로그 업로드(ver " + version + ")")
        print("전달 받은 키워드:", self.keyword)
        life_tips_keyword(self.keyword)




class Monitoring_one(QThread):
    # def __init__(self, parent):
    #     super().__init__(parent)
    #     self.parent = parent
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            print("monitoring start")
            line_monitor(str(v_.game_folder), "one")
        except Exception as e:
            print(e)
            return 0

class Monitoring_two(QThread):
    # def __init__(self, parent):
    #     super().__init__(parent)
    #     self.parent = parent
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            print("monitoring start")
            line_monitor(str(v_.game_folder), "two")
        except Exception as e:
            print(e)
            return 0

class Monitoring_three(QThread):
    # def __init__(self, parent):
    #     super().__init__(parent)
    #     self.parent = parent
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            print("monitoring start")
            line_monitor(str(v_.game_folder), "three")
        except Exception as e:
            print(e)
            return 0

class Monitoring_four(QThread):
    # def __init__(self, parent):
    #     super().__init__(parent)
    #     self.parent = parent
    def __init__(self):
        super().__init__()

    def run(self):
        try:
            print("monitoring start")
            line_monitor(str(v_.game_folder), "four")
        except Exception as e:
            print(e)
            return 0

class game_Playing_Ready(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            # v_.now_cla = 'none' <= 최초 부를때 자동으로 불러옴. 또는 실행하여 바꿀수 있음. 오딘은 그냥 설정해줘야함.

            # self.m_ = Monitoring_one()
            # self.m_.start()
            print("game_Playing_Ready")
            self.x_ = game_Playing()
            self.x_.start()
        except Exception as e:
            print(e)
            return 0

class game_Playing_onecla(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
            file_path = dir_path + "\\start.txt"

            with open(file_path, "w", encoding='utf-8-sig') as file:
                data = 'yes'
                file.write(str(data))

            v_.now_cla = 'one' # <= 오딘 제외하고 1클라 돌리는 게임은 주석 처리.

            self.m_ = Monitoring_one()
            self.m_.start()


        except Exception as e:
            print(e)
            return 0


class game_Playing_twocla(QThread):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
            file_path = dir_path + "\\start.txt"

            with open(file_path, "w", encoding='utf-8-sig') as file:
                data = 'yes'
                file.write(str(data))


            v_.now_cla = 'two' # <= 오딘 제외하고 1클라 돌리는 게임은 주석 처리.

            self.m_ = Monitoring_two()
            self.m_.start()

        except Exception as e:
            print(e)
            return 0

class game_Playing_threecla(QThread):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
            file_path = dir_path + "\\start.txt"

            with open(file_path, "w", encoding='utf-8-sig') as file:
                data = 'yes'
                file.write(str(data))


            v_.now_cla = 'three' # <= 오딘 제외하고 1클라 돌리는 게임은 주석 처리.

            self.m_ = Monitoring_three()
            self.m_.start()

        except Exception as e:
            print(e)
            return 0

class game_Playing_fourcla(QThread):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
            file_path = dir_path + "\\start.txt"

            with open(file_path, "w", encoding='utf-8-sig') as file:
                data = 'yes'
                file.write(str(data))


            v_.now_cla = 'four' # <= 오딘 제외하고 1클라 돌리는 게임은 주석 처리.

            self.m_ = Monitoring_four()
            self.m_.start()

        except Exception as e:
            print(e)
            return 0

class game_Playing_fivecla(QThread):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
            file_path = dir_path + "\\start.txt"

            with open(file_path, "w", encoding='utf-8-sig') as file:
                data = 'yes'
                file.write(str(data))


            v_.now_cla = 'five' # <= 오딘 제외하고 1클라 돌리는 게임은 주석 처리.

            self.m_ = Monitoring_four()
            self.m_.start()

        except Exception as e:
            print(e)
            return 0

class game_Playing_sixcla(QThread):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            dir_path = "C:\\my_games\\load\\" + str(v_.game_folder)
            file_path = dir_path + "\\start.txt"

            with open(file_path, "w", encoding='utf-8-sig') as file:
                data = 'yes'
                file.write(str(data))


            v_.now_cla = 'six' # <= 오딘 제외하고 1클라 돌리는 게임은 주석 처리.

            self.m_ = Monitoring_four()
            self.m_.start()

        except Exception as e:
            print(e)
            return 0


# 실제 게임 플레이 부분 #################################################################
################################################
################################################


class game_Playing(QThread):

    def __init__(self):
        super().__init__()
        # self.parent = parent

        self.isCheck = True

    def run(self):

        import sys
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtTest import QTest
        import random
        from life_tips import life_tips_keyword
        from trend_search_page import collect_all_topics, filter_topics_by_category

        try:
            print("game_Playing")
            print(str(v_.game_folder))

            while self.isCheck is True:


                # print("게임 실행 모드(ver " + version + ")")
                # print("now_arduino", v_.now_arduino)
                # result_game = game_start()
                # if result_game == True:
                print("자동발행 시작")

                result_suggest = False

                random_topic = random.randint(1, 2)
                print("random_topic", random_topic)

                if random_topic == 1:

                    result_suggest = suggest_life_tip_topic()
                    print("result_suggest", result_suggest)

                else:
                    topic_list = collect_all_topics()

                    filtered_topics = filter_topics_by_category(topic_list)

                    print("\n🔷 최종 필터링된 블로그 키워드:", filtered_topics)
                    if len(filtered_topics) > 0:
                        result_suggest = True
                        life_tips_keyword(filtered_topics)
                    else:
                        print("없..................")

                if result_suggest == True:

                    # QTest.qWait(18000000)


                    total_minutes = 300  # 총 5시간 = 300분
                    interval_minutes = 5
                    interval_ms = interval_minutes * 60 * 1000  # 5분 = 300,000ms

                    print("⏳ 대기 시작: 총 5시간 (300분)\n")

                    for i in range(1, (total_minutes // interval_minutes) + 1):
                        QTest.qWait(interval_ms)

                        elapsed_minutes = i * interval_minutes
                        remaining_minutes = total_minutes - elapsed_minutes

                        # 특수 알림 강조 (5, 10, 15분 구간)
                        if elapsed_minutes in [5, 10, 15]:
                            print(f"⭐️ {elapsed_minutes}분 경과 / ⏱️ 남은 시간: {remaining_minutes}분")
                        else:
                            print(f"⌛ {elapsed_minutes}분 경과 / ⏱️ 남은 시간: {remaining_minutes}분")

                    print("\n✅ 대기 완료: 총 5시간(300분) 경과!")

                else:
                    # QTest.qWait(600000)
                    total_minutes = 5
                    for i in range(1, total_minutes + 1):
                        QTest.qWait(60 * 1000)  # 1분 = 60,000ms
                        passed = i
                        remaining = total_minutes - i
                        print(f"⏱️ {passed}분 지남 | ⏳ 남은 시간: {remaining}분")

                    print("✅ 5분 대기 완료!")



        except Exception as e:
            print(e)
            os.system("pause")
            return 0

####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    # sys.exit(1)


# if __name__ == '__main__':
#     try:
#         app = QApplication(sys.argv)
#         ex = MyApp()
#
#         # Back up the reference to the exceptionhook
#         sys._excepthook = sys.excepthook
#
#         # Set the exception hook to our wrapping function
#         sys.excepthook = my_exception_hook
#
#         sys.exit(app.exec_())
#     except Exception as e:
#         print(e)
#         print("프로그램 꺼지기전 정지")
#         os.system("pause")
