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
    from env_ai import wp_id, wp_ps, keys
    from life_tips import life_tips_keyword, check_openai_ready, suggest_life_tip_topic
    from trend_search_page import trend_search

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

        print("v_.my_prompt", v_.my_prompt)

        print(sys.executable)

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


def post_test():
    from env_ai import wp_id, wp_ps
    from wordpress_xmlrpc import Client, WordPressPost
    from wordpress_xmlrpc.methods.posts import NewPost

    try:
        print("▶ post_test 시작")

        username = wp_id()
        password = wp_ps()
        site_url = "https://hobbycolorful.com/xmlrpc.php"

        # 1) 클라이언트 생성
        client = Client(site_url, username, password)

        # 2) 포스트 객체 생성
        post = WordPressPost()

        # 📰 제목·본문 설정
        post.title       = "여기는 글의 제목입니다"
        post.content     = "여기는 글의 내용입니다"
        post.post_status = "publish"  # 공개 발행

        # 🎯 카테고리 지정 (카테고리 이름 그대로, 괄호 포함)
        post.terms_names = {
            'category': ['HobbyWhite(뉴스)']
        }

        # 3) 포스트 업로드
        client.call(NewPost(post))
        print("✅ 포스팅이 HobbyWhite(뉴스) 카테고리에 업로드 되었습니다.")

    except Exception as e:
        print("❌ 오류 발생:", e)

def naver_news():
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


        print("네이버 경제 뉴스")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # 1. 구글 뉴스에서 "네이버 경제" 관련 기사 검색
        query = "네이버 경제 site:news.naver.com"
        google_news_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=nws&hl=ko"

        res = requests.get(google_news_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # 2. 구글 링크에서 실제 네이버 뉴스 주소만 추출
        def extract_real_url(google_href):
            match = re.search(r"/url\?q=(https?://[^&]+)", google_href)
            if match:
                return urllib.parse.unquote(match.group(1))
            return None

        article_links = []
        for a in soup.select("a[href^='/url?q=']"):
            real_url = extract_real_url(a.get("href"))
            if real_url and "news.naver.com" in real_url:
                article_links.append(real_url)

        article_links = list(set(article_links))[:5]  # 상위 5개만

        print("✅ 정제된 네이버 뉴스 링크:")
        for link in article_links:
            print(link)

        # 3. 각 기사에서 제목/본문/GPT 요약 추출
        results = []

        for url in article_links:
            try:
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, "html.parser")

                # 제목 추출
                title_tag = soup.select_one("h2#title_area span")
                title = title_tag.text.strip() if title_tag else "제목 없음"

                # 본문 추출
                content_tag = soup.select_one("#dic_area")
                if not content_tag:
                    print(f"❌ 본문 없음: {url}")
                    continue

                content = content_tag.get_text(separator=" ", strip=True)
                content = re.sub(r"\s+", " ", content)

                # 간단한 GPT 스타일 요약 생성 (룰 기반)
                summary = f"이 기사는 '{title}'에 대한 내용으로, 주요 경제 이슈는 다음과 같습니다:\n"
                if "금리" in content or "인상" in content:
                    summary += "📈 금리 정책이 주요 쟁점이며, 중앙은행의 결정이 금융시장에 영향을 미치고 있습니다."
                elif "물가" in content or "인플레이션" in content:
                    summary += "💹 인플레이션과 물가 변화가 핵심 이슈로, 소비자 경제에 중요한 영향을 미치고 있습니다."
                elif "환율" in content:
                    summary += "💱 환율 변동이 글로벌 무역과 수출입에 미치는 영향이 분석되고 있습니다."
                elif "무역" in content or "수출" in content:
                    summary += "🚢 무역수지와 수출입 변화가 거시경제에 주는 영향을 다루고 있습니다."
                else:
                    summary += "📊 다양한 경제 지표와 정책 변화가 논의되고 있으며, 향후 시장 흐름이 주목됩니다."

                # 결과 저장
                results.append({
                    "title": title,
                    "summary": summary,
                    "content": content
                })

                print(f"✅ '{title}' 기사 요약 완료")

            except Exception as e:
                print(f"❌ 오류 발생: {e}")

        # 4. 출력
        print(f"\n📦 최종 수집된 뉴스 개수: {len(results)}")
        for i, r in enumerate(results, 1):
            print(f"\n📰 뉴스 {i}")
            print(f"제목: {r['title']}")
            print(f"\n✏️ 요약:\n{r['summary']}")
            print(f"\n📄 본문:\n{r['content'][:500]}...")

    except Exception as e:
        print(e)

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


def openai_api_test__():

    from openai import OpenAI
    from dotenv import load_dotenv
    from env_ai import keys

    client = OpenAI(api_key = keys())
    load_dotenv()


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


        print("Opneai")

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": "너는 누구야?"
                }
            ]
        )

        print(completion.choices[0].message.content)

    except Exception as e:
        print(e)

