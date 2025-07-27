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
    from news_economy import news_economy_start
    from drama_review import drama_start
    from life_tips import life_tips_keyword, check_openai_ready, suggest_life_tip_topic
    from trend_search_page import get_zum_ai_issue_trends, get_google_trending_keywords, get_youtube_trending_titles

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


        # suggest_life_tip_topic()

        yt_titles = get_youtube_trending_titles()
        print("▶ YouTube 급상승 영상 제목:")
        for i, title in enumerate(yt_titles, 1):
            print(f"{i}. {title}")


        # trend_search()





    except Exception as e:
        print(e)


def stable_diff():
    import requests
    import base64

    # 1. 이미지 생성 요청
    payload = {
        "prompt": "a fantasy castle at sunset, highly detailed, artstation style",
        "negative_prompt": "blurry, low quality, bad anatomy",
        "steps": 20,
        "width": 512,
        "height": 512,
        "sampler_index": "Euler",
        "cfg_scale": 7.5
    }

    response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)

    # 2. base64 문자열 추출 및 디코딩
    image_base64 = response.json()['images'][0]
    image_data = base64.b64decode(image_base64)

    # 3. PNG 이미지로 저장
    with open("output.png", "wb") as f:
        f.write(image_data)

    print("✅ 이미지 저장 완료: output.png")

    #############################################
#
def check_quota():
    import openai
    try:
        usage = openai.API().usage()  # 실제 quota 확인은 OpenAI Dashboard API로 구현 필요
        print(f"🔎 사용량 진단: {usage}")
    except Exception as e:
        print(f"⚠️ 사용량 확인 실패 또는 API 제한: {e}")



def daum_news():
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


        print("다음 경제 뉴스")

        import feedparser

        # ——————————————
        # 1. 연합뉴스TV 경제 RSS 파싱
        # ——————————————
        RSS_URL = "http://www.yonhapnewstv.co.kr/category/news/economy/feed/"
        feed = feedparser.parse(RSS_URL)

        # 정상 응답 확인
        if feed.bozo:
            raise RuntimeError("RSS 파싱 중 오류 발생: 확인이 필요합니다.")

        # 상위 5개 항목 가져오기
        entries = feed.entries[:5]

        # ——————————————
        # 2. 결과 리스트에 제목·링크·설명 저장
        # ——————————————
        results = []
        for entry in entries:
            results.append({
                'title': entry.get('title', '').strip(),
                'url': entry.get('link', '').strip(),
                'description': entry.get('summary', '').strip()
            })

        # ——————————————
        # 3. 결과 출력
        # ——————————————
        print(f"📦 수집된 뉴스 수: {len(results)}\n")
        for i, item in enumerate(results, 1):
            print(f"=== 뉴스 {i} ===")
            print(f"제목       : {item['title']}")
            print(f"링크       : {item['url']}")
            print(f"간략설명   : {item['description']}\n")

    except Exception as e:
        print(e)


