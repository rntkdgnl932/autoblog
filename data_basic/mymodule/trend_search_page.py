def get_zum_ai_issue_trends():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from bs4 import BeautifulSoup
    import time

    keywords = []
    try:
        options = Options()
        options.add_argument('--headless')  # 필요 시 주석 처리
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://zum.com/")
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 모든 이슈 키워드 추출
        keyword_spans = soup.select("span.issue-word-list__keyword")
        for span in keyword_spans:
            text = span.text.strip()
            if text:
                keywords.append(text)

        driver.quit()
    except Exception as e:
        print("⚠️ ZUM AI 이슈 트렌드 오류:", e)
    return keywords


    # 답 받기
    # ai_keywords = get_zum_ai_issue_trends()
    # print("▶ ZUM AI 이슈 트렌드:")
    # for i, kw in enumerate(ai_keywords, 1):
    #     print(f"{i}. {kw}")


def get_google_trending_keywords():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    import time

    keywords = []

    try:
        options = Options()
        # headless로 실행하고 싶다면 아래 줄을 활성화
        # options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://trends.google.co.kr/trends/trendingsearches/daily?geo=KR")
        time.sleep(5)

        # ✅ 핵심: 모든 <div class="mZ3RIc"> 요소 추출
        elements = driver.find_elements(By.CSS_SELECTOR, 'div.mZ3RIc')

        print("\n▶ Google 급상승 키워드:")
        for i, el in enumerate(elements[:20], 1):
            text = el.text.strip()
            if text:
                print(f"{i}. {text}")
                keywords.append(text)

        driver.quit()
    except Exception as e:
        print("⚠️ Google Trends 오류:", e)

    return keywords

    # google_keywords = get_google_trending_keywords()
    # print("▶ Google 급상승 키워드:")
    # for i, kw in enumerate(google_keywords, 1):
    #     print(f"{i}. {kw}")


def get_youtube_trending_titles():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    import time

    titles = []

    try:
        options = Options()
        # options.add_argument('--headless')  # 개발 단계에서는 브라우저 띄우는 것이 좋음
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://www.youtube.com/feed/trending")
        time.sleep(5)

        # 유튜브 트렌드 영상의 제목 선택
        elements = driver.find_elements(By.CSS_SELECTOR, 'a#video-title')

        for el in elements[:20]:  # 상위 20개
            text = el.text.strip()
            if text:
                titles.append(text)

        driver.quit()
    except Exception as e:
        print("⚠️ YouTube Trending 오류:", e)

    return titles







