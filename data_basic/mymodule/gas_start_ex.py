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


# ==============================================================================
# Gemini API 호출 래퍼 함수 (안전 설정 포함)
# ==============================================================================
def call_gemini(prompt, temperature=0.6, is_json=False, max_retries=3):
    import time  # time.sleep()을 위해 상단에 추가해야 합니다.
    """
    API 호출 실패 시 원인을 파악하여 '통신 오류'에 대해서만 자동 재시도합니다.
    """
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel('gemini-2.5-pro')
            safety_settings = {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE", "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE", "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
            generation_config = genai.types.GenerationConfig(
                temperature=temperature, response_mime_type="application/json" if is_json else "text/plain"
            )

            # ✅ API 호출 시 타임아웃 설정 (예: 5분)
            response = model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings,
                request_options={'timeout': 300}
            )

            if response.parts:
                return response.text  # 성공 시 즉시 결과 반환

            # 안전 필터에 의해 차단된 경우
            elif response.candidates and response.candidates[0].finish_reason.name == "SAFETY":
                print("⚠️ API 응답이 안전 필터에 의해 차단되었습니다. (재시도 안 함)")
                return "SAFETY_BLOCKED"  # ✅ 재시도 없이 즉시 '안전 차단' 신호 반환

            # 기타 이유로 빈 응답이 온 경우
            else:
                print(f"⚠️ API가 알 수 없는 이유로 빈 응답을 반환했습니다. ({attempt + 1}/{max_retries}차 시도)")
                time.sleep(5 * (attempt + 1))  # 5초, 10초, 15초 간격으로 대기
                continue  # 다음 재시도 실행

        except Exception as e:
            print(f"❌ Gemini API 통신 중 예외 발생: {e} ({attempt + 1}/{max_retries}차 시도)")
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))  # ✅ 재시도 전 N초 대기
            continue  # 다음 재시도 실행

    print("❌ 최대 재시도 횟수를 초과했습니다. 최종 실패 처리합니다.")
    return "API_ERROR"  # 모든 재시도 실패 시 '통신 오류' 신호 반환


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
# $ 사진 생성 (프롬프트 강화 버전)
def stable_diffusion(article, filename, description, slug):
    try:
        print(f"▶ Gemini로 [{filename}] 이미지 프롬프트 생성 요청: {description}")

        # ✅ 1. 네거티브 프롬프트 강화
        ENHANCED_NEGATIVE = (
            "(deformed, distorted, disfigured:1.3), "
            "poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, "
            "(mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, "
            "ugly, disgusting, blurry, amputation, (text, watermark, signature, username, artist name, logo)"
        )

        # ✅ 2. Gemini에게 전달할 프롬프트를 훨씬 더 구체적이고 구조적으로 변경
        if filename == "thumb":
            # 썸네일: 시선 집중, 상징적, 미니멀 스타일
            meta_prompt = f"""
            [역할]
            당신은 AI 이미지 생성 모델 'Stable Diffusion'의 전문 프롬프트 엔지니어입니다.

            [지시]
            '{description}'이라는 주제에 맞춰, 시선을 사로잡는 블로그 **썸네일**용 프롬프트를 생성해주세요.

            [스타일 가이드]
            - 스타일: **미니멀리즘, 플랫 디자인, 벡터 아트**
            - 색상: 밝고 선명한 색상, 긍정적인 느낌
            - 구성: 주제를 상징적으로 표현하는 아이콘이나 인물 중심, 배경은 단순하게
            - 절대 조건: **프롬프트 내에 글자(Text)가 포함되면 안 됨**

            [출력 형식]
            - 가장 중요한 키워드부터 순서대로, 쉼표(,)로 구분된 영어 키워드 목록으로만 출력하세요.
            - 다른 설명은 일절 포함하지 마세요.

            [출력 예시]
            A young woman smiling holding a glowing piggy bank, minimalist, vector illustration, simple background, vibrant colors, clean lines, trending on artstation
            """
        else:  # "scene"
            # 본문 이미지: 사실적, 감성적, 고품질 사진 스타일
            meta_prompt = f"""
            [역할]
            당신은 AI 이미지 생성 모델 'Stable Diffusion'의 전문 프롬프트 엔지니어입니다.

            [지시]
            '{description}'이라는 주제의 블로그 **본문 삽입용** 프롬프트를 생성해주세요.

            [스타일 가이드]
            - 스타일: **극사실적, 고품질 사진(Photorealistic)**
            - 인물/감성: 주제와 관련된 인물이 등장한다면, 자연스럽고 긍정적인 표정
            - 조명 및 배경: 자연광 또는 영화적인 조명(cinematic lighting), 배경 흐림(depth of field) 효과로 주제에 집중
            - 절대 조건: **프롬프트 내에 글자(Text)가 포함되면 안 됨**

            [출력 형식]
            - 가장 중요한 키워드부터 순서대로, 쉼표(,)로 구분된 영어 키워드 목록으로만 출력하세요.
            - 다른 설명은 일절 포함하지 마세요.

            [출력 예시]
            photorealistic, a happy family sitting on a couch and planning their budget, warm natural light from window, cozy living room, depth of field, candid shot, 8k, raw photo
            """

        # Gemini를 호출하여 SD 프롬프트 생성
        short_prompt = call_gemini(meta_prompt, temperature=0.5)
        if not short_prompt:
            raise ValueError("Gemini로부터 프롬프트를 생성하지 못했습니다.")

        print(f"🖼 생성된 프롬프트: {short_prompt}")

        # ✅ 3. 최종 payload 구성 시 고품질 키워드를 앞쪽에 추가
        final_prompt = f"masterpiece, best quality, 8k, ultra high res, {short_prompt}"

        payload = {
            "prompt": final_prompt,
            "negative_prompt": ENHANCED_NEGATIVE,
            "steps": 30,
            "width": 512,
            "height": 512,
            "sampler_index": "Euler a",  # 'Euler a'가 일반적으로 좋은 품질을 보여줌
            "cfg_scale": 7.5,
            "override_settings": {
                "sd_model_checkpoint": "xxmix9realistic_v40.safetensors [18ed2b6c48]"
            }
        }

        print("▶ Stable Diffusion 이미지 요청")
        response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload, timeout=300)
        response.raise_for_status()

        b64_image = response.json()['images'][0]
        image_bytes = base64.b64decode(b64_image)

        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=75)  # 품질을 60 -> 75로 약간 상향
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

#$ 제목 설정하기


def generate_impactful_titles(keyword, article_summary):
    """
    Gemini를 활용해 클릭을 유도하는 강력한 블로그 제목 5개를 생성합니다.
    """
    print("▶ Gemini로 클릭 유도형 제목 생성 요청...")

    prompt = f"""
    [역할]
    당신은 10년차 전문 디지털 마케터이자 바이럴 콘텐츠 카피라이터입니다.

    [지시]
    아래 '핵심 키워드'와 '글 요약'을 바탕으로, 사용자들이 클릭하지 않고는 못 배길 매력적인 블로그 제목 5개를 생성해주세요.

    [제목 생성 원칙]
    1.  **숫자 활용:** '5가지', 'TOP 3' 등은 반드시 내용을 파악하고 구체적인 숫자를 포함하여 신뢰도를 높여라.
    - 예시 : 실제 방법은 3가지인데, 소제목이 5개라서 5가지로 하면 안됨.
    2.  **호기심 자극:** '숨겨진', '...하는 유일한 방법', '모르면 손해' 등 궁금증을 유발하라.
    3.  **이득 강조:** 'OO만원 절약', '시간 단축' 등 독자가 얻을 명확한 혜택을 제시하라.
    4.  **강력한 단어:** '총정리', 'A to Z', '필수', '비법' 등 단어를 사용하여 전문성을 어필하라.
    5.  **질문 형식:** 독자에게 직접 말을 거는 듯한 질문으로 참여를 유도하라.

    [핵심 키워드]
    {keyword}

    [글 요약]
    {article_summary}

    [출력 형식]
    - 위 5가지 원칙 중 최소 2~3가지를 조합하여 창의적인 제목을 만드세요.
    - 다른 설명 없이, 생성된 제목 5개를 JSON 배열 형식으로만 출력하세요.
    - 예시: ["제목1", "제목2", "제목3", "제목4", "제목5"]
    """

    response_text = call_gemini(prompt, temperature=0.8, is_json=True)
    # ✅ call_gemini로부터 오류 신호를 받으면 그대로 반환
    if response_text in ["SAFETY_BLOCKED", "API_ERROR"] or not response_text:
        print("⚠️ 제목 생성 실패, 상위 함수로 오류를 전달합니다.")
        return response_text if response_text else "API_ERROR"

    try:
        titles = json.loads(response_text)
        return titles if isinstance(titles, list) and titles else "API_ERROR"
    except Exception as e:
        print(f"⚠️ 제목 JSON 파싱 실패: {e}")
        return "API_ERROR"


# ==============================================================================
#  ✨ [신규] 분업화된 콘텐츠 생성 함수들
# ==============================================================================

def generate_main_body_html(article, keyword):
    """(분업 1) Gemini에게 오직 '본문'의 HTML 구조화만 요청하는 함수"""
    print("  ▶ (분업 1) Gemini로 본문 HTML 생성 중...")
    prompt = f"""
    [역할] 당신은 HTML 구조화에 능숙한 전문 작가입니다. 주어진 '초안'을 '엄격한 HTML 규칙'에 따라 변환하세요.
    [엄격한 HTML 규칙]
    1. **소제목**: 주요 섹션 소제목은 **반드시 `<h2>` 태그**로 감싸세요.
    2. **목록/표**: 항목 나열은 `<ul><li>`, 데이터 정리는 `<table>`을 사용하세요. 각 `<h2>` 섹션마다 최소 1개 이상의 목록 또는 표를 포함해야 합니다.
    3. **마무리**: 글 마지막에 `<p><strong>한줄요약:</strong>...</p>`과 `<p><em>개인의견:</em>...</p>`을 순서대로 추가하세요.
    4. **출력 형식**: 다른 설명, `<html>`, `<body>` 태그 없이, 본문에 해당하는 순수 HTML 조각(fragment)만 출력하세요.
    [초안 내용]
    {article}
    """
    html_body = call_gemini(prompt, temperature=0.5)
    return html_body or f"<p>{keyword}에 대한 글을 생성하지 못했습니다.</p>"


# ==============================================================================
# ✨ [신규] 분업화된 콘텐츠 '데이터' 생성 함수들
# ==============================================================================
def generate_structured_content_json(article, keyword):
    """(분업 1) Gemini에게 'HTML이 아닌' 구조화된 'JSON 데이터'를 생성하도록 요청"""
    print("  ▶ (분업 1) Gemini로 본문 JSON 데이터 생성 중...")
    prompt = f"""
    [역할] 당신은 블로그 콘텐츠 구조화 전문가입니다.
    [지시] 주어진 '초안'을 분석하여, 아래 'JSON 출력 구조'에 맞춰 콘텐츠를 재구성해주세요.

    [JSON 출력 구조]
    {{
      "sections": [
        {{
          "title": "첫 번째 소제목 텍스트",
          "content": "첫 번째 소제목에 해당하는 본문 텍스트입니다. 목록이 필요하면 * 항목 1\\n* 항목 2 와 같이 마크다운 형식으로 작성해주세요."
        }},
        {{
          "title": "두 번째 소제목 텍스트",
          "content": "두 번째 소제목 본문입니다. 표가 필요하다면 | 헤더1 | 헤더2 |\\n|---|---|\\n| 내용1 | 내용2 | 와 같이 마크다운 형식으로 작성해주세요."
        }}
      ],
      "summary": "글 전체를 요약하는 한 문장입니다.",
      "opinion": "전문가로서의 직설적인 개인 의견입니다."
    }}

    [가장 중요한 규칙]
    - **절대 HTML 태그를 사용하지 마세요.**
    - 출력은 다른 설명 없이, 오직 위에서 설명한 JSON 형식이어야 합니다.

    [초안 내용]
    {article}
    """
    json_response = call_gemini(prompt, temperature=0.5, is_json=True)
    try:
        return json.loads(json_response)
    except Exception as e:
        print(f"⚠️ 본문 JSON 생성 또는 파싱 실패: {e}")
        return None

def generate_meta_description(content_text, keyword):
    """(분업 2) 본문 텍스트를 기반으로 메타 디스크립션을 생성"""
    print("  ▶ (분업 2) Gemini로 메타 디스크립션 생성 중...")
    prompt = f"다음 글을 SEO에 최적화하여 120자 내외의 흥미로운 '메타 디스크립션'으로 요약해줘. 반드시 한 문장의 순수 텍스트만 출력해야 해.\n\n[본문 요약]\n{content_text[:1000]}"
    desc = call_gemini(prompt, temperature=0.5)
    return desc.split('\n')[0].strip() if desc else f"{keyword}에 대한 상세 정보와 신청 방법, 꿀팁을 확인하세요."


def generate_json_ld_faq(content_text):
    """(분업 3) 본문 텍스트를 기반으로 'mainEntity'를 포함한 표준 JSON-LD FAQ 스키마 '데이터' 생성"""
    print("  ▶ (분업 3) Gemini로 표준 JSON-LD FAQ 데이터 생성 중...")

    # ✅ 1. 프롬프트 강화: 'mainEntity'를 포함한 정확한 구조를 예시로 명시
    prompt = f"""
    [지시]
    다음 글 내용을 바탕으로 SEO에 유용한 FAQ 3~4개를 만들어줘.

    [가장 중요한 규칙]
    - **반드시 아래 예시와 동일한 키와 중첩 구조를 가진 순수한 JSON 객체만** 응답해야 합니다.
    - **특히 최상위 키로 "mainEntity"를 반드시 사용해야 합니다.**
    - 설명, `<script>` 태그, 마크다운 등 다른 텍스트는 절대 포함하지 마세요.

    [JSON 출력 구조 예시]
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "질문 1 텍스트",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "답변 1 텍스트"
          }}
        }},
        {{
          "@type": "Question",
          "name": "질문 2 텍스트",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "답변 2 텍스트"
          }}
        }}
      ]
    }}

    [블로그 내용]
    {content_text[:2000]}
    """
    json_content = call_gemini(prompt, temperature=0.2, is_json=True)

    # ✅ 2. 코드 레벨에서 'mainEntity' 키 존재 여부 검증
    if json_content:
        try:
            parsed_json = json.loads(json_content)
            if isinstance(parsed_json, dict) and 'mainEntity' in parsed_json:
                print("✅ 'mainEntity'를 포함한 유효한 JSON-LD 데이터 생성 완료.")
                # 가독성을 위해 다시 포맷팅하여 반환
                return json.dumps(parsed_json, indent=2, ensure_ascii=False)
            else:
                print("⚠️ JSON은 유효하지만, 표준 키('mainEntity')가 누락되었습니다.")
                return None
        except json.JSONDecodeError:
            print(f"⚠️ Gemini가 유효하지 않은 JSON 형식을 반환했습니다: {json_content[:100]}...")
            return None

    return None


# ==============================================================================
#  ✨ [신규] 파이썬 기반의 HTML 처리 함수들
# ==============================================================================

def create_table_of_contents(soup):
    """(파이썬 역할 1) BeautifulSoup으로 목차를 안정적으로 생성"""
    print("  ▶ (파이썬 역할 1) 코드로 목차 생성 중...")
    toc_list = []
    for i, h2 in enumerate(soup.find_all('h2'), 1):
        title_text = h2.get_text(strip=True)
        slug_id = slugify(title_text) if slugify(title_text) else f"section-{i}"
        h2['id'] = slug_id
        toc_list.append(f'<li><a href="#{slug_id}">{title_text}</a></li>')
    return f'<h2>목차</h2><ul class="table-of-contents">{"".join(toc_list)}</ul>' if toc_list else ""


def clean_and_refine_html(soup):
    """(파이썬 역할 2) URL 자동 링크, '개인의견' 스타일링 등 최종 정리"""
    print("  ▶ (파이썬 역할 2) 코드로 HTML 최종 정리 중...")
    url_pattern = re.compile(r'(?<!href=")(?<!src=")((?:https?://|www\.)[^\s<>"\'\(\)]+)')
    for element in soup.find_all(string=True):
        if element.parent.name not in ['a', 'script', 'style']:
            new_html = url_pattern.sub(r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>', str(element))
            new_html = new_html.replace('<a href="www.', '<a href="https://www.')
            element.replace_with(BeautifulSoup(new_html, 'html.parser'))
    for p_tag in soup.find_all('p'):
        if '개인의견:' in p_tag.get_text():
            p_tag['style'] = 'font-style: italic;'
            if p_tag.em: p_tag.em.unwrap()
    return soup


# ==============================================================================
# ✨ [핵심 수정] 전체 작업 흐름을 제어하는 메인 함수
# ==============================================================================
def markdown_to_html(content):
    """
    본문 내용에 포함된 간단한 마크다운(리스트, 테이블, 볼드)을 HTML로 변환합니다.
    """
    # ✅ 1. **text** => <strong>text</strong> 변환
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)

    lines = content.strip().split('\n')
    html_output = []
    in_list = False
    in_table = False

    for line in lines:
        line = line.strip()

        # ✅ 2. 문장 시작의 '*' 리스트 마커만 처리하고, 문장 내의 '*'는 제거
        if line.startswith('* '):
            if not in_list:
                html_output.append("<ul>")
                in_list = True
            # 나머지 문장에서 불필요한 '*' 제거
            clean_line = line[2:].strip().replace('*', '')
            html_output.append(f"<li>{clean_line}</li>")
            continue
        elif in_list:
            html_output.append("</ul>")
            in_list = False

        # 테이블 처리
        if line.startswith('|') and line.endswith('|'):
            if not in_table:
                html_output.append("<table><tbody>")
                in_table = True
            if all(c in '-| ' for c in line): continue
            cells = [cell.strip().replace('*', '') for cell in line.split('|')[1:-1]]
            row_html = "".join([f"<td>{cell}</td>" for cell in cells])
            html_output.append(f"<tr>{row_html}</tr>")
            continue
        elif in_table:
            html_output.append("</tbody></table>")
            in_table = False

        # 일반 문단 처리 (불필요한 '*' 제거)
        if line:
            html_output.append(f"<p>{line.replace('*', '')}</p>")

    if in_list: html_output.append("</ul>")
    if in_table: html_output.append("</tbody></table>")

    return "\n".join(html_output)


def life_tips_start(article, keyword):
    """
    초안을 받아 제목 생성, 콘텐츠 분업 생성, 최종 조립 및 발행을 총괄하는 메인 함수
    """
    if not wp:
        print("❌ WordPress 클라이언트가 설정되지 않아 포스팅을 중단합니다.")
        return

    # 1. 매력적인 제목 생성
    title_options = generate_impactful_titles(keyword, article[:400])
    final_title = title_options[0]
    print(f"👑 선택된 최종 제목: {final_title}")

    # 2. 이미지 생성 및 업로드
    short_slug = slugify(keyword)[:50]
    thumb_media = stable_diffusion(article, "thumb", f"{final_title}", short_slug)
    thumbnail_id = wp.call(UploadFile(thumb_media)).get("id") if thumb_media else None
    scene_media = stable_diffusion(article, "scene", f"{final_title}", short_slug)
    scene_url = wp.call(UploadFile(scene_media)).get("link") if scene_media else ""

    # 3. 분업 및 조립 프로세스
    structured_content = generate_structured_content_json(article, keyword)
    if not structured_content:
        print("❌ 본문 JSON 데이터 생성에 실패하여 포스팅을 중단합니다.")
        return

    plain_text_content = " ".join(
        [s.get('title', '') + " " + s.get('content', '') for s in structured_content.get('sections', [])])

    meta_description = generate_meta_description(plain_text_content, keyword)
    json_ld_content = generate_json_ld_faq(plain_text_content)

    # 4. 파이썬 코드가 '데이터'를 기반으로 100% 완벽한 HTML 조립
    print("▶ (최종 조립) 모든 데이터를 하나의 HTML로 결합합니다.")

    body_html_parts = []
    for section in structured_content.get('sections', []):
        title = section.get('title', '')
        content = section.get('content', '')
        body_html_parts.append(f"<h2>{title}</h2>")
        body_html_parts.append(markdown_to_html(content))

    body_html_parts.append(f"<p><strong>한줄요약:</strong> {structured_content.get('summary', '')}</p>")
    body_html_parts.append(f"<p style='font-style: italic;'>개인의견: {structured_content.get('opinion', '')}</p>")
    final_body_html_str = "".join(body_html_parts)

    soup = BeautifulSoup(final_body_html_str, 'html.parser')
    toc_html = create_table_of_contents(soup)

    json_ld_script = f'<script type="application/ld+json">\n{json_ld_content}\n</script>' if json_ld_content else ""

    # ✅ 5. 최종 HTML 결합 시, 이미지 태그에 'aligncenter' 클래스를 확실하게 적용
    img_html = f"<figure class='wp-block-image aligncenter size-large'><img src='{scene_url}' alt='{keyword}'/></figure>" if scene_url else ""
    final_body_content = soup.decode_contents()

    final_html = f"""{json_ld_script}
<meta name="description" content="{meta_description.replace('"', ' ')}">
{img_html}
{toc_html}
{final_body_content}
"""

    # 6. 태그 추출 및 워드프레스 발행
    auto_tags = extract_tags_from_html_with_gpt(final_body_html_str, keyword)

    post = WordPressPost()
    post.title = final_title
    post.content = final_html
    post.excerpt = meta_description
    post.terms_names = {
        'category': [safe_term_cate(CATEGORY)],
        'post_tag': list(set([safe_term_word(keyword)] + [safe_term_word(t) for t in auto_tags]))
    }
    if thumbnail_id: post.thumbnail = thumbnail_id
    post.post_status = 'publish'

    if not final_title or not final_html or len(final_html.strip()) < 500:
        print("❌ 콘텐츠 품질이 낮아 업로드를 중단합니다.")
    else:
        try:
            post_id = wp.call(NewPost(post))
            print("==========================================================")
            print(f"✅ 게시 완료! (Post ID: {post_id}) - 제목: {final_title}")
            print("==========================================================")
        except Exception as e:
            print(f"❌ 워드프레스 발행 중 오류 발생: {e}")

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


# ==============================================================================
# [최종 강화판] SEO 요소를 모두 통합하여 생성하는 함수
# ==============================================================================
def postprocess_and_refine_html(html_text):
    """
    Gemini가 생성한 HTML의 구조적 오류를 보정하는 후처리 함수
    """
    from bs4 import BeautifulSoup
    import re

    if not html_text:
        return ""

    # 1. 마크다운 형식의 볼드체를 <strong> 태그로 변환
    html_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_text)

    soup = BeautifulSoup(html_text, 'html.parser')

    # 2. <p><strong>숫자. ...</strong></p> 같은 패턴을 <h2> 태그로 변환
    for p_tag in soup.find_all('p'):
        # strong 태그가 첫 자식인 경우만 고려하여 안정성 확보
        if p_tag.strong and p_tag.get_text(strip=True).startswith(p_tag.strong.get_text(strip=True)):
            text = p_tag.get_text(strip=True)
            # "숫자." 또는 "숫자)" 로 시작하는 패턴 감지
            if re.match(r'^\d+[\.\)]\s*', text):
                print(f"✅ HTML 구조 보정: '{text}' -> <h2>")
                h2_tag = soup.new_tag('h2')
                # "1. " 같은 앞부분을 제거하고 순수 텍스트만 h2에 넣기
                h2_tag.string = re.sub(r'^\d+[\.\)]\s*', '', text)
                p_tag.replace_with(h2_tag)

    return str(soup)


def optimize_html_for_seo_with_gpt(article, keyword, main_image_url=""):
    """
    초안을 받아 SEO에 최적화된 최종 HTML을 생성하고,
    결과물의 HTML 구조를 코드 레벨에서 강력하게 보정합니다.
    """
    from bs4 import BeautifulSoup, NavigableString
    from slugify import slugify
    import json
    import re

    print("▶ Gemini로 SEO 요소 전체 최적화 작업 시작...")

    # 1. 강화된 프롬프트로 Gemini에게 HTML 구조화 요청
    prompt = f"""
    [역할]
    당신은 HTML 구조화에 매우 능숙한 전문 기술 작가입니다.
    [엄격한 HTML 규칙]
    1.  **소제목 규칙**: 주요 섹션을 나누는 소제목은 **반드시 `<h2>` 태그**로 감싸야 합니다.
    2.  **목록/표 규칙**: 항목 나열은 `<ul>`, 데이터 정리는 `<table>`을 사용하세요. 각 `<h2>` 섹션마다 최소 1개 이상의 목록 또는 표를 포함해야 합니다.
    3.  **마무리 형식**: 글 마지막에 `<p><strong>한줄요약:</strong> ...</p>`과 `<p><em>개인의견:</em> ...</p>`을 순서대로 추가하세요.
    4.  **출력 형식**: 다른 설명 없이, 최종 결과물은 순수 HTML 코드여야 합니다.
    5.  **[절대 금지]**: `<html>`, `<head>`, `<body>`, `<!DOCTYPE html>` 태그는 절대 포함하지 마세요.
    [초안 내용]
    {article}
    """
    generated_html_raw = call_gemini(prompt, temperature=0.5)
    if not generated_html_raw:
        print("❌ Gemini로부터 HTML을 생성하지 못했습니다.")
        return ""

    # 2. 코드 자동 보정: AI의 실수를 교정하는 안전장치
    print("▶ 생성된 HTML 구조를 코드로 최종 보정합니다...")
    soup = BeautifulSoup(generated_html_raw, 'html.parser')
    if soup.body:
        body_content_html = soup.body.decode_contents()
    else:
        body_content_html = generated_html_raw
    refined_html = postprocess_and_refine_html(body_content_html)
    soup = BeautifulSoup(refined_html, 'html.parser')

    # 3. 목차, 메타 정보 등 추가
    toc_list = []
    h2_tags = soup.find_all('h2')
    for i, h2 in enumerate(h2_tags, 1):
        title_text = h2.get_text(strip=True)
        slug_id = slugify(title_text) if slugify(title_text) else f"section-{i}"
        h2['id'] = slug_id
        toc_list.append(f'<li><a href="#{slug_id}">{title_text}</a></li>')
    toc_html = f'<h2>목차</h2><ul class="table-of-contents">{"".join(toc_list)}</ul>' if toc_list else ""

    meta_prompt = f"다음 블로그 글의 핵심 내용을 SEO에 최적화하여 120자 내외의 흥미로운 '메타 디스크립션'으로 요약해줘. 반드시 한 개의 최종 문장으로만 응답해야 해.\n[본문]\n{soup.get_text(strip=True, separator=' ')[:1000]}"
    meta_description_raw = call_gemini(meta_prompt, temperature=0.5)
    meta_description = meta_description_raw.split('\n')[
        0].strip() if meta_description_raw else f"{keyword}에 대한 모든 정보를 확인하세요."

    # ✅ 4. JSON-LD 생성 로직 (안정성 강화 버전)
    faq_prompt = f"""
    [지시]
    다음 블로그 글의 내용을 바탕으로 SEO에 유용한 FAQ 3~4개를 만들어줘.

    [가장 중요한 규칙]
    - **반드시 순수한 JSON 객체 형식으로만 응답해야 합니다.**
    - `<script>` 태그, 설명, 마크다운 등 다른 텍스트는 절대 포함하지 마세요.
    - 아래의 'JSON 출력 구조 예시'를 반드시 정확히 따라야 합니다.

    [JSON 출력 구조 예시]
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {{
          "@type": "Question",
          "name": "질문 1 텍스트",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "답변 1 텍스트"
          }}
        }},
        {{
          "@type": "Question",
          "name": "질문 2 텍스트",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "답변 2 텍스트"
          }}
        }}
      ]
    }}

    [블로그 내용]
    {soup.get_text(strip=True, separator=' ')[:2000]}
    """
    json_ld_content_raw = call_gemini(faq_prompt, temperature=0.2, is_json=True)
    json_ld_script = ""

    if json_ld_content_raw:
        try:
            # ✅ 1. 실제 JSON으로 파싱 시도 (가장 확실한 검증)
            parsed_json = json.loads(json_ld_content_raw)

            # ✅ 2. 필수 키(mainEntity)가 존재하는지 구조 검증
            if isinstance(parsed_json, dict) and 'mainEntity' in parsed_json:
                print("✅ 유효한 JSON-LD 콘텐츠 생성 완료, <script> 태그로 래핑합니다.")
                # 가독성을 위해 json.dumps로 다시 예쁘게 포맷팅
                json_ld_content = json.dumps(parsed_json, indent=2, ensure_ascii=False)
                json_ld_script = f'<script type="application/ld+json">\n{json_ld_content}\n</script>'
            else:
                print("⚠️ JSON 파싱은 성공했으나, 필수 키('mainEntity')가 누락되었습니다.")

        except json.JSONDecodeError:
            # ✅ 3. JSON 파싱 자체에 실패할 경우 예외 처리
            print("⚠️ Gemini가 유효하지 않은 JSON 형식을 반환했습니다.")
            print(f"   - 원본 응답: {json_ld_content_raw[:100]}...")
    else:
        print("⚠️ 유효한 JSON-LD 콘텐츠를 생성하지 못했습니다.")

    # 5. URL 자동 링크 및 '개인의견' 스타일링
    url_pattern = re.compile(r'(?<!href=")(?<!src=")((?:https?://|www\.)[^\s<>"\'\(\)]+)')
    for element in soup.find_all(string=True):
        if isinstance(element, NavigableString) and element.parent.name not in ['a', 'script', 'style']:
            new_html = url_pattern.sub(r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>', str(element))
            new_html = new_html.replace('<a href="www.', '<a href="https://www.')
            element.replace_with(BeautifulSoup(new_html, 'html.parser'))

    for p_tag in soup.find_all('p'):
        if '개인의견:' in p_tag.get_text():
            p_tag['style'] = 'font-style: italic;'
            if p_tag.em:
                p_tag.em.unwrap()
            break

    # 6. 최종 HTML 조립
    img_html = f"<figure class='wp-block-image aligncenter size-large'><img src='{main_image_url}' alt='{keyword}'/></figure>" if main_image_url else ""
    body_content = soup.decode_contents()

    final_html = f"""{json_ld_script}
<meta name="description" content="{meta_description.replace('"', ' ')}">
{img_html}
{toc_html}
{body_content}
"""

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
    print("📌 최신 글 20개 제목을 가져옵니다. gas")
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


def suggest_life_tip_topic_issue(kw):
    from openai import OpenAI
    import variable as v_

    from datetime import datetime
    today = datetime.today().strftime("%Y년 %m월 %d일")
    month = datetime.today().month


    suggest__ = False

    if "none" in v_.wd_id:
        print("v_.wd_id", v_.wd_id)
    elif "none" in v_.wd_pw:
        print("v_.wd_pw", v_.wd_pw)
    elif "none" in v_.api_key:
        print("v_.api_key", v_.api_key)
    elif "none" in v_.domain_adress:
        print("v_.domain_adress", v_.domain_adress)
    elif "none" in v_.my_category:
        print("v_.my_category", v_.my_category)

    else:
        print("▶ suggest_life_tip_topic_issue", kw)

        # 기존 제목 가져오기
        result_titles = load_existing_titles()

        # 중복 주제 여부 판단
        score = is_similar_topic(kw, result_titles)
        if score < 70:
            print(f"✅ 주제 선정: '{kw}' (유사도: {score}%)")
            life_tips_keyword(kw)
            return True  # 포스팅 1개 작성 후 종료
        else:
            print(f"⚠️ 유사 주제 건너뛰기: '{kw}' (유사도: {score}%)")

    return suggest__