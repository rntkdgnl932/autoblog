# 🔄 [Gemini 2.5 Pro 최종 버전] 자동 블로그 업로드 스크립트
# 모델: Gemini 2.5 Pro 전면 사용

import os
import requests
import base64
import json
import re
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.media import UploadFile
from bs4 import BeautifulSoup
from slugify import slugify
from datetime import datetime

# 사용자 정의 변수 모듈 (유동적으로 변경되는 부분)
import variable as v_

# --- 설정 로드 ---
dir_path = "C:\\my_games\\" + str(v_.game_folder)
file_path_one = dir_path + "\\mysettings\\idpw\\onecla.txt"
if os.path.isfile(file_path_one):
    with open(file_path_one, "r", encoding='utf-8-sig') as file:
        lines_one = file.read().split('\n')
        v_.wd_id = lines_one[0]
        v_.wd_pw = lines_one[1]
        v_.domain_adress = lines_one[2]
        if len(lines_one) > 3:
            # variable.py 또는 텍스트 파일에 Gemini API 키를 저장했다고 가정
            v_.gemini_api_key = lines_one[3]
        if len(lines_one) > 4:
            v_.my_category = lines_one[4]
else:
    print('one 파일 없당')

# --- 클라이언트 설정 ---
# ✅ Gemini API + WordPress 클라이언트 설정
try:
    genai.configure(api_key=v_.my_gas_key)
except Exception as e:
    print(f"❌ Gemini API 키 설정 실패: {e}")

wp = Client(f"{v_.domain_adress}/xmlrpc.php", v_.wd_id, v_.wd_pw)
CATEGORY = v_.my_category if hasattr(v_, 'my_category') else "일반"


# --- Gemini 호출 래퍼 함수 ---
def call_gemini(prompt, temperature=0.6, is_json=False):
    """Gemini API를 호출하고 결과를 반환하는 중앙 함수"""
    try:
        # ✅ 요청하신 최신 모델 'gemini-2.5-pro'로 변경
        model = genai.GenerativeModel('gemini-2.5-pro')
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            response_mime_type="application/json" if is_json else "text/plain"
        )
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text
    except Exception as e:
        print(f"❌ Gemini API 호출 실패 (모델: gemini-2.5-pro): {e}")
        return None


# $ 요약
def summarize_for_description(content, title=None, keyword=None):
    if title and title in content:
        content = content.replace(title, "")

    import textwrap
    summary_target = textwrap.shorten(content, width=1800, placeholder="...")
    keyword_line = f"이 내용은 '{keyword}'에 관한 블로그 본문입니다." if keyword else ""

    prompt = f"""
    [역할]
    당신은 '{v_.my_topic}' 주제에 특화된 전문 블로그 기획자입니다. SEO를 고려한 요약 문장을 작성합니다.

    [지시]
    {keyword_line}
    다음 블로그 본문 내용을 **100자 이내로 자연스럽게 요약**해줘.

    [요약 조건]
    - 핵심 내용을 간결하게 전달할 것
    - **제목 문장과 겹치지 않도록** 요약할 것
    - 흥미를 유발하는 정보 요약 중심 (의문형·감성 문장 허용)
    - **불필요한 형식, 이모티콘, 마크다운, HTML 금지**
    - 순수 자연어 문장만 출력

    [본문 내용]
    {summary_target}
    """

    result = call_gemini(prompt, temperature=0.6)
    if result and len(result) >= 15:
        return result.strip()
    else:
        print("⚠️ 요약 결과가 너무 짧아 원본 내용으로 대체합니다.")
        return content.strip()[:100]


# $ 사진 생성
def stable_diffusion(article, filename, description, slug):
    try:
        print("▶ Gemini로 Stable Diffusion 프롬프트 생성 요청", description)

        COMMON_NEGATIVE = "blurry, low quality, bad anatomy, disfigured, deformed, cropped, watermark, jpeg artifacts, text, bad anatomy, deformed face, mutated hands, poorly drawn face, missing lips, fused eyes, extra limbs, ugly, lowres"

        if filename == "thumb":
            style_prompt = "flat design, minimal, vector style, sharp eyes, cinematic style, clear background, high detail face, photorealistic, 8k, perfect lighting"
            prompt_base = f"다음 내용을 기반으로 블로그 썸네일 이미지를 생성할 수 있도록, {style_prompt} 키워드 중심으로 스테이블 디퓨전 프롬프트를 만들어줘:\n{description}"
        else:  # "scene"
            style_prompt = "photo, realistic, cinematic, natural light, sharp eyes, cinematic style, clear background, high detail face, photorealistic, 8k, perfect lighting"
            prompt_base = f"다음 내용을 기반으로 사실적이고 정보성 있는 본문 이미지를 생성할 수 있도록, {style_prompt} 스타일의 스테이블 디퓨전 프롬프트를 만들어줘:\n{description}"

        short_prompt = call_gemini(prompt_base, temperature=0.5)
        if not short_prompt:
            raise ValueError("Gemini로부터 프롬프트를 생성하지 못했습니다.")

        print(f"🖼 생성된 프롬프트: {short_prompt}")

        payload = {
            "prompt": f"{short_prompt}, highly detailed, cinematic lighting, ultra-realistic, 4K",
            "negative_prompt": COMMON_NEGATIVE,
            "steps": 30, "width": 512, "height": 512, "sampler_index": "Euler", "cfg_scale": 8,
            "override_settings": {"sd_model_checkpoint": "xxmix9realistic_v40.safetensors [18ed2b6c48]"}
        }

        print("▶ Stable Diffusion 이미지 요청")
        response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload, timeout=300)
        response.raise_for_status()

        b64_image = response.json()['images'][0]
        image_bytes = base64.b64decode(b64_image)

        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=60)
        image = BytesIO(buf.getvalue())
        image.name = f"{slug}_{filename}.jpg"
        image.seek(0)

        media = {
            'name': image.name, 'type': 'image/jpeg', 'caption': short_prompt,
            'description': description, 'bits': xmlrpc_client.Binary(image.read())
        }
        return media
    except Exception as e:
        print(f"⚠️ Stable Diffusion 이미지 생성 실패: {e}")
        return None


# $ AI 상태 체크
def check_gemini_ready():
    """Gemini API가 정상적으로 응답하는지 확인"""
    print("🛰️ Gemini API 상태를 확인합니다...")
    try:
        response = call_gemini("hello")
        if response:
            return True
        return False
    except Exception as e:
        print(f"❗ Gemini API 연결 오류: {e}")
        return False


# $ 주제 선정 및 초안 생성
def life_tips_keyword(keyword):
    print(f"▶ 키워드 '{keyword}'로 본문 초안 생성 요청")
    today = datetime.today().strftime("%Y년 %m월 %d일")
    this_year = datetime.today().year

    prompt = f"""
    [역할]
    당신은 '{v_.my_topic}' 주제에 특화된 전문 블로그 기획자입니다. 실제로 조사해 요약하는 방식으로, 정확하고 감성적인 콘텐츠를 작성해야 합니다. 특히 독자가 실질적으로 도움을 받을 수 있도록 유효한 최신 정보만 반영해야 합니다.

    [지시]
    아래 조건에 맞춰 '{keyword}' 주제로 블로그 본문 초안을 작성해주세요.

    [정보 최신성 기준]
    - 이 콘텐츠는 **{today} 기준으로 최신 정보만 포함**되어야 합니다.
    - **{this_year}년 이전에 발표된 정책·제도·지원금은 제외**하고, **현재 신청 가능한 정보**만 반영해야 합니다.

    [작성 조건]
    - 분량: 약 1000~1200자
    - 문체: 친근하고 감성적인 말투이되, **정보성 중심**
    - 포맷: HTML 태그 없이 일반 텍스트로 구성 (단락 구분은 줄바꿈)

    [금지 사항]
    - 이미 종료된 정책 또는 신청 불가능한 정보 포함
    - 추정 정보, 존재하지 않는 기관·사이트·전화번호 작성
    """

    article = call_gemini(prompt, temperature=0.5)
    if article:
        life_tips_start(article.replace("```html", "").replace("```", ""), keyword)


# $ 콘텐츠 고도화 및 발행
def life_tips_start(article, keyword):
    slug = slugify(keyword)

    print("▶ Gemini로 콘텐츠 구조화 및 상세화 작업")

    # optimize_html_for_seo_with_gpt 함수가 전체 HTML을 생성
    final_html = optimize_html_for_seo_with_gpt(article, keyword)
    if not final_html:
        print("❌ 콘텐츠 고도화에 실패하여 업로드를 중단합니다.")
        return

    try:
        soup = BeautifulSoup(final_html, 'html.parser')
        title_tag = soup.find("meta", attrs={"name": "title"})
        title = title_tag["content"] if title_tag else f"{keyword}에 대한 모든 것"

        desc_tag = soup.find("meta", attrs={"name": "description"})
        meta_description = desc_tag["content"] if desc_tag else ""

        body_content_tag = soup.find("div", id="gemini-blog-body")
        body_html = body_content_tag.decode_contents() if body_content_tag else final_html
    except Exception as e:
        print(f"❌ 최종 HTML 파싱 실패: {e}\n생성된 HTML: {final_html}")
        return

    print("▶ 썸네일/본문 이미지 생성")
    short_slug = slugify(keyword)[:50]
    thumb_media = stable_diffusion(article, "thumb", f"{keyword} 썸네일", short_slug)
    thumbnail_id = wp.call(UploadFile(thumb_media)).get("id") if thumb_media else None

    scene_media = stable_diffusion(article, "scene", f"{keyword} 본문 이미지", short_slug)
    scene_url = wp.call(UploadFile(scene_media)).get("link") if scene_media else ""

    if scene_url:
        img_tag_html = f"<figure class='wp-block-image size-large'><img src='{scene_url}' alt='{keyword}'/></figure>"
        body_html = img_tag_html + body_html

    print("▶ 태그 추출 및 워드프레스 게시물 준비")
    auto_tags = extract_tags_from_html_with_gpt(body_html, keyword)

    post = WordPressPost()
    post.title = title
    post.content = body_html
    post.excerpt = meta_description
    post.terms_names = {
        'category': [safe_term_cate(CATEGORY)],
        'post_tag': list(set([safe_term_word(keyword)] + [safe_term_word(t) for t in auto_tags]))
    }
    post.custom_fields = [
        {'key': 'rank_math_description', 'value': meta_description},
        {'key': 'rank_math_focus_keyword', 'value': keyword},
        {'key': 'rank_math_secondary_keywords', 'value': ", ".join(auto_tags)}
    ]
    if thumbnail_id:
        post.thumbnail = thumbnail_id
    post.post_status = 'publish'

    if not title or not body_html or len(body_html.strip()) < 200:
        print("❌ 콘텐츠 품질이 낮아 업로드를 중단합니다.")
    else:
        post_id = wp.call(NewPost(post))
        print(f"✅ 게시 완료! (Post ID: {post_id}) - 제목: {title}")


# $ 태그 추출
def extract_tags_from_html_with_gpt(html_content, keyword):
    prompt = f"""
    [역할]
    당신은 SEO 전문가입니다.

    [지시]
    다음 블로그 HTML 콘텐츠에서, 블로그 태그로 사용할 핵심 키워드 5~7개를 추출해주세요.

    [조건]
    - 본문에 실제 등장한 주요 용어만 사용합니다.
    - 각 키워드는 1~3단어로 짧고 명확해야 합니다.
    - 메인 키워드 '{keyword}'와 중복되지 않아야 합니다.
    - 출력은 반드시 JSON 배열 형식이어야 합니다. 예: ["전기차", "요금 할인", "환경부"]

    [HTML 콘텐츠]
    {html_content}
    """

    response_text = call_gemini(prompt, temperature=0.2, is_json=True)
    if not response_text: return []
    try:
        tags = json.loads(response_text)
        return tags if isinstance(tags, list) else []
    except json.JSONDecodeError:
        print(f"⚠️ 태그 추출 JSON 파싱 실패:\n{response_text}")
        return []


# $ 내용 상세하게 (핵심 로직 통합)
def optimize_html_for_seo_with_gpt(article, keyword):
    print("▶ Gemini로 전체 콘텐츠 재구성 요청")
    today = datetime.today().strftime("%Y년 %m월 %d일")
    this_year = datetime.today().year

    prompt = f"""
    [역할]
    당신은 '{v_.my_topic}' 주제의 전문 블로그 작가이자 SEO 전문가입니다. 당신의 목표는 독자가 다른 페이지로 이탈하지 않고 모든 정보를 얻을 수 있는, 완결성 높은 콘텐츠를 만드는 것입니다.

    [기본 정보]
    - 블로그 주제: '{v_.my_topic}'
    - 핵심 키워드: '{keyword}'
    - 작성 기준일: {today}

    [초안 내용]
    {article}

    [최종 콘텐츠 작성 지시]
    위 '초안 내용'을 바탕으로, 아래의 모든 조건을 충족하는 완벽한 블로그 포스트용 HTML을 작성해주세요.

    1.  **전체 구조**:
        - `<meta name="title" content="...">` : '{keyword}'로 시작하는, 클릭을 유도하는 50자 내외 제목.
        - `<meta name="description" content="...">` : 본문 핵심 내용을 120자 내외로 요약한 설명.
        - `<div id="gemini-blog-body">...</div>` : 아래 2~5번 항목을 포함하는 실제 본문.

    2.  **본문 스타일 및 내용**:
        - **소제목(<h2>)**: 4~6개의 명확한 소제목으로 내용을 구분합니다.
        - **상세 내용**: 각 소제목 아래, 초안을 재해석하고 웹 검색을 통해 얻은 최신/정확한 정보로 내용을 상세화합니다. (신청 대상, 조건, 절차, 금액, 예시, 필요 서류 등 구체적인 정보 포함)
        - **가독성**: 각 소제목 섹션마다 **표(<table>) 또는 목록(<ul>)을 반드시 1개 이상** 사용하여 정보를 시각적으로 정리합니다.
        - **신뢰성**: 'A기관에 따르면', 'B정책의 경우'처럼 정보 출처를 명확히 밝히되, "링크 참조"와 같은 표현 대신 내용을 직접 서술합니다. 모든 기관명, 웹사이트 주소, 전화번호는 **실존하는 공식 정보**여야 합니다.
        - **최신성**: **{this_year}년 기준 현재 유효한 정보**만 다루며, 종료된 정책은 절대 포함하지 않습니다.

    3.  **마무리 형식**:
        - **한줄요약**: 본문 맨 끝에 `<p><strong>한줄요약:</strong> [본문 전체를 관통하는 핵심 한 문장]</p>` 형식으로 추가합니다.
        - **개인의견**: 한줄요약 바로 아래에 `<p><em>개인의견:</em> [전문가로서의 냉철하고 직설적인 최종 결론 또는 팁]</em></p>` 형식으로 추가합니다.

    4.  **SEO 및 HTML 규칙**:
        - **AI 흔적 제거**: "도움이 되셨기를 바랍니다" 같은 AI 말투나, "ChatGPT가 생성함" 등의 문구는 절대 금지입니다.
        - **태그 사용**: `<h1>`은 사용하지 않습니다. 핵심 단어는 `<strong>`으로 자연스럽게 강조합니다.
        - **HTML 유효성**: 최종 결과물은 다른 설명 없이 순수 HTML 코드여야 합니다.

    5.  **추가 조건**:
        {v_.my_prompt if hasattr(v_, 'my_prompt') else ''}
    """

    final_html = call_gemini(prompt, temperature=0.6)
    return final_html


# --- 유틸리티 함수 ---
def safe_term_cate(term):
    if not term or not isinstance(term, str): return "일반"
    return term.strip()[:40]


def safe_term_word(term):
    if not term or not isinstance(term, str): return "일반"
    term = term.strip()[:40]
    term = re.sub(r"[^\w가-힣\s-]", "", term)
    return re.sub(r"\s+", "-", term)


def load_existing_titles():
    print("📌 최신 글 20개 제목을 가져옵니다.")
    url = f"{v_.domain_adress}/wp-json/wp/v2/posts?per_page=20&page=1&orderby=date&order=desc"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        titles = [post['title']['rendered'] for post in resp.json()]
        print(f"✅ {len(titles)}개의 제목 로드 완료.")
        return titles
    except requests.RequestException as e:
        print(f"❌ 제목 가져오기 실패: {e}")
        return []


def is_similar_topic(new_topic, existing_titles):
    if not existing_titles: return 0
    prompt = f"새 주제 '{new_topic}'이 기존 제목 목록 {existing_titles}과 얼마나 유사한지 0~100점 사이의 숫자로만 평가해줘."
    result = call_gemini(prompt, temperature=0.1)
    try:
        return int(re.search(r'\d+', result).group()) if result else 0
    except (ValueError, AttributeError):
        return 0


# $ 제목 정하기 (메인 실행 함수)
def suggest_life_tip_topic():
    print("▶ 새로운 주제 추천 요청")
    result_titles = load_existing_titles()
    today = datetime.today().strftime("%Y년 %m월 %d일")
    month = datetime.today().month
    seasons = {3: "봄", 4: "봄", 5: "봄", 6: "여름", 7: "여름", 8: "여름", 9: "가을", 10: "가을", 11: "가을"}
    current_season = seasons.get(month, "겨울")

    # ✅ 사용자 정의 역할(System)과 주제(User)를 동적으로 반영
    system_prompt = v_.my_topic_system if hasattr(v_,
                                                  'my_topic_system') else f"당신은 '{v_.my_topic}' 주제에 특화된 전문 블로그 기획자입니다."
    user_prompt = f"""
    {v_.my_topic_user if hasattr(v_, 'my_topic_user') else ''}

    [이미 다룬 블로그 제목 목록]
    {result_titles}

    [주제 선정 조건]
    - 위 목록과 **겹치지 않는 새로운 주제** 10개를 추천해주세요.
    - 검색 수요가 높은 구체적인 정보 위주로 제시해주세요. (예: '여름철 건강관리' ❌ → '폭염 속 전기요금 할인제도 신청방법' ✅)
    - 출력은 반드시 JSON 배열 형식이어야 합니다. 예: ["주제1", "주제2"]
    """

    prompt = f"{system_prompt}\n\n{user_prompt}"

    response_text = call_gemini(prompt, temperature=0.8, is_json=True)
    if not response_text:
        print("❌ 주제 추천을 받지 못했습니다.")
        return False

    try:
        suggested_keywords = json.loads(response_text)
        if not isinstance(suggested_keywords, list): raise ValueError()
    except (json.JSONDecodeError, ValueError):
        print(f"❌ 추천 주제 파싱 실패:\n{response_text}")
        return False

    print("🆕 추천 키워드들:", suggested_keywords)
    for kw in suggested_keywords:
        score = is_similar_topic(kw, result_titles)
        if score < 70:
            print(f"✅ 주제 선정: '{kw}' (유사도: {score}%)")
            life_tips_keyword(kw)
            return True  # 포스팅 1개 작성 후 종료
        else:
            print(f"⚠️ 유사 주제 건너뛰기: '{kw}' (유사도: {score}%)")

    print("✅ 모든 추천 주제가 기존 글과 유사하여 종료합니다.")
    return False

#
# # --- 스크립트 실행 ---
# if __name__ == "__main__":
#     if check_gemini_ready():
#         print("✅ Gemini API 상태 정상. 자동 포스팅을 시작합니다.")
#         suggest_life_tip_topic()
#     else:
#         print("❌ Gemini API 상태를 확인할 수 없어 스크립트를 종료합니다.")