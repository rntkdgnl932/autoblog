from blog_function import call_gemini
from trend_search_page import search_web_for_keyword
from datetime import datetime
from bs4 import BeautifulSoup # BeautifulSoup 임포트 추가



# $ 주제 선정 및 초안 생성
def generate_issue_draft(keyword):
    """
    주어진 키워드로 웹 검색을 수행하고, 검색 결과를 바탕으로 블로그 초안을 생성합니다.
    """
    print(f"▶ 키워드 '{keyword}' 분석 및 자료 수집 시작")

    # 1. 웹 검색으로 최신 정보 수집 (새로운 단계)
    search_results = search_web_for_keyword(keyword, num_results=5)  # 예시: 상위 5개 결과 수집
    if not search_results:
        print(f"❌ '{keyword}'에 대한 웹 검색 결과가 없어 다음으로 넘어갑니다.")
        return False

    # 검색 결과를 프롬프트에 넣기 좋은 형식으로 가공
    reference_texts = "\n\n".join(
        [f"[출처 {i + 1}: {item['title']}]\n{item['snippet']}" for i, item in enumerate(search_results)])

    today = datetime.today().strftime("%Y년 %m월 %d일")

    print(f"▶ 수집된 자료 기반, '{keyword}' 본문 초안 생성 요청")
    prompt = f"""
    [역할]
    당신은 최신 이슈에 정통한 데이터 분석가이자 전문 작가입니다. 당신의 임무는 주어진 '참고 자료'만을 활용하여 사실에 기반한 깊이 있는 블로그 초안을 작성하는 것입니다.

    [지시]
    '{keyword}'라는 주제에 대해, 아래 '참고 자료'와 '작성 규칙'을 모두 준수하여 블로그 포스팅을 위한 상세한 '초안'을 작성해주세요. **절대로 '참고 자료'에 언급되지 않은 내용을 추측하거나 지어내지 마세요.**

    [참고 자료]
    {reference_texts}

    [작성 규칙]
    1. **사실 기반 작성:** 모든 내용은 반드시 위에 제공된 '[참고 자료]'에 근거해야 합니다.
    2. **정보의 최신성:** 글의 시점은 {today}입니다.
    3. **내용의 구체성:** 추상적인 설명 대신, 독자들이 바로 활용할 수 있는 구체적인 조건, 수치, 방법, 예시를 풍부하게 포함해주세요.
    4. **구조적 글쓰기:** 서론-본론-결론의 구조를 갖추고, 본론은 3~4개의 명확한 소주제로 나누어 각 소주제별로 내용을 상세히 서술해주세요.
    5. **출력 형식:** **가장 중요합니다. 절대 HTML 태그를 사용하지 말고, 오직 '일반 텍스트'로만** 작성해주세요.
    """

    article_result = call_gemini(prompt, temperature=0.5)  # 사실 기반 요약이므로 temperature를 약간 낮추는 것을 추천

    if article_result in ["SAFETY_BLOCKED", "API_ERROR"] or not article_result:
        print(f"❌ 초안 생성 실패({article_result}). 다음 키워드로 넘어갑니다.")
        return False

    print("✅ 초안 생성 완료.")
    # print(article_result) # 디버깅 시에만 활성화

    return article_result


def add_personal_view(article_draft, keyword):
    """
    생성된 사실 기반 초안에 개인적인 견해나 분석을 추가합니다.
    """
    print("▶ 생성된 초안에 개인적인 견해 추가 요청")
    prompt = f"""
    [역할]
    당신은 20년 경력의 데이터 분석 기반 칼럼니스트이자, 온라인 커뮤니티의 참여를 극대화하는 콘텐츠 전략가입니다. 당신의 글은 깊이 있는 분석과 독자의 눈높이를 맞춘 친근함을 동시에 갖추고 있습니다.

    [최종 목표]
    아래 '[기존 초안]'과 '[작업 규칙]'에 따라, '{keyword}'라는 주제의 글을 네이버 카페에 바로 게시할 수 있는 **완벽한 하나의 'HTML 코드 덩어리'**로 변환해주세요.

    [작업 규칙]

    1.  **제목 생성 (가장 중요):**
        - `[정보/분석]`, `[심층취재]` 와 같은 말머리를 사용해주세요.
        - 독자의 호기심을 자극하면서도, 핵심 키워드인 '{keyword}'가 반드시 포함된 매력적인 제목을 새로 만들어주세요.
        - 제목은 `<h2>` 태그로 감싸주세요.

    2.  **글의 구조 (엄격히 준수):**
        - **도입부 (Hook):** 독자의 공감을 사거나 문제의식을 던지는 2~3 문단의 짧은 글로 시작합니다.
        - **본문:** 최소 3개 이상의 소주제(`<h3>` 태그 사용)로 나누어 '기존 초안'의 내용을 논리적으로 재구성하고 발전시켜주세요.
        - **전문가 시각:** `<blockquote>` 태그를 사용하여 본문과 시각적으로 구분되는 분석 파트를 만들어주세요. 여기서는 '그래서 이게 왜 중요한가?', '앞으로의 전망은?'과 같은 깊이 있는 통찰을 제시합니다.
        - **결론:** 전체 내용을 2~3 문단으로 요약하며, 독자가 취해야 할 행동이나 생각해 볼 점을 명확히 제시합니다.
        - **참여 유도 (Call to Action):** 글 마지막에 구분선(`<hr>`)을 넣고, 독자들의 댓글과 투표 참여를 유도하는 친근한 문구를 추가해주세요.

    3.  **스타일 및 가독성:**
        - 모든 문단은 `<p>` 태그로 감싸고, 2~3줄을 넘지 않게 짧게 작성해주세요.
        - 핵심 단어나 문장은 `<strong>` 태그로 강조해주세요.
        - 문맥에 맞는 이모지(Emoji)를 적절히 사용하여 글의 활기를 더해주세요.
        - 체크리스트나 열거형 내용은 `<ul>`과 `<li>` 태그를 사용해 목록으로 만들어주세요.

    4.  **이미지 위치 지정:**
        - 글의 흐름상 이미지가 필수적인 위치에 `` 또는 `[IMAGE_PLACEHOLDER_1]`과 같은 주석이나 태그를 명확하게 남겨주세요.

    5.  **SEO 및 키워드 배치:**
        - 생성한 제목과 첫 번째 문단, 그리고 최소 2개 이상의 소주제(`<h3>`)에 핵심 키워드인 '{keyword}'를 자연스럽게 포함시켜주세요.

    6.  **HTML 제약사항:**
        - 네이버 카페 에디터와 완벽히 호환되도록, 기본적인 HTML 태그(`h2`, `h3`, `p`, `strong`, `ul`, `li`, `blockquote`, `hr`)만 사용해주세요.
        - 절대로 `<style>`, `<script>` 태그나 인라인 스타일(예: `style="..."`)은 사용하지 마세요.

    [기존 초안]
    {article_draft}
    """
    final_html_full = call_gemini(prompt, temperature=0.8)

    if not final_html_full or final_html_full in ["SAFETY_BLOCKED", "API_ERROR"]:
        print(f"❌ 최종본 생성 실패({final_html_full}).")
        return None, None  # 실패 시 두 개의 None을 반환

    print("✅ 최종본 생성 완료. 제목과 본문을 분리합니다.")

    # --- 이 부분이 핵심 수정 사항입니다 ---
    try:
        soup = BeautifulSoup(final_html_full, 'html.parser')

        # 1. 제목(h2 태그) 추출
        title_tag = soup.find('h2')
        if title_tag:
            # .get_text()로 태그 안의 텍스트만 깔끔하게 추출
            subject = title_tag.get_text()
            # .decompose()로 원본 HTML에서 제목 태그를 완전히 제거
            title_tag.decompose()
        else:
            # 만약 Gemini가 h2 태그를 만드는 데 실패하면, 키워드를 기본 제목으로 사용
            subject = f"[분석] {keyword}"

        # 2. 제목이 제거된 나머지 HTML 본문
        html_content = str(soup)

        # 3. (제목, 본문HTML) 두 개의 값을 반환
        return subject, html_content

    except Exception as e:
        print(f"❌ HTML 파싱 중 에러 발생: {e}")
        # 파싱 실패 시, 원본 HTML을 본문으로 하고 키워드를 제목으로 사용
        return f"[분석] {keyword}", final_html_full

# --- 메인 실행 로직 예시 ---
# keyword = "2025년 부동산 정책 변화"
# draft = generate_issue_draft(keyword)
# if draft:
#     final_post = add_personal_view(draft, keyword)
#     # 이후 네이버 카페 업로드 로직 호출
#     # upload_to_naver_cafe(final_post)