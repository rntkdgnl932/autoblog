# 🔄 [Gemini 2.5 Pro 최종 버전] 자동 블로그 업로드 스크립트
# 모델: Gemini 2.5 Pro 전면 사용

import requests
import base64
import json
import re
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from PyQt5.QtTest import QTest
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.media import UploadFile
from bs4 import BeautifulSoup
from slugify import slugify
from datetime import datetime
from blog_function import call_gemini, stable_diffusion


import variable as v_

# ---- Windows 콘솔 UTF-8 강제 (한글 로그/데이터 안전) ----
import sys, os
if os.name == "nt":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass



# wp = Client(f"{v_.domain_adress}/xmlrpc.php", v_.wd_id, v_.wd_pw)

_wp_client = None
def get_wp():
    global _wp_client
    if _wp_client:
        return _wp_client
    try:
        _wp_client = Client(f"{v_.domain_adress}/xmlrpc.php", v_.wd_id, v_.wd_pw)
        return _wp_client
    except Exception as e:
        print(f"❌ WordPress 연결 실패: {e}", flush=True)
        return None


CATEGORY = v_.my_category if hasattr(v_, 'my_category') else "일반"





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
# def stable_diffusion(article, filename, description, slug):
#     """
#     [최종 수정] article 요약 프롬프트 추가 및 AI 실패 시 대체 프롬프트 사용 로직 추가
#     """
#     try:
#         print(f"▶ Gemini로 [{filename}] 이미지 프롬프트 및 캡션 동시 생성 요청...")
#
#         # ... (style_guideline, ENHANCED_NEGATIVE 등은 이전과 동일) ...
#         if filename == "thumb":
#             style_guideline = "- 스타일: **미니멀리즘, 플랫 디자인, 벡터 아트**\n- 구성: 주제를 상징적으로 표현하는 아이콘 또는 오브젝트 중심"
#         elif filename == "scene":
#             style_guideline = "- 스타일: **극사실적, 고품질 사진**\n- 구성: 주제의 개념이나 상황을 은유적으로 묘사\n- 조명/배경: 자연광 또는 cinematic lighting, 배경 흐림(depth of field)"
#         else:
#             style_guideline = "- 스타일: 고품질의 상징적인 사진"
#
#         # ✅ 1. article 요약 내용이 추가된, 개선된 프롬프트
#         meta_prompt = f"""
#         [역할] 당신은 추상적인 개념을 시각적으로 구현하는 데 능숙한 AI 이미지 프롬프트 엔지니어이자 카피라이터입니다.
#         [지시] 아래 '글 요약'과 '주제'를 참고하여 Stable Diffusion용 'image_prompt'와 블로그 독자용 'caption'을 생성해주세요.
#         [가장 중요한 규칙]
#         - 인물보다 주제를 가장 잘 상징하는 사물, 풍경, 추상적인 이미지로 자연스럽게 표현하세요.
#         - 프롬프트에 글자(Text)가 포함되면 안 됩니다.
#         [스타일 가이드] {style_guideline}
#         [출력 형식]
#         - 반드시 {{"image_prompt": "...", "caption": "..."}} 형식의 순수 JSON으로만 응답해야 합니다.
#         [글 요약] {article[:500]}
#         [주제] {description}
#         """
#
#         response_text = call_gemini(meta_prompt, temperature=0.7, is_json=True)
#
#         # ✅ 2. AI 프롬프트 생성 실패 시 '대체 프롬프트' 사용
#         try:
#             # API 호출 자체가 실패했는지 먼저 확인
#             if response_text in ["SAFETY_BLOCKED", "API_ERROR"] or not response_text:
#                 raise ValueError(f"API 호출 실패: {response_text}")
#
#             # 성공 시, JSON 파싱 시도
#             parsed_data = json.loads(response_text)
#             short_prompt = parsed_data.get("image_prompt")
#             image_caption = parsed_data.get("caption")
#
#             # 파싱된 데이터에 필수 키가 있는지 확인
#             if not all([short_prompt, image_caption]):
#                 raise ValueError("JSON 결과물에 필수 키가 누락되었습니다.")
#
#         except Exception as e:
#             # API 호출 실패 또는 JSON 파싱/검증 실패 시 모두 여기서 처리
#             print(f"⚠️ AI 프롬프트/캡션 생성 실패({e}). 대체 프롬프트를 사용합니다.")
#             short_prompt = f"{description.replace(' ', ', ')}, symbolic, high quality, photorealistic"
#             image_caption = description
#
#         print(f"🖼 생성된 프롬프트: {short_prompt}")
#         print(f"✍️ 생성된 캡션: {image_caption}")
#
#         ENHANCED_NEGATIVE = "(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, (mutated hands and fingers:1.4), ugly, blurry, (text, watermark, signature)"
#
#         final_prompt = f"masterpiece, best quality, 8k, ultra high res, {short_prompt}"
#         payload = {"prompt": final_prompt, "negative_prompt": ENHANCED_NEGATIVE, "steps": 30, "width": 512,
#                    "height": 512, "sampler_index": "Euler a", "cfg_scale": 7.5}
#
#         response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload, timeout=300)
#         response.raise_for_status()
#
#         b64_image = response.json()['images'][0]
#         image_bytes = base64.b64decode(b64_image)
#
#         img = Image.open(BytesIO(image_bytes)).convert("RGB")
#         buf = BytesIO()
#         img.save(buf, format="WEBP", quality=85)
#         image = BytesIO(buf.getvalue())
#         image.name = f"{slug}_{filename}.webp"
#         image.seek(0)
#
#         media = {
#             'name': image.name,
#             'type': 'image/webp',
#             'caption': image_caption,
#             'description': description,
#             'bits': xmlrpc_client.Binary(image.read())
#         }
#         return (media, image_caption)
#
#     except Exception as e:
#         print(f"⚠️ Stable Diffusion 처리 중 예외 발생: {e}")
#         return (None, None)


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
    wp = get_wp()
    if not wp:
        print("❌ WordPress 클라이언트를 얻지 못해 중단합니다.")
        return False

    """초안 생성 후 life_tips_start를 호출하고 그 결과를 반환"""

    today = datetime.today().strftime("%Y년 %m월 %d일")

    print(f"▶ 키워드 '{keyword}'로 본문 초안 생성 요청")
    prompt = f"""
    [역할]
    당신은 '{getattr(v_, 'my_topic', '생활 정보')}' 분야의 전문 작가이자 사실 확인 전문가입니다. 당신의 임무는 독자들이 신뢰할 수 있는 정확하고 깊이 있는 정보로 구성된 블로그 초안을 작성하는 것입니다.
    [지시]
    '{keyword}'라는 주제에 대해, 아래 규칙을 모두 준수하여 블로그 포스팅을 위한 상세한 '초안'을 작성해주세요.
    [작성 규칙]
    1. **정보의 정확성:** 모든 정보는 {today} 현재 유효한 것이어야 합니다. 기관명, 정책명, 통계 수치는 실제 존재하는 공식적인 정보를 기반으로 작성하세요.
    2. **내용의 구체성:** 추상적인 설명 대신, 독자들이 바로 활용할 수 있는 구체적인 조건, 수치, 방법, 예시를 풍부하게 포함해주세요.
    3. **구조적 글쓰기:** 서론-본론-결론의 구조를 갖추고, 본론은 3~4개의 명확한 소주제로 나누어 각 소주제별로 내용을 상세히 서술해주세요.
    4. **출력 형식:** **가장 중요합니다. 절대 HTML 태그를 사용하지 말고, 오직 '일반 텍스트'로만** 작성해주세요.
    """
    article_result = call_gemini(prompt, temperature=0.7)

    if article_result in ["SAFETY_BLOCKED", "API_ERROR"] or not article_result:
        print(f"❌ 초안 생성 실패({article_result}). 다음 키워드로 넘어갑니다.")
        return False

    # life_tips_start가 True 또는 False를 반환하면, 그 값을 그대로 상위 루프에 전달
    return life_tips_start(article_result.replace("```html", "").replace("```", "").strip(), keyword)

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
    4.  **강력한 단어:** '총정리', '필수', '비법' 등 임팩트 있는 단어를 사용하여 전문성을 어필하라.
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
    """(AI 역할) 초안을 받아 '비교분석', '경험' 등을 추가하여 전문가 수준의 'JSON 데이터'로 재구성"""
    print("▶ (AI 작업 2/6) 본문 JSON 데이터 생성 중...")
    #      {getattr(v_, 'my_topic', '생활 정보')}
    prompt = f"""
    [역할]
    당신은 '{v_.my_topic}' 분야의 15년차 전문 블로거이자 SEO 콘텐츠 전략가입니다. 당신의 임무는 주어진 '초안'을 독자에게 독보적인 가치를 제공하는 전문가 콘텐츠로 재탄생시키는 것입니다.
    또한, 특정 주제에 대해 매우 깊이 있는 지식을 가진 전문 작가이자, E-E-A-T(경험, 전문성, 권위, 신뢰성)를 고려하여 SEO 콘텐츠를 작성하는 전략가입니다.

    
    [지시]
    '{keyword}'를 주제로 한 아래 '초안'을 바탕으로, 다음 [필수 포함 요소]를 모두 반영하여 'JSON 출력 구조'에 맞춰 콘텐츠를 재구성해주세요.

    [필수 포함 요소]
    1.  **독창적 분석:** 주제와 관련된 여러 방법이나 옵션이 있다면, 장단점을 비교하는 '유형별 비교 분석' 표(Table)를 반드시 포함하세요.
    2.  **개인 경험(E-E-A-T):** 본문 내용과 관련된 당신의 짧은 경험담이나 실제 사례를 1인칭 시점("제가 직접 해보니...")으로 자연스럽게 녹여내세요.
    - "제가 직접 해보니..." 는 단순 예시일 뿐, 본문 내용 흐름에 맞춰 팁이 될 내용을 적어주세요.
    3.  **전문가 팁 & 주의사항:** 독자들이 놓치기 쉬운 '전문가의 꿀팁'이나 '주의사항' 섹션을 구체적으로 추가하여 신뢰도(T)를 높이세요.
    4.  **구조화:** 전체 내용은 서론, 3~4개의 소주제를 명확하게 구분해주세요.

    [콘텐츠 생성 원칙]
    1.  **소제목(title) 작성:** 독자가 검색할 만한 핵심 키워드를 중심으로, 간결하고 명확하게 작성하세요.
    2.  **서론 강화:** 독자의 흥미를 유발하는 도입부와 함께, 이 글을 통해 무엇을 얻을 수 있는지 알려주는 핵심 요약 목록(bullet points)을 서론 내용에 포함해주세요.
    - 제목에 '서론', '본론', '결론' 이라는 단어 지양
    3.  **독창적 분석(content):** 단순 정보 나열을 피하세요.
        - 만약 주제에 여러 선택지나 유형이 있다면, **장단점을 비교하는 '비교 분석표'**를 포함하세요.
        - 만약 주제가 어떤 절차나 방법을 설명한다면, **구체적인 '단계별 가이드'**를 제시하세요.
        - 만약 주제가 특정 정책이나 사건이라면, 그 **'배경과 영향'**을 깊이 있게 설명하세요.
    4.  **신뢰도 향상(E-E-A-T):** 본문 내용 중 한 곳에, 주제와 관련된 당신의 짧은 **1인칭 경험담("제가 직접 해보니...")**을 자연스럽게 삽입하세요. 또한, 독자들이 놓치기 쉬운 **'전문가의 팁' 또는 '주의사항'**을 구체적으로 추가하세요.


    [JSON 출력 구조]
    {{
      "sections": [
        {{
          "title": "서론에 해당하는 소제목",
          "content": "서론 본문입니다. 목록이 필요하면 * 항목 형식으로 작성해주세요."
        }},
        {{
          "title": "비교 분석표가 포함된 소제목",
          "content": "비교 분석 본문입니다. 표는 | 헤더1 | 헤더2 |\\n|---|---|\\n| 내용1 | 내용2 | 형식으로 작성해주세요."
        }}
      ],
      "summary": "글 전체를 요약하는 한 문장입니다.",
      "opinion": "전문가로서의 팁이나 직설적인 개인 의견입니다."
    }}

    [가장 중요한 규칙]
    - **절대 HTML 태그를 사용하지 마세요.**
    - 출력은 다른 설명 없이, 오직 위에서 설명한 JSON 형식이어야 합니다.

    [초안 내용]
    {article}
    """
    json_response = call_gemini(prompt, temperature=0.7, is_json=True)
    if json_response in ["SAFETY_BLOCKED", "API_ERROR"] or not json_response:
        return json_response if json_response else "API_ERROR"
    try:
        return json.loads(json_response)
    except:
        return "API_ERROR"

def generate_meta_description(content_text, keyword):
    """(분업 2) 본문 텍스트를 기반으로 메타 디스크립션을 생성"""
    print("  ▶ (분업 2) Gemini로 메타 디스크립션 생성 중...")
    prompt = f"다음 글을 SEO에 최적화하여 120자 내외의 흥미로운 '메타 디스크립션'으로 요약해줘. 반드시 한 문장의 순수 텍스트만 출력해야 해.\n\n[본문 요약]\n{content_text[:1000]}"
    desc = call_gemini(prompt, temperature=0.5)
    return desc if desc not in ["SAFETY_BLOCKED", "API_ERROR"] else "API_ERROR"


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
    if json_content in ["SAFETY_BLOCKED", "API_ERROR"] or not json_content:
        return json_content if json_content else "API_ERROR"
    try:
        parsed_json = json.loads(json_content)
        # if isinstance(parsed_json, dict) and 'mainEntity' in parsed_json:
        #     return json.dumps(parsed_json, indent=2, ensure_ascii=False)
        if isinstance(parsed_json, dict) and 'mainEntity' in parsed_json:
            # 한 줄(JSON minify): 줄바꿈이 없으니 <br>로 안 바뀝니다.
            return json.dumps(parsed_json, ensure_ascii=False, separators=(",", ":"))

        return "API_ERROR"
    except:
        return "API_ERROR"



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
    url_pattern = re.compile(r'(?<!href=")(?<!src=")((?:https?://|www\.)[^\s<>"\'()]+)')
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
    마크다운(리스트, 볼드, 테이블+캡션)을 HTML로 변환합니다.
    """
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    lines = content.strip().split('\n')
    html_output = []
    in_list = False
    in_table = False
    table_caption = None

    for line in lines:
        line = line.strip()

        # ✅ 1. [표 제목]: 패턴을 감지하여 캡션으로 저장
        if line.startswith('[표 제목]:'):
            table_caption = line.replace('[표 제목]:', '').strip()
            continue

        # 리스트 처리
        if line.startswith('* '):
            if not in_list:
                html_output.append("<ul>")
                in_list = True
            html_output.append(f"<li>{line[2:].strip().replace('*', '')}</li>")
            continue
        elif in_list:
            html_output.append("</ul>")
            in_list = False

        # 테이블 처리
        # 테이블 처리 부분 교체
        if line.startswith('|') and line.endswith('|'):
            if not in_table:
                html_output.append("<table>")
                if table_caption:
                    html_output.append(f"<caption>{table_caption}</caption>")
                    table_caption = None
                html_output.append("<tbody>")
                in_table = True

            # 구분선 라인 건너뛰기
            if re.match(r'^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|$', line):
                continue

            cells = [cell.strip().replace('*', '') for cell in line.split('|')[1:-1]]

            # 첫 데이터 행을 헤더로 간주(간단 규칙)
            if (len(html_output) >= 1 and
                    html_output[-1].endswith("<tbody>") and
                    not any(tag in html_output[-1] for tag in ("<tr>", "<td>", "<th>"))):
                row_html = "".join([f"<th>{c}</th>" for c in cells])
            else:
                row_html = "".join([f"<td>{c}</td>" for c in cells])
            html_output.append(f"<tr>{row_html}</tr>")
            continue

        elif in_table:
            html_output.append("</tbody></table>")
            in_table = False

        # 일반 문단 처리
        if line:
            html_output.append(f"<p>{line.replace('*', '')}</p>")

    if in_list: html_output.append("</ul>")
    if in_table: html_output.append("</tbody></table>")

    return "\n".join(html_output)

def pick_best_title(candidates, keyword):
    def score(t):
        s = 0
        tl = len(t)
        if keyword in t: s += 20
        if 28 <= tl <= 42: s += 15
        if re.search(r"\d", t): s += 5   # 숫자
        if any(w in t for w in ["비법","꿀팁","총정리","완벽","필수"]): s += 5
        if any(w in t for w in ["클릭","후기","내돈내산"]): s -= 5
        return s
    return sorted(candidates, key=lambda x: score(x), reverse=True)[0]

def extract_tags_fallback(html, keyword):
    text = BeautifulSoup(html, "html.parser").get_text(" ")
    words = re.findall(r"[가-힣A-Za-z0-9]{2,}", text)
    stops = set([keyword, "한줄요약", "개인의견"])
    freq = {}
    for w in words:
        if w.lower() in stops or len(w) > 20:
            continue
        freq[w] = freq.get(w, 0) + 1
    return [w for w,_ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:7]]


def life_tips_start(article, keyword):
    """
    [최종 안정화 버전] 모든 체크포인트와 본문 조립 로직이 포함된 완전한 함수
    """
    wp = get_wp()
    if not wp:
        print("❌ WordPress 클라이언트를 얻지 못해 중단합니다.")
        return False

    # === 체크포인트 1: 제목 생성 ===
    title_options_result = generate_impactful_titles(keyword, article[:400])
    if not isinstance(title_options_result, list):
        print(f"❌ 제목 생성 실패({title_options_result}). 포스팅 중단.")
        return False
    final_title = pick_best_title(title_options_result, keyword)
    print(f"👑 선택된 최종 제목: {final_title}")

    # === 체크포인트 2: 본문 JSON 데이터 생성 ===
    structured_content = generate_structured_content_json(article, keyword)
    if not isinstance(structured_content, dict):
        print(f"❌ 본문 데이터 생성 실패({structured_content}). 포스팅 중단.")
        return False

    # === 체크포인트 3: 썸네일/본문 이미지 생성 ===
    short_slug = slugify(keyword)[:50]

    thumb_media, _ = stable_diffusion(article, "thumb", f"{final_title}", short_slug)
    if thumb_media is None:
        print("⚠️ 썸네일 생성 실패 → 대체 이미지 사용")
        thumb_media = {
            "name": "fallback_thumb.webp",
            "type": "image/webp",
            "caption": final_title,
            "description": final_title,
            "bits": xmlrpc_client.Binary(open(v_.fallback_thumb_path, "rb").read())
        }
    thumbnail_id = wp.call(UploadFile(thumb_media)).get("id")

    scene_media, scene_caption = stable_diffusion(article, "scene", f"{final_title}", short_slug)
    if scene_media is None:
        print("⚠️ 본문 이미지 생성 실패 → 대체 이미지 사용")
        scene_path = v_.fallback_scene_path
        scene_media = {
            "name": "fallback_scene.webp",
            "type": "image/webp",
            "caption": final_title,
            "description": final_title,
            "bits": xmlrpc_client.Binary(open(scene_path, "rb").read())
        }
    scene_url = wp.call(UploadFile(scene_media)).get("link")

    # === 체크포인트 4: 메타정보 생성 ===
    plain_text_content = " ".join(
        [s.get('title', '') + " " + s.get('content', '') for s in structured_content.get('sections', [])])

    meta_description = generate_meta_description(plain_text_content, keyword)
    if meta_description in ["SAFETY_BLOCKED", "API_ERROR"]:
        print(f"❌ 메타 디스크립션 생성 실패({meta_description}). 포스팅 중단.")
        return False

    json_ld_content = generate_json_ld_faq(plain_text_content)
    if json_ld_content in ["SAFETY_BLOCKED", "API_ERROR"] or not json_ld_content:
        print(f"❌ JSON-LD 생성 실패({json_ld_content}). 포스팅 중단.")
        return False

    # === 모든 생성 작업 성공! 최종 조립 및 발행 ===
    print("✅ 모든 AI 콘텐츠 생성 성공! 최종 조립 및 발행을 시작합니다.")

    # ✅ [핵심 복원] 본문 조립 로직
    body_html_parts = []
    for section in structured_content.get('sections', []):
        body_html_parts.append(f"<h2>{section.get('title', '')}</h2>")
        body_html_parts.append(markdown_to_html(section.get('content', '')))
    body_html_parts.append(f"<p><strong>한줄요약:</strong> {structured_content.get('summary', '')}</p>")
    body_html_parts.append(f"<p style='font-style: italic;'>개인의견: {structured_content.get('opinion', '')}</p>")
    final_body_html_str = "".join(body_html_parts)

    soup = BeautifulSoup(final_body_html_str, 'html.parser')
    toc_html = create_table_of_contents(soup)
    # json_ld_content 가 dict/str 섞여 올 수 있으니 안전 처리
    try:
        _json_obj = json.loads(json_ld_content) if isinstance(json_ld_content, str) else json_ld_content
        json_ld_min = json.dumps(_json_obj, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        json_ld_min = str(json_ld_content).strip().replace("\n", "")

    # 구텐베르크 HTML 블록 래핑 + 개행 제거된 스크립트
    json_ld_script = (
        '<!-- wp:html -->'
        f'<script type="application/ld+json">{json_ld_min}</script>'
        '<!-- /wp:html -->'
    )

    # figcaption_html = f"<figcaption>{scene_caption}</figcaption>" if scene_caption else ""
    # img_html = f"<figure class='wp-block-image aligncenter size-large'><img src='{scene_url}' alt='{keyword}'/>{figcaption_html}</figure>"
    # 캡션이 없을 경우를 대비하여 final_title을 대체값으로 사용
    final_alt_text = scene_caption if scene_caption else final_title
    figcaption_html = f"<figcaption>{scene_caption}</figcaption>" if scene_caption else ""
    # img_html = f"<figure class='wp-block-image aligncenter size-large'><img src='{scene_url}' alt='{final_alt_text.replace('"', '')}'/>{figcaption_html}</figure>"
    from html import escape

    safe_alt = escape((final_alt_text or "").strip(), quote=True)

    img_html = (
        '<figure class="wp-block-image aligncenter size-large">'
        f'<img src="{scene_url}" alt="{safe_alt}"/>{figcaption_html}</figure>'
    )

    final_body_content = soup.decode_contents()

    meta_attr = (meta_description or "").replace('"', ' ').strip()

    final_html = f"""{json_ld_script}
    <meta name="description" content="{meta_attr}">
    {img_html}
    {toc_html}
    {final_body_content}
    """.strip()

    #     final_html = f"""{json_ld_script}
# <meta name="description" content="{meta_description.replace('"', ' ')}">
# {img_html}
# {toc_html}
# {final_body_content}
# """

    # === 체크포인트 5: 태그 추출 ===
    auto_tags = extract_tags_from_html_with_gpt(final_html, keyword)
    if not isinstance(auto_tags, list):
        print("⚠️ 태그 추출 실패 → 로컬 백업 사용")
        auto_tags = extract_tags_fallback(final_html, keyword)

    # (발행 로직)
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

    try:
        post_id = wp.call(NewPost(post))
        print("==========================================================")
        print(f"✅ 게시 완료! (Post ID: {post_id}) - 제목: {final_title}")
        print("==========================================================")
        return True
    except Exception as e:
        print(f"❌ 워드프레스 발행 중 오류 발생: {e}")
        return False

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
    if response_text in ["SAFETY_BLOCKED", "API_ERROR"] or not response_text:
        return response_text if response_text else "API_ERROR"
    try:
        tags = json.loads(response_text)
        return tags if isinstance(tags, list) else "API_ERROR"
    except:
        return "API_ERROR"


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
                json_ld_content = json.dumps(parsed_json, ensure_ascii=False, separators=(",", ":"))
                # json_ld_content 가 dict/str 섞여 올 수 있으니 안전 처리
                try:
                    _json_obj = json.loads(json_ld_content) if isinstance(json_ld_content, str) else json_ld_content
                    json_ld_min = json.dumps(_json_obj, ensure_ascii=False, separators=(",", ":"))
                except Exception:
                    json_ld_min = str(json_ld_content).strip().replace("\n", "")

                # 구텐베르크 HTML 블록 래핑 + 개행 제거된 스크립트
                json_ld_script = (
                    '<!-- wp:html -->'
                    f'<script type="application/ld+json">{json_ld_min}</script>'
                    '<!-- /wp:html -->'
                )


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

    meta_attr = (meta_description or "").replace('"', ' ').strip()

    final_html = f"""{json_ld_script}
    <meta name="description" content="{meta_attr}">
    {img_html}
    {toc_html}
    {body_content}
    """.strip()

    #     final_html = f"""{json_ld_script}
# <meta name="description" content="{meta_description.replace('"', ' ')}">
# {img_html}
# {toc_html}
# {body_content}
# """

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
            return life_tips_keyword(kw)
            # return True  # 포스팅 1개 작성 후 종료
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
            return life_tips_keyword(kw)
            # return True  # 포스팅 1개 작성 후 종료
        else:
            print(f"⚠️ 유사 주제 건너뛰기: '{kw}' (유사도: {score}%)")

    return suggest__