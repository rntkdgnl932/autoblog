import variable as v_

def get_zum_ai_issue_trends():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    from bs4 import BeautifulSoup

    keywords = []
    try:
        options = Options()
        options.add_argument('--headless')  # 필요 시 주석 해제
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://zum.com/")

        # 최대 300초 대기
        WebDriverWait(driver, 300).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.issue-word-list__keyword"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')

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
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager

    keywords = []

    try:
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')  # 필요 시 주석 해제

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://trends.google.co.kr/trends/trendingsearches/daily?geo=KR")

        # 최대 300초 대기
        WebDriverWait(driver, 300).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.mZ3RIc'))
        )

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


def get_youtube_trending_titles(max_results=20, region_code="KR"):
    from googleapiclient.discovery import build

    # 카테고리 ID 및 설명 정의
    category_map = {
        "22": "People & Blogs",
        "26": "Howto & Style",
        "24": "News & Politics"
    }

    all_titles = []

    try:
        youtube = build("youtube", "v3", developerKey=v_.my_google_custom_api)

        for category_id, category_name in category_map.items():
            print(f"\n📌 [{category_name}] 카테고리 영상 추출 중...")

            response = youtube.videos().list(
                part="snippet",
                chart="mostPopular",
                regionCode=region_code,
                maxResults=max_results,
                videoCategoryId=category_id
            ).execute()

            category_titles = []
            for item in response.get("items", []):
                title = item["snippet"]["title"].strip()
                if title:
                    category_titles.append(title)
                    all_titles.append(title)

            for i, t in enumerate(category_titles, 1):
                print(f"{i}. {t}")

    except Exception as e:
        print("⚠️ YouTube API 카테고리 트렌딩 오류:", e)

    return all_titles





    # yt_titles = get_youtube_trending_titles()
    # print("▶ YouTube 급상승 영상 제목:")
    # for i, title in enumerate(yt_titles, 1):
    #     print(f"{i}. {title}")




def fetch_health_titles(limit=30):
    import feedparser

    RSS_URL = "https://www.yna.co.kr/rss/health.xml"
    print("▶ 연합뉴스 생활·건강 RSS 불러오는 중...")
    try:
        feed = feedparser.parse(RSS_URL)

        if not feed.entries:
            print("❌ RSS 데이터 없음")
            return []

        print(f"✅ 총 {len(feed.entries)}건 중 상위 {limit}개 제목 추출:\n")

        titles = []
        for i, entry in enumerate(feed.entries[:limit], 1):
            try:
                title = entry.title.strip()
                if title:
                    print(f"{i}. {title}")
                    titles.append(title)
                else:
                    print(f"⚠️ {i}번 항목: 제목 비어 있음")
            except Exception as e:
                print(f"❌ {i}번 항목에서 오류 발생: {e}")
        return titles
    except Exception as e:
        print(f"❌ RSS 파싱 실패: {e}")
        return []


    #fetch_health_titles()


def collect_all_topics():
    topic_list = []

    # 1. ZUM AI 이슈 트렌드
    zum_topics = get_zum_ai_issue_trends()
    topic_list.extend(zum_topics)
    print(f"✅ ZUM 키워드 {len(zum_topics)}개 수집 완료")

    # 2. Google 트렌드
    google_topics = get_google_trending_keywords()
    topic_list.extend(google_topics)
    print(f"✅ Google 키워드 {len(google_topics)}개 수집 완료")

    # 3. YouTube 트렌드 영상 제목
    youtube_topics = get_youtube_trending_titles()
    topic_list.extend(youtube_topics)
    print(f"✅ YouTube 제목 {len(youtube_topics)}개 수집 완료")

    # 4. 연합뉴스 건강 기사 제목

    health_topics = fetch_health_titles()
    topic_list.extend(health_topics)
    print(f"✅ 연합뉴스 건강기사 {len(health_topics)}개 수집 완료")

    return topic_list


def filter_topics_by_category(topic_list):
    from openai import OpenAI
    import json

    client = OpenAI(api_key=v_.api_key, timeout=200)

    """
    OpenAI GPT를 활용해 블로그 카테고리에 맞는 키워드 1개만 추출
    """

    system_message = (
        "당신은 콘텐츠 전문가이며, 주어진 블로그 카테고리에 가장 적합한 주제 1개를 JSON 배열 형식으로 출력하는 역할을 맡고 있습니다. "
        "출력은 반드시 JSON 배열만 사용하며, 그 외 부가 설명은 포함하지 마세요. "
        "이모지, 특수문자, 따옴표가 많은 문장, 부제 포함 등은 모두 제외하고 순수한 키워드 문장 1개만 반환하세요. "
        "출력 예시: [\"전기요금 절약하는 5가지 방법\"]"
    )

    user_prompt = f"""
    다음은 뉴스, 트렌드, 유튜브 영상에서 수집된 제목 및 키워드 목록입니다:

    {topic_list}

    이 중 다음 블로그 카테고리와 가장 관련성 높은 주제 1개만 골라주세요:

    [카테고리 설명]
    '{v_.my_category}', {v_.my_topic}

    ✅ 조건
    - 한글 제목 중심
    - 실용 정보, 생활 꿀팁, 정책, 정부 지원, 절약 노하우 등 실제로 도움이 되는 주제만
    - 연예, 게임, 스포츠, 유머 영상, 단순 일상 Vlog 등은 제외
    - 특수문자와 이모지 ❌
    - 출력은 반드시 JSON 배열 1개짜리 형식만 사용 (예: ["청년 전세자금대출 신청방법"])
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3
        )

        filtered_raw = response.choices[0].message.content.strip()
        filtered = json.loads(filtered_raw)
        if isinstance(filtered, list) and len(filtered) == 1:
            return filtered[0] if filtered else ""
        else:
            print("⚠️ GPT가 1개짜리 리스트로 반환하지 않음:", filtered_raw)
            return []
    except Exception as e:
        print("❌ 필터링 실패:", e)
        return []


