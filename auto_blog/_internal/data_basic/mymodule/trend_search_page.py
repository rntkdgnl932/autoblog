def trend_search():
    import requests
    from bs4 import BeautifulSoup
    from pytrends.request import TrendReq

    print("\n📌 [Google Trends - 한국 실시간 급상승 검색어]")
    try:
        pytrends = TrendReq(hl='ko', tz=540)
        trending = pytrends.trending_searches(pn='south_korea')
        for i, keyword in enumerate(trending[0].tolist()[:10], 1):
            print(f"{i}위: {keyword}")
    except Exception as e:
        print("⚠️ Google Trends 오류:", e)

    print("\n📌 [Naver Datalab 실시간 트렌드 (급상승 키워드)]")
    try:
        naver_url = 'https://datalab.naver.com/keyword/realtimeList.naver'
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(naver_url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')

        ranks = soup.select('.ranking_box .title')
        for i, rank in enumerate(ranks[:10], 1):
            print(f"{i}위: {rank.get_text().strip()}")
    except Exception as e:
        print("⚠️ Naver 크롤링 오류:", e)

    print("\n📌 [Daum 뉴스 트렌드 검색어]")
    try:
        daum_url = "https://search.daum.net/ranking/bestreply"
        resp = requests.get(daum_url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')

        keywords = soup.select("ol.list_ranking li a")
        for i, k in enumerate(keywords[:10], 1):
            print(f"{i}위: {k.get_text().strip()}")
    except Exception as e:
        print("⚠️ Daum 크롤링 오류:", e)
