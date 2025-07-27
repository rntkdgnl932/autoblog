# * QTabWidget 탭에 다양한 위젯 추가
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QColor       #아이콘
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtTest import *

import os
import time
from datetime import datetime
import random
import os.path
from datetime import date, timedelta
import re
import git

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
import screeninfo
from bs4 import BeautifulSoup
# import keyboard
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client, WordPressPost
import slugify as unicode_slugify
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from openai import OpenAI


# 패키지 다운 불필요
import tkinter
import webbrowser
import colorthief
import ctypes
import shutil
import serial
import pydirectinput
import sys


sys.path.append('C:/my_games/auto_blog/data_basic/mymodule')

# 나의 모듈 모두 표시해야함
# from function import imgs_set, imgs_set_, click_pos_2, random_int, text_check_get_3, int_put_, text_check_get, \
#     click_with_image, drag_pos, image_processing, get_region, click_pos_reg
from function_game import imgs_set, imgs_set_, click_pos_2, random_int, text_check_get_3, int_put_, text_check_get, click_with_image, drag_pos, image_processing, get_region, click_pos_reg


from massenger import line_monitor
from schedule import myQuest_play_check, myQuest_play_add
from PIL import ImageGrab
from functools import partial

from test_ import go_test

import variable as v_
print("v_.game_folder", v_.game_folder)
print("v_.data_folder", v_.data_folder)
sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')

sys.setrecursionlimit(10 ** 7)
# pyqt5 관련###################################################
rowcount = 0
colcount = 0
thisRow = 0
thisCol = 0
table_datas = ""
#  onCollection= False
onCharacter = 0
onRefresh_time = 0
onDunjeon = "none"
onDunjeon_level = 0
onHunt = "none"
onHunt2 = "none"
onHunt3 = "none"
onMaul = "none"

isgloballoop = False

# 기존 오토모드 관련###############################################


pyautogui.FAILSAFE = False
####################################################################################################################
# pytesseract.pytesseract.tesseract_cmd = R'E:\workspace\pythonProject\Tesseract-OCR\tesseract'
pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract'
from PyQt5.QtWidgets import *
import sys

import main_p

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')

import os.path

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = main_p.MyApp()

        # Back up the reference to the exceptionhook
        sys._excepthook = sys.excepthook

        # Set the exception hook to our wrapping function
        sys.excepthook = main_p.my_exception_hook

        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        print("프로그램 꺼지기전 정지")
        os.system("pause")
