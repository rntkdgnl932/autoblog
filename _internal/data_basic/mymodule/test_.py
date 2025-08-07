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
    from redesign_existing_posts import redesign_posts_by_category_restapi
    from gas_start import get_gemini_response

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

        # redesign_all_recent_posts()

        blogger_prompt = """
            [역할]
            당신은 최신 정부 정책을 일반인들이 이해하기 쉽게 설명해주는 '워드프레스 전문 블로거'입니다.
            독자들의 흥미를 끌 수 있도록 제목을 붙이고, 친근하면서도 전문적인 어조로 글을 작성해주세요.

            [요청]
            '민생회복 소비쿠폰'에 대한 블로그 포스팅 초안을 작성해주세요. 아래 내용을 포함해주세요.
            - 정책의 도입 배경
            - 쿠폰 사용처 및 사용 방법
            - 신청 자격 및 방법
            - 예상되는 기대 효과
            - 신청 자격에 따른 신청 금액
            """

        print("🤖 제미나이에게 블로그 포스팅 초안 작성을 요청합니다...")
        print("-" * 40)

        # 함수 호출
        blog_post_draft = get_gemini_response(blogger_prompt)

        # 결과 출력
        print(blog_post_draft)






    except Exception as e:
        print(e)

# # ✅ GPT로 소제목별 본문 생성
#     new_body = []
#     for section in sections:
#         h2 = section[0]
#         h2_text = h2.get_text(strip=True)
#
#         system_message = (
#             "당신은 정부 정책, 지원금, 제도 정보를 전문적으로 안내하는 공공기관 블로그 콘텐츠 작성 전문가입니다. "
#             "절대 허위 정보를 생성하지 않으며, 전화번호나 웹사이트 주소는 존재하는 공식 정보만 사용합니다. "
#             "AI 스타일의 흔적을 남기지 않고, 자연스럽고 신뢰감 있는 공공 콘텐츠를 생성합니다."
#         )
#
#         prompt = f"""
#         📌 [콘텐츠 작성 목적]
#         - '{keyword}' 주제의 소제목 항목 '{h2_text}'에 대한 블로그 콘텐츠 본문을 작성합니다.
#
#         📌 [출력 형식 및 문법 규칙]
#         - 출력은 반드시 **HTML 형식**만 사용 (※ Markdown 문법 `###`, `**` 등 절대 사용 금지)
#         - `<h2>` 태그는 절대 포함하지 마세요. 본문 내용만 출력합니다.
#         - 소제목 본문 중 추가 단락 구분이 필요할 경우에만 `<h3>` 태그를 사용하되, **중복이나 형식적 사용 금지**
#         - `<h3>` 제목은 최대 2~3개까지만 사용하고, **반드시 서로 다른 표현**으로 구성
#         - 강조는 `<strong>` 태그만 사용 (Markdown `**` 금지)
#         - `<ul>` 또는 `<table>` 구조를 최소 1회 이상 포함하여 시각적으로 요약 제공
#         - `<a>` 태그는 **중첩 없이 단독 사용**, 동일 문장 내 반복 금지
#
#         📌 [정보 분류 및 구성 규칙]
#         - ‘신청’, ‘조건’, ‘주의’ 등의 항목을 기계적으로 나누지 말고, **정보의 의미에 따라 하위 구성을 자연스럽게 결정**하세요.
#             - 예: ‘신청 절차’라는 표현 대신 → ‘모바일로 신청하는 방법’, ‘지자체별 접수 차이’ 등 **문맥 기반 제목** 사용
#         - 하위 문단은 다음 중 하나 이상의 기준으로 구분:
#             - 대상별(연령, 소득, 거주지 등)
#             - 신청 방식별(온라인/오프라인, 앱/서류 등)
#             - 유사 정책 간 비교 또는 혼동 사례
#             - 실제 지원 사례 또는 신청 시 실수 사례
#         - 반복 문단은 반드시 제거하며, **같은 의미의 메시지는 한 번만 강조**하세요.
#
#         📌 [정보 정확도 및 SEO 최적화 기준]
#         - 본문에는 다음 중 **최소 3개 이상** 포함되어야 함:
#             - 제도명, 운영 기관명(실명)
#             - 구체적 수치 (예: 소득 기준, 연령 제한)
#             - 실제 신청 가능 링크 (`<a href="..." target="_blank" rel="noopener">`)
#             - 표 또는 목록을 활용한 시각 정보 정리
#             - <strong>을 활용한 키워드 강조 (문맥 기반)
#         - SEO 최적화를 위해 키워드는 자연스럽게 삽입하되, **과도한 반복 없이** 문맥에 맞게 활용
#
#         📌 [참조 링크 작성 규칙]
#         - 본문 끝에만 1회, 다음 형식으로 삽입:
#           `<p>참조: <a href="https://도메인" target="_blank" rel="noopener">기관명</a>, <a href="https://도메인" target="_blank" rel="noopener">기관명</a></p>`
#         - 같은 문구 반복 또는 "자세한 사항은 홈페이지 참조" 등의 문장은 사용 금지
#
#         📌 [최신성 및 제한 조건]
#         - 콘텐츠는 오늘 기준({today}) 최신 정보로 작성해야 하며,
#         - {this_year}년 이전 종료된 정책이나 시효가 지난 지원금은 절대 포함하지 마세요.
#         - 정보가 불확실할 경우, 새로운 내용을 생성하지 말고 기존 원문 내용을 정리해 재사용하세요.
#
#         """
#
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[
#                     {"role": "system", "content": system_message},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=0.3
#             )
#             rewritten_html = response.choices[0].message.content.strip()
#         except Exception as e:
#             print(f"❌ GPT 재구성 실패 - {h2_text}: {e}")
#             rewritten_html = f"<p>{h2_text} 관련 내용을 준비하지 못했습니다.</p>"
#
#         new_body.append("\n" + str(h2))
#         new_body.append("\n" + rewritten_html)

