import sys
import os
import time
import requests
from PyQt5.QtTest import *
import variable as v_

sys.path.append('C:/my_games/' + str(v_.game_folder) + '/' + str(v_.data_folder) + '/mymodule')

my_newsapi = "ad1a0e63885745ffbee8a5258bda298a"


def go_test(keyword):
    import numpy as np
    import cv2
    import pyautogui
    import random
    from bs4 import BeautifulSoup
    import re
    import requests
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    from bs4 import BeautifulSoup
    import time
    import requests
    import re
    import urllib.parse
    from life_tips import life_tips_keyword, check_openai_ready, suggest_life_tip_topic
    from trend_search_page import get_zum_ai_issue_trends, get_google_trending_keywords, get_youtube_trending_titles, \
        fetch_health_titles, collect_all_topics, filter_topics_by_category, search_naver_blog_top_post
    from organization_info import scan_internet

    try:
        print("test")
        cla = "one"

        plus = 0


        if cla == "one":
            plus = 0
        elif cla == "two":
            plus = 960
        elif cla == "three":
            plus = 960 * 2
        elif cla == "four":
            plus = 960 * 3
        elif cla == "five":
            plus = 960 * 4
        elif cla == "six":
            plus = 960 * 5

        search_naver_blog_top_post("전기요금 할인 제도")







    except Exception as e:
        print(e)



