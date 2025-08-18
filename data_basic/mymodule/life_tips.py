# 🔄 리디자인된 연합뉴스 자동 블로그 업로드 스크립트
# 카테고리: 생활 팁과 정보 (Blue)
# 모델: GPT-4o 전면 사용

import os
import requests
import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.compat import xmlrpc_client


import variable as v_

# ✅ OpenAI + WordPress 클라이언트 설정

dir_path = "C:\\my_games\\" + str(v_.game_folder)
file_path_one = dir_path + "\\mysettings\\idpw\\onecla.txt"
file_path_two = dir_path + "\\mysettings\\idpw\\twocla.txt"
if os.path.isfile(file_path_one) == True:
    # 파일 읽기
    with open(file_path_one, "r", encoding='utf-8-sig') as file:
        lines_one = file.read().split('\n')
        # print('lines_one', lines_one)
        thismyid_one = lines_one[0]
        v_.wd_id = thismyid_one
        thismypw_one = lines_one[1]
        v_.wd_pw = thismypw_one
        thismyps_one = lines_one[2]
        v_.domain_adress = thismyps_one
        if len(lines_one) > 3:

            if len(lines_one) > 4:
                thismykey_one = lines_one[3]
                v_.api_key = thismykey_one
                thismycategory_one = lines_one[4]
                v_.my_category = thismycategory_one
            else:

                thismykey_one = lines_one[3]
                v_.api_key = thismykey_one

        one_id = thismyid_one
        one_pw = thismypw_one
else:
    print('one 파일 없당')
    thismyid_one = 'none'
    thismyps_one = 'none'

if os.path.isfile(file_path_two) == True:
    # 파일 읽기
    with open(file_path_two, "r", encoding='utf-8-sig') as file:
        lines_two = file.read().split('\n')
        print('lines_two', lines_two)
        thismyid_two = lines_two[0]
        thismypw_two = lines_two[1]
        thismyps_two = lines_two[2]

        two_id = thismyid_two
        two_pw = thismypw_two
else:
    print('two 파일 없당')
client = OpenAI(api_key=v_.api_key, timeout=200)
wp = Client(f"{v_.domain_adress}/xmlrpc.php", v_.wd_id, v_.wd_pw)
CATEGORY = v_.my_category


#$ 요약

def summarize_for_description(client, content, title=None, keyword=None):
    # 타이틀 제거 (본문에 포함되어 있을 수 있음)
    if title and title in content:
        content = content.replace(title, "")

    # ▶ 요약 프롬프트 구성
    import textwrap

    summary_target = textwrap.shorten(content, width=1800, placeholder="...")  # 문장 잘림 최소화
    keyword_line = f"이 내용은 '{keyword}'에 관한 블로그 본문입니다." if keyword else ""

    system_msg = f"당신은 '{v_.my_topic}' 주제에 특화된 전문 블로그 기획자입니다. SEO를 고려한 요약 문장을 작성합니다."

    prompt = f"""
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

    try:
        # ▶ GPT 호출
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        result = response.choices[0].message.content.strip()

        # 너무 짧거나 비어 있으면 예비 fallback
        if not result or len(result) < 15:
            return content.strip()[:100]

        return result

    except Exception as e:
        print("❌ 요약 실패:", e)
        return content.strip()[:100]

#$ 사진 생성

def stable_diffusion(client, article, filename, description, slug):
    try:
        print("▶ Stable Diffusion 프롬프트 요약 요청", description)

        COMMON_NEGATIVE = (
            "blurry, low quality, bad anatomy, disfigured, deformed, cropped, watermark, jpeg artifacts, text"
            "bad anatomy, deformed face, mutated hands, poorly drawn face, "
            "missing lips, fused eyes, extra limbs, blurry, ugly, lowres, jpeg artifacts, watermark"
        )

        if filename == "thumb":
            summary_prompt = (
                f"다음 내용을 기반으로 블로그 썸네일 이미지를 생성할 수 있도록 "
                f"flat design, minimal, vector style 키워드 중심으로 스테이블 디퓨전 프롬프트를 만들어줘:\n{description}"
                f"sharp eyes, cinematic style, clear background, high detail face, photorealistic, 8k, perfect lightin"
            )
        elif filename == "scene":
            summary_prompt = (
                f"다음 내용을 기반으로 사실적이고 정보성 있는 본문 이미지를 생성할 수 있도록 "
                f"photo, realistic, cinematic, natural light 스타일의 스테이블 디퓨전 프롬프트를 만들어줘:\n{description}"
                f"sharp eyes, cinematic style, clear background, high detail face, photorealistic, 8k, perfect lightin"
            )
        else:
            summary_prompt = (
                f"다음 블로그 본문 내용을 바탕으로 구체적이고 묘사적인 단어로 요약해줘 (50자 이내):\n{article}"
                f"sharp eyes, cinematic style, clear background, high detail face, photorealistic, 8k, perfect lightin"
                f"그리고 시각적으로 표현 가능한 스테이블 디퓨전 프롬프트를 만들어줘."
            )

        short_prompt = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.5
        ).choices[0].message.content.strip()

        print(f"🖼 생성된 프롬프트: {short_prompt}")

        payload = {
            "prompt": f"{short_prompt}, highly detailed, cinematic lighting, ultra-realistic, 4K",
            "negative_prompt": COMMON_NEGATIVE,
            "steps": 30,
            "width": 512,
            "height": 512,
            "sampler_index": "Euler",
            "cfg_scale": 8,
            "override_settings": {
                "sd_model_checkpoint": "xxmix9realistic_v40.safetensors [18ed2b6c48]"
            }
        }

        print("▶ Stable Diffusion 이미지 요청")
        response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)
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
            'name': image.name,
            'type': 'image/jpeg',
            'caption': short_prompt,
            'description': description,
            'bits': xmlrpc_client.Binary(image.read())
        }

        return media

    except Exception as e:
        print(f"⚠️ Stable Diffusion 이미지 생성 실패: {e}")
        return None


#$ ai 남은 량 체크

def check_openai_ready():

    from openai import OpenAI

    from openai import OpenAIError  # 범용 예외 처리 클래스 사용

    try:

        client = OpenAI(api_key=v_.api_key, timeout=200)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "hello"}],
            temperature=0.7
        )
        return True
    except OpenAIError as e:
        print(f"⚠️ OpenAI 예외 발생: {e}")
        return False  # 이 라인 추가 추천

    except Exception as e:
        print(f"❗ 기타 오류 발생: {e}")

#$ 주제 선정

def life_tips_keyword(keyword):
    from openai import OpenAI
    print(f"▶ 키워드로 본문 초안 생성: {keyword}")
    client = OpenAI(api_key=v_.api_key, timeout=200)

    from datetime import datetime
    today = datetime.today().strftime("%Y년 %m월 %d일")
    this_year = datetime.today().year

    prompt = f"""
    📌 [정보 최신성 기준]
    이 콘텐츠는 **{today} 기준으로 최신 정보만 포함**되어야 합니다.

    - **{this_year}년 이전에 발표된 정책·제도·지원금은 제외**
    - **{today}년 기준으로 신청기간 지난 정책·제도·지원금은 제외**
    - **현재 시점에서 실제로 신청 가능한 정보**만 반영
    - 특히 '신청방법', '지원조건', '대상자' 등은 **오늘 날짜 기준으로 유효한 내용만 포함**

    📌 [작성 요청]
    다음 주제: **'{keyword}'**

    이 주제를 바탕으로 블로그용 본문 초안을 작성해주세요.

    작성 조건:
    - **분량**: 약 1000~1200자
    - **문체**: 친근하고 감성적인 말투이되, **정보성 중심**
    - **목적**: 이후 요약·전문화 작업을 위해 구조화된 초안 생성
    - **포맷**: HTML 태그 없이 일반 텍스트로 구성 (단락 구분은 줄바꿈)

    ⛔ 금지:
    - 이미 종료된 정책 또는 신청 불가능한 정보 포함
    - 추정 정보, 존재하지 않는 기관·사이트·전화번호 작성
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    f"당신은 '{v_.my_topic}' 주제에 특화된 전문 블로그 기획자입니다. "
                    "실제로 조사해 요약하는 방식으로, "
                    "정확하고 감성적인 콘텐츠를 작성해야 합니다. "
                    "특히 독자가 실질적으로 도움을 받을 수 있도록 유효한 최신 정보만 반영해야 합니다."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5
    )

    article = response.choices[0].message.content.strip().replace("```html", "").replace("```", "")
    life_tips_start(article, keyword)


#$ 요약

def life_tips_start(article, keyword):
    from bs4 import BeautifulSoup
    from slugify import slugify
    from openai import OpenAI
    from wordpress_xmlrpc import Client, WordPressPost
    from wordpress_xmlrpc.methods.posts import NewPost
    from wordpress_xmlrpc.methods.media import UploadFile
    from organization_info import my_organization_list, last_upload_ready, scan_internet

    print("▶ OpenAI ● WP 클라이언트 초기화")
    client = OpenAI(api_key=v_.api_key, timeout=200)
    wp = Client(f"{v_.domain_adress}/xmlrpc.php", v_.wd_id, v_.wd_pw)
    CATEGORY = v_.my_category
    slug = slugify(keyword)

    print("▶ GPT 콘텐츠 구조화")
    from datetime import datetime
    today = datetime.today().strftime("%Y년 %m월 %d일")
    this_year = datetime.today().year

    prompt = f"""
    [정보 최신성 강조]
    이 콘텐츠는 {today} 현재 시점 기준으로 최신 내용을 기반으로 작성되어야 합니다.
    - {this_year}년 이전에 발표된 정책·제도·지원금은 제외해야 해
    - 현재 시점에서 유효한 자료만 반영
    - 특히 '신청방법'이나 '조건', '대상자'는 오늘 날짜 기준으로 실제 신청 가능한 정보만 포함
    [목표]  
    '{keyword}' 주제를 바탕으로 생활정보성 블로그 콘텐츠를 제작합니다.  
    정보는 전문적이고 구체적으로 구성되며, **공식기관의 실제 설명을 기반으로 요약한 것처럼** 작성됩니다.  
    읽는 사람이 '링크를 눌러서 다시 확인하지 않아도 충분한 정보'를 얻을 수 있어야 합니다.  
    → 🔥 **정보는 블로그 내부에서 완결되도록 작성. 외부 링크는 부가설명일 뿐.**

    [초안]  
    {article}

    [작성 방식 및 구성]  
    1. 초안 내용을 먼저 요약한 뒤 → 영어로 번역 → 다시 한국어로 역번역 → 재해석하여 **중복 없이 완전히 새롭게 구성**
    2. 반드시 오늘 날짜 기준으로 최신의 것으로 구성.
       - 예를 들어 각종 정책, 지원금, 신청방법 등의 주제로 작성하는데 오늘 날짜 기준으로 최신 내용으로 이루어질 것.
       - 시간이 3개월 이상 지난 내용은 반드시 현재에도 그 내용이 유효한지 검사
    3. 내용은 다음 조건을 **모두 충족해야 합니다**:  
       - 추상적 설명 제거, 실질적 정보로 구성 (신청 대상, 조건, 절차, 금액, 예시 등)  
       - 정보 출처가 명확하되, “자세한 내용은 링크 참조” 금지 → **내용을 직접 서술로 대체**  
       - **공식기관이나 제도 문서처럼** 수치, 기간, 조건, 사례, 필요서류 등을 명확히 제시  
       - 각 `<h2>` 블록마다 **표(`<table>`) 또는 목록(`<ul>`) 반드시 1회 이상 삽입** (누락 시 실패)  
       - 문장마다 의미가 다르고 중복 표현 없이 다양하게 표현될 것  
       - **문장 구조는 사람의 블로그처럼 자연스럽고 리듬감 있게 작성** (GPT 티 제거)

    [본문 구조]  
    - `<title>` 태그: '{keyword}'를 앞에 배치하고, 클릭 유도형 문구 포함 (50자 이내)  
    - `<meta name="description">`: 120자 이내로 요약 설명 작성  
    - `<body>`: 전체 HTML 구조로 출력하며, `<h2>`로 구성된 소제목 4~6개 포함  
    - 각 `<h2>` 아래는 최소 600자 이상, 다음 필수 요소 포함:
       - 신청 대상/조건/금액/절차/주의사항
       - 관련 수치(예: 소득 3% 초과, 15만원 이상, 3년 이상 등)
       - 제도 운영기관 명시 (링크는 부가적 설명, 핵심정보는 본문에)
       - 내용에 링크 넣을 경우, 실제로 그 사이트 존재 유무 판단하고 링크 입력하기
       - 신청 방법/제한사항/사례 설명  
       - **표 1개 이상 또는 리스트 1개 이상 반드시 포함 (누락 금지)**
    - <h3> 제목은 동일한 단어 반복을 피하고, 문맥에 맞는 다양한 표현으로 작성할 것

    [소제목 구성 예시]  
    - 아래는 예시이며, 실제 콘텐츠 내용에 맞게 유연하게 적용할 것  
    - 정보형: OO이란 무엇이며 어떤 기준이 있는가?  
    - 절차형: 어떻게 신청하고 어떤 준비가 필요한가?  
    - 조건형: 어떤 사람이 대상이며 자격 조건은 무엇인가?  
    - 활용형: 어떤 상황에서 가장 유리하게 활용할 수 있는가?  
    - 주의사항형: 어떤 실수나 조건에서 불이익이 발생할 수 있는가?

    [마무리 구성]  
    - 각 소제목 끝에 핵심 요점 정리 `<ul>` 삽입하거나 테이블로 가능한 경우는 테이블로 정리하기
    - 마지막에 `<strong>한줄요약:</strong>` 문단 삽입  
        → 한 문장으로 요약하며, 절대 형식 템플릿(예: ‘~~~하세요’) 사용 금지  
        → 블로거가 실제로 정리해준 느낌 나도록 구성  
    - 한줄요약 아래에 `<em>개인 의견:</em>` 문단 삽입  
        → 감성 표현·의문형·두루뭉실한 마무리 금지  
        → 블로거가 직접 경험하고 결론 낸 듯, **직설적/냉정하게 마무리**
    - <strong>한줄요약:</strong> 문단은 본문 맨 마지막에 **1번만 삽입**, 반드시 <p><strong>한줄요약:</strong> ~ </p> 형식으로
    - <p><em>개인 의견:</em> ~ </p> 역시 한 번만 마지막에 삽입

    [예시 표현 방식]  
    - “국세청 기준에 따르면 총급여의 3%를 초과하는 의료비는 공제 대상입니다.”  
    - “주택청약저축 납입액은 연 240만원 한도로 소득공제를 받을 수 있습니다.”  
    - “이러한 항목은 영수증이나 납입 증명서 등의 증빙이 필요합니다.”  

    [금지 사항]  
    - “자세한 내용은 링크에서 확인하세요”라는 문장 사용 금지  
    - “ChatGPT가 생성한”, “AI에 의해 요약됨” 등 AI 흔적 금지  
    - 모호한 표현, 감성적 미사여구, 반복적인 형식 문장 금지  
    - `<h1>` 태그 금지 (본문에 제목 중복 절대 금지)  

    [최종 출력 형식]  
    - 전체 콘텐츠는 HTML 코드 전체 출력 (title, meta, body 포함)  
    - 문단별 `<h2>`, `<p>`, `<ul>`, `<table>` 구조 명확히 유지  
    - 반드시 `<p><strong>한줄요약:</strong> ~</p>` 형식  
    - 반드시 `<p><em>개인 의견:</em> ~</p>` 형식  

    [추가 조건]  
    {v_.my_prompt}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    f"당신은 '{v_.my_topic}' 주제에 특화된 전문 블로그 기획자입니다. "
                    "독자가 다른 사이트를 열지 않아도 될 만큼 상세하고 정확하게 설명해야 합니다. "
                    "공식 기관의 설명처럼 전문성과 신뢰도를 유지하되, "
                    "블로그 스타일로 자연스럽고 매끄럽게 작성하는 능력이 중요합니다. "
                    "특히 수치·절차·조건 등 구체적인 정보를 중심으로 전달하세요. "
                    "모든 전화번호 및 URL은 존재하는 정보만 활용하며, 자신 없으면 '대표전화 문의 필요' 또는 '공식 홈페이지 참조'로 처리하세요."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.6  # ✅ 정보성과 감성의 균형을 위한 적정 수치
    )

    result = response.choices[0].message.content.strip().replace("```html", "").replace("```", "")

    print("▶ GPT 응답 파싱")
    try:
        soup = BeautifulSoup(result, 'html.parser')
        title = soup.title.string.strip() if soup.title else "제목 없음"
        meta_tag = soup.find("meta", attrs={"name": "description"})
        meta_description = meta_tag["content"].strip() if meta_tag else ""

        # ✅ 중복 <h1> 제거
        h1_tags = soup.find_all("h1")
        for h1 in h1_tags:
            if title in h1.get_text(strip=True):
                print("🧹 중복 제목 제거:", h1.get_text())
                h1.decompose()

        # ✅ 한줄요약 및 개인 의견 파싱
        strong_html, opinion_html = "", ""

        # 우선 <p><strong> 또는 <strong> 태그 안에서 찾기
        for tag in soup.find_all(["p", "strong", "em"]):
            text = tag.get_text(strip=True)
            if "한줄요약" in text and not strong_html:
                strong_html = str(tag)
                tag.decompose()
            elif "개인 의견" in text and not opinion_html:
                opinion_html = str(tag)
                tag.decompose()

        # fallback: p태그 중 텍스트로만 되어 있는 경우까지 추출
        if not strong_html or not opinion_html:
            all_ps = soup.find_all("p")
            for p in all_ps:
                text = p.get_text(strip=True)
                if "한줄요약" in text and not strong_html:
                    strong_html = f"<p><strong>{text}</strong></p>"
                    p.decompose()
                elif "개인 의견" in text and not opinion_html:
                    opinion_html = f"<p><em>{text}</em></p>"
                    p.decompose()

        # ✅ 본문 HTML 재조립
        if soup.body:
            content_body = soup.body.decode_contents().strip()
        else:
            content_body = soup.decode_contents().strip()

        body_html = f"{content_body}\n{strong_html}\n{opinion_html}".strip()

        import re
        body_html = re.sub(r'<h1.*?>.*?</h1>', '', body_html, flags=re.DOTALL)

    #
        # print("▶ [DEBUG] 원본 body_html (최적화 전)")
        # print("=" * 50)
        # print(body_html)
        # print("=" * 50)


    except Exception as e:
        print("❌ GPT 응답 파싱 실패")
        print("⛼ GPT 응답 내용:")
        print(result)
        return

    # 이후 워드프레스 업로드/이미지 생성 로직은 기존 코드 유지


    print("▶ 썸네일 이미지 생성")
    # 너무 긴 slug 방지
    short_slug = slugify(keyword)[:50]  # 또는 40자 등 원하는 길이

    thumb_media = stable_diffusion(client, article, "thumb", f"{keyword} 썸네일", short_slug)
    if thumb_media:
        res = wp.call(UploadFile(thumb_media))
        thumbnail_id = getattr(res, "id", res["id"])
        thumb_desc = summarize_for_description(client, body_html, title=title, keyword=keyword)
    else:
        thumbnail_id = None
        thumb_desc = ""

    print("▶ 본문 이미지 생성")
    scene_media = stable_diffusion(client, article, "scene", f"{keyword} 본문 이미지", short_slug)
    if scene_media:
        res = wp.call(UploadFile(scene_media))
        scene_url = getattr(res, "link", res.get("link"))
    else:
        scene_url = ""



    print("▶ 워드프레스 게시물 업로드")
    post = WordPressPost()
    post.title = title

    one_line_summary = strong_html.replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>",
                                                                                                          "").strip()
    personal_opinion = opinion_html.replace("<p>", "").replace("</p>", "").replace("<em>", "").replace("</em>",
                                                                                                       "").strip()
    #
    # print("body_htmlbody_htmlbody_htmlbody_htmlbody_htmlbody_htmlbody_htmlbody_htmlbody_htmlbody_html")
    # print(body_html)
    # print("body_htmlbody_htmlbody_htmlbody_htmlbody_htmlbody_htmlbody_htmlbody_htmlbody_htmlbody_html")

    # ✅ GPT로 본문 구성 후
    gpt_generated_html = optimize_html_for_seo_with_gpt(
        client,
        f"<img src='{scene_url}' style='display:block; margin:auto;' alt='{keyword}'><br>{body_html}",
        keyword,
        one_line_summary=one_line_summary,
        personal_opinion=personal_opinion,
        this_title=title
    )
    #
    # print("gpt_generated_htmlgpt_generated_htmlgpt_generated_htmlgpt_generated_htmlgpt_generated_html")
    # print(gpt_generated_html)
    # print("gpt_generated_htmlgpt_generated_htmlgpt_generated_htmlgpt_generated_htmlgpt_generated_html")

    # ✅ 기관명 추출 후 검색 및 저장
    for org_name in my_organization_list(gpt_generated_html):
        scan_internet(org_name)

    # ✅ 기관 정보 기반 교체 및 최종 업로드 준비
    optimized_html = last_upload_ready(gpt_generated_html)

    # ✅ 3. GPT 기반 키워드 자동 추출
    auto_tags = extract_tags_from_html_with_gpt(client, optimized_html, keyword)

    #########$$$$$$$$$$$$$$$$$$$$$$$$$$$

    post.content = optimized_html

    post.excerpt = thumb_desc
    post.terms_names = {
        'category': [safe_term_cate(CATEGORY)],
        'post_tag': list(set([safe_term_word(keyword)] + [safe_term_word(t) for t in auto_tags]))
    }
    post.custom_fields = [
        {'key': 'rank_math_description', 'value': thumb_desc},
        {'key': 'rank_math_focus_keyword', 'value': keyword},  # 메인 키워드
        {'key': 'rank_math_secondary_keywords', 'value': ", ".join(auto_tags)}  # 보조 키워드
    ]
    if thumbnail_id:
        post.thumbnail = thumbnail_id
    post.post_status = 'publish'

    if not title or not optimized_html or "제목 없음" in title or len(optimized_html.strip()) < 200:
        print("❌ 콘텐츠가 비정상입니다. 업로드를 중단합니다.")
    else:
        wp.call(NewPost(post))
        print(f"✅ 게시 완료: {title}")

#$ 태그 추출

def extract_tags_from_html_with_gpt(client, html_content, keyword):
    prompt = f"""
    다음은 블로그 콘텐츠 HTML입니다. 본문에 실제 등장한 주요 용어 중에서, 블로그 태그로 적합한 핵심 키워드 5~7개를 **중복 없이** 뽑아주세요.

    📌 조건:
    - 본문에 실제 존재하는 단어만 사용합니다.
    - 각 키워드는 1~3단어로 짧고 명확해야 합니다.
    - 형식 설명 없이 아래 예시처럼 **JSON 배열만** 반환하세요.

    예시 출력:
    ["전기차", "요금 할인", "환경부", "신청 방법", "지원 대상"]

    🔽 HTML 콘텐츠:
    {html_content}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        import json
        import re
        # GPT 응답에서 JSON 배열만 추출
        content = response.choices[0].message.content.strip()
        json_match = re.search(r'\[\s*"[^"]+"\s*(,\s*"[^"]+"\s*)*\]', content)

        if json_match:
            return json.loads(json_match.group())
        else:
            print("no json_match", content)

        print(f"⚠️ JSON 형식 불일치:\n{content}")
        return []

    except Exception as e:
        print(f"❌ 태그 추출 실패: {e}")
        return []


def safe_term_cate(term):
    import re
    # 너무 길면 짜르고, 빈 값 방지, (태그에 특수문자 제거 포함
    if not term or not isinstance(term, str):
        return "일반"
    term = term.strip()[:40]
    return term

def safe_term_word(term):
    import re
    # 너무 길면 짜르고, 빈 값 방지, (태그에 특수문자 제거 포함
    if not term or not isinstance(term, str):
        return "일반"
    term = term.strip()[:40]
    # 특수문자 제거, 공백 → 하이픈 변환
    term = re.sub(r"[^\w가-힣\s-]", "", term)
    term = re.sub(r"\s+", "-", term)
    return term

def optimize_html_for_seo(html_content, keyword):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, 'html.parser')

    summary_tag = soup.find("strong")
    summary_html = None
    if summary_tag and summary_tag.parent.name == "p":
        summary_html = str(summary_tag.parent)
        summary_tag.parent.decompose()

    opinion_tag = soup.find("em")
    opinion_html = None
    if opinion_tag and opinion_tag.parent.name == "p":
        opinion_html = str(opinion_tag.parent)
        opinion_tag.parent.decompose()

    for h2 in soup.find_all("h2"):
        section = soup.new_tag("section")
        h2.insert_before(section)
        section.append(h2.extract())
        next_tag = section.find_next_sibling()
        while next_tag and next_tag.name not in ["h2", "section"]:
            section.append(next_tag.extract())
            next_tag = section.find_next_sibling()

    replacements = ["첫째", "둘째", "셋째", "넷째", "다섯째"]
    for section in soup.find_all("section"):
        ol = soup.new_tag("ol")
        for rep in replacements:
            for tag in section.find_all("p"):
                if tag.text.strip().startswith(rep):
                    li = soup.new_tag("li")
                    li.string = tag.text.strip().replace(f"{rep},", "").strip()
                    tag.replace_with(li)
                    ol.append(li)
        if ol.contents:
            section.insert(1, ol)

    for img in soup.find_all("img"):
        if not img.has_attr("alt") or img["alt"].strip() == "":
            img["alt"] = keyword

    if summary_html:
        soup.append(BeautifulSoup(summary_html, 'html.parser'))
    if opinion_html:
        soup.append(BeautifulSoup(opinion_html, 'html.parser'))

    return str(soup)

#$ 내용 상세하게

def optimize_html_for_seo_with_gpt(client, html_content, keyword, one_line_summary="", personal_opinion="", this_title=""):
    from bs4 import BeautifulSoup
    from datetime import datetime

    print("▶ GPT로 소제목 단위 재구성 시작")
    soup = BeautifulSoup(html_content, 'html.parser')

    # ✅ 이미지 alt 속성 삽입

    main_image = soup.find("img")
    if main_image:
        plain_keyword = BeautifulSoup(keyword, "html.parser").get_text().strip()
        main_image["alt"] = plain_keyword
        img_html = str(main_image).replace("\n", "").strip()
        main_image.decompose()
    else:
        img_html = ""
        print("⚠️ 이미지가 없습니다.")

    # ✅ 날짜 설정
    today = datetime.today().strftime("%Y년 %m월 %d일")
    this_year = datetime.today().year

    # ✅ 목차 보존 및 섹션 추출 함수 정의
    def extract_sections_preserving_toc(soup):
        body_container = soup.body if soup.body else soup
        sections = []
        current_section = []
        toc_section = []

        for elem in body_container.children:
            if getattr(elem, 'name', None) == "h2":
                h2_text = elem.get_text(strip=True)
                if h2_text == "목차" and not toc_section:
                    toc_section.append(elem)
                    next_elem = elem.find_next_sibling()
                    while next_elem and getattr(next_elem, 'name', None) == "ul":
                        toc_section.append(next_elem)
                        next_elem = next_elem.find_next_sibling()
                else:
                    if current_section:
                        sections.append(current_section)
                    current_section = [elem]
            elif current_section:
                current_section.append(elem)

        if current_section:
            sections.append(current_section)

        toc_section_html = "\n".join([str(tag) for tag in toc_section]) if toc_section else ""
        return toc_section_html, sections

    # ✅ 목차 및 섹션 추출
    toc_section_html, sections = extract_sections_preserving_toc(soup)

    # ✅ 스타일 태그 삽입
    style_tag = """
    <style>
    h2 { margin-top: 40px; color: #0077cc; font-weight: bold; }
    h3 { margin-top: 25px; color: #333; font-weight: bold; }
    ul, table { margin: 10px 0; padding: 0 10px; }
    em { color: #444; font-style: normal; }
    </style>
    """.strip()

    # ✅ GPT로 소제목별 본문 생성 (중복 방지 + 문맥 기반 생성 방식)
    new_body = []

    # 전체 소제목 리스트 먼저 수집
    h2_list = [h2.get_text(strip=True) for h2, *_ in sections]

    print("🔍 섹션 개수:", len(sections))

    for i, section in enumerate(sections):

        print(f"[{i}] 소제목: {section[0].get_text(strip=True)}")
        h2 = section[0]
        h2_text = h2.get_text(strip=True)

        system_message = (
            f"당신은 '{v_.my_topic}' 주제에 특화된 전문 블로그 기획자입니다. "
            "절대 허위 정보를 생성하지 않으며, 전화번호, 정책명, 웹사이트 주소는 반드시 실존하는 공식 정보만 사용합니다. "
            "내용은 자연스럽고 신뢰감 있게 구성하며, AI 스타일의 흔적 없이 공공기관 공식 자료를 바탕으로 작성합니다. "
            "팩트 체크에 철저하며, 최신 제도 기준으로만 작성합니다."
        )

        # 소제목 따로 분리해서 전체내용을 알수 있도록
        other_titles = [t for j, t in enumerate(h2_list) if j != i][:9]
        other_titles_text = "\n".join([f"- {t}" for t in other_titles])

        prompt = f"""
        📌 [작성 목적]
        당신은 전문 블로그 콘텐츠 기획자로서, '{keyword}' 주제의 블로그 글 중 다음 소제목에 해당하는 **세부 본문**을 작성해야 합니다:
        → <strong>{h2_text}</strong>

        📌 [중복 방지 조건]
        다음 소제목들과 **내용이 겹치지 않도록 완전히 다른 정보로 작성**하세요:
        {other_titles_text}

        📌 [팩트 체크 및 정확성 유지]
        - 작성 전 반드시 실제로 시행 중인 정책, 제도, 기관 기준으로 **사실 확인**을 완료해야 합니다.
        - **웹검색 기반으로 실제 공공기관, 정부 사이트, 공식 보도자료를 바탕으로만 정보 작성**하세요.
        - 다음 항목에 대해 **허위/추측 없이 실제 존재하는 정보만 포함**하세요:
          1. 제도명, 기관명, 부서명, 전화번호, 웹사이트 주소
          2. 정책 시행일, 종료일, 신청 가능 시기
          3. 소득/연령 기준, 면적/가격 요건
          4. 신청 절차, 준비 서류, 유의사항
          5. 시행 기관의 실제 신청 페이지나 안내 링크

        📌 [출력 형식 - HTML]
        - 전체 출력은 반드시 순수 HTML 형식으로 작성하세요. **마크다운(예: ```html) 금지**
        - `<h2>` 태그는 사용하지 마세요.
        - **<h3> 소제목을 2~3개** 포함하고, 각 문단은 **서로 다른 의미를 담도록 분리**하세요.
        - 본문 중간에 최소 1개 이상의 **<ul> 또는 <table>** 포함 필수.
        - 핵심 키워드는 **자연스럽게 <strong>으로 강조**하세요.
        - **<a href="...">링크는 중복 없이 1회만 삽입**, 공공기관의 실제 주소만 사용하세요.

        📌 [정보 구성 필수 조건]
        다음 중 **최소 3가지 이상**을 포함하여 구성하세요:
        - 법률/공식문서에서 확인 가능한 제도·정책 이름
        - 시행 기관명 또는 담당 부서 명시
        - 연령/소득/면적 조건 등 상세 요건
        - 신청 절차 및 방법(어디서, 어떻게, 언제 신청 가능한지)
        - 표나 목록 형식으로 정리된 항목
        - 실제 통계자료나 사례, 공공기관 보도자료 기반 근거

        📌 [참조 링크]
        - 본문 마지막에 다음 형식으로 **1회만 삽입**하세요:
          <p>참조: <a href="https://기관도메인" target="_blank" rel="noopener">기관명</a></p>

        📌 [최신 정보 기준]
        - 오늘 날짜 기준({today}), **{this_year}년 이후에 시행 중인 제도 또는 공식 공표된 정책만** 포함하세요.
        - **과거 종료된 제도, 입법예고, 제안 중인 제도는 절대 포함하지 마세요.**

        📌 [문체 및 SEO 스타일 가이드]
        - 문장은 **공식 블로그처럼 신뢰감 있고 자연스럽게** 작성하세요.
        - **GPT 또는 AI 스타일의 반복 어투, 과장된 마무리 표현 등은 절대 금지**입니다.
        - 문장마다 **핵심 키워드를 SEO를 고려하여 자연스럽게 포함**하세요.
        - 단락 간 **논리적 연결과 문단 흐름**을 신경 써서 매끄럽게 구성하세요.

        ❗ 절대 금지 사항
        - 허구의 전화번호, URL, 기관명
        - AI 스타일 마무리 문구 (“도움이 되었길 바랍니다” 등)
        - `<h2>` 사용, 마크다운 코드블럭( ``` ) 사용
        
        ❗❗ 다시 강조: 출력은 순수 HTML 콘텐츠만 작성하며, 마크다운 코드블록( ```)은 절대 사용하지 마세요.

        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            rewritten_html = response.choices[0].message.content.strip()
            rewritten_html = strip_markdown_code_block(rewritten_html)
        except Exception as e:
            print(f"❌ GPT 재구성 실패 - {h2_text}: {e}")
            rewritten_html = f"<p>{h2_text} 관련 내용을 준비하지 못했습니다.</p>"

        new_body.append("\n" + str(h2))
        new_body.append("\n" + rewritten_html)

        # ✅ 목차 추가

    system_message = (
        f"당신은 '{v_.my_topic}' 주제에 특화된 전문 블로그 기획자입니다. "
        "절대 허위 정보를 생성하지 않으며, 전화번호나 웹사이트 주소는 존재하는 공식 정보만 사용합니다. "
        "AI 흔적을 남기지 마세요."
    )

    prompt = f"""
📌 [콘텐츠 작성 목적]
- 여기 콘텐츠에 담겨진 내용을 분석해서 '<목차>' 라는 소제목을 제일 먼저 작성하고 소제목 아래 내용에는 <ul> 리스트로 소제목을 작성하고 그 리스트가 밑에 생성된 소제목에 링크 되도록. 

📌 [콘텐츠]
- {new_body}

📌 [콘텐츠 배치 순서]
- 생성된 '<목차>' 라는 소제목을 가장 위에 배치하고 그 아래에 리스트, {new_body} 순으로 배치
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        rewritten_html = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ GPT 재구성 실패 - {h2_text}: {e}")
        rewritten_html = f"<p>{h2_text} 관련 내용을 준비하지 못했습니다.</p>"

    body_html = f"{rewritten_html}"  # GPT가 만든 전체 HTML

    # ✅ 요약 및 의견 추가
    extra_parts = []
    if one_line_summary:
        cleaned_summary = one_line_summary.replace("한줄요약:", "").strip()
        extra_parts.append(f"<p></p><br><p><strong>한줄요약:</strong> {cleaned_summary}</p>")
    if personal_opinion:
        cleaned_opinion = personal_opinion.replace("개인 의견:", "").strip()
        extra_parts.append(
            f"<p><em style='color:#555; font-weight:bold; font-style: italic; '>{cleaned_opinion}</em></p>")

    # ✅ 메타 설명

    meta_description = summarize_for_description(client, body_html, title=this_title, keyword=keyword)
    # meta_description = f"{keyword}에 대한 실생활 정보 및 가이드입니다."
    meta_description_paragraph = f'<p style="color:#888;"><strong>📌 </strong> {meta_description}</p>'

    # ✅ JSON-LD FAQ 생성 (GPT 활용)
    # ✅ JSON-LD FAQ 생성
    json_ld_block = generate_json_ld_faq_with_gpt(client, body_html, keyword)

    # ✅ 본문 최종 구성
    full_body = "\n".join([style_tag, body_html] + ([json_ld_block] if json_ld_block else []) + extra_parts)
    # full_body = "\n".join([style_tag, toc_section_html] + new_body + extra_parts + [tag_html])

    # ✅ 메타 태그 삽입용 <meta> (SEO 목적)
    meta_content = cleaned_summary if cleaned_summary else f"{keyword}에 대한 정보 요약입니다."
    meta_tag = f'<meta name="description" content="{meta_content}">'

    # ✅ 최종 HTML 조립
    final_html = f"""<!-- wp:html -->
    {meta_tag}
    {img_html}
    {meta_description_paragraph}
    {full_body}
    <!-- /wp:html -->""".strip()

    # ✅ <a> 태그 중첩 제거 처리
    final_html = postprocess_html_for_blog(final_html, keyword)

    return final_html





#############후처리

def strip_markdown_code_block(text: str) -> str:
    # ```html 또는 ``` 제거
    import re
    return re.sub(r"```html\s*|```", "", text).strip()

def generate_json_ld_faq_with_gpt(client, full_html, keyword):
    """
    전체 HTML 콘텐츠를 바탕으로 GPT에게 JSON-LD FAQ 구조를 생성 요청
    :param client: OpenAI 클라이언트
    :param full_html: 최종 콘텐츠 HTML (style 포함)
    :param keyword: 핵심 키워드 (title 및 질문 내용 참조)
    :return: JSON-LD <script> 블록 문자열
    """
    system_message = (
        "당신은 Google SEO 전문가이자 JSON-LD 마크업 구조화에 특화된 개발자입니다. "
        "사용자의 블로그 HTML 콘텐츠를 바탕으로 FAQPage 스키마를 생성합니다. "
        "질문은 <h2> 또는 중요한 문단 제목을 기반으로 하고, 답변은 해당 섹션 요약입니다. "
        "출력은 JSON-LD 형식이며 <script type=\"application/ld+json\">...</script> 태그 전체만 출력하세요. "
        "마크다운이나 다른 텍스트는 절대 포함하지 마세요. HTML 태그는 JSON 내부에 포함하지 마세요."
        "FAQPage 스키마를 JSON-LD 형식으로 정확하게 출력하세요. "
        "출력에는 절대 ```json 같은 마크다운 블럭을 사용하지 마세요. "
        "오직 <script type=\"application/ld+json\">...</script> 로 감싼 JSON만 출력하세요."
    )

    prompt = f"""
📌 [콘텐츠 키워드]
- {keyword}

📌 [HTML 본문]
{full_html}

📌 [FAQ 생성 조건]
- 총 3~5개 질문-답변으로 구성하세요.
- 질문은 사용자가 실제 검색할 법한 문장으로 바꾸고, 답변은 친절하고 요약된 설명으로 작성하세요.
- HTML은 제거한 순수 텍스트 기반 질문·답변으로 구성합니다.
- 출력 형식은 반드시 JSON-LD (FAQPage 스키마) 입니다.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1200
        )
        json_ld_raw = response.choices[0].message.content
        json_ld = clean_json_ld_output(json_ld_raw)
        # json_ld = response.choices[0].message.content.strip()
        if json_ld.startswith("<script"):
            print("✅ 생성된 JSON-LD FAQ:\n", json_ld)  # 👈 이 위치에서 확인
            return json_ld if json_ld.startswith("<script") else ""
        else:
            print("⚠️ JSON-LD 응답 형식 아님:\n", json_ld)
            return ""
    except Exception as e:
        print(f"❌ JSON-LD GPT 생성 실패: {e}")
        return ""

def clean_json_ld_output(gpt_response: str) -> str:
    import re
    # 1. ```json 코드 블럭 제거
    cleaned = re.sub(r"^```json", "", gpt_response.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"```$", "", cleaned.strip())

    # 2. 불필요한 개행/띄어쓰기 정리
    cleaned = re.sub(r"\s+\n", "\n", cleaned)
    cleaned = re.sub(r"\n\s+", "\n", cleaned)

    # 3. 줄바꿈된 단어 붙이기 (예: 수 있\n습니다 → 수 있습니다)
    cleaned = re.sub(r"(\S)\s*\n\s*(\S)", r"\1 \2", cleaned)

    return cleaned.strip()

def postprocess_html_for_blog(html: str, keyword: str) -> str:
    html = remove_nested_a_tags(html)
    html = remove_whitespace_before_images(html)
    html = clean_ul_paragraphs(html)
    html = convert_markdown_bold_to_html(html)
    return html


def remove_nested_a_tags(html: str) -> str:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    for a_tag in soup.find_all("a"):
        nested_links = a_tag.find_all("a")
        for nested in nested_links:
            nested.unwrap()
    return str(soup)
def remove_whitespace_before_images(html: str) -> str:
    import re
    return re.sub(r'(\s*<br\s*/?>\s*)*(<img[^>]+>)', r'\2', html)
def clean_ul_paragraphs(html: str) -> str:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    for ul in soup.find_all("ul"):
        for p in ul.find_all("p"):
            p.unwrap()
    return str(soup)
def boldify_keyword_once(html: str, keyword: str) -> str:
    import re
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")

    # 텍스트가 있는 태그에서만 대체 (img, script 등은 무시)
    count = 0
    for tag in soup.find_all(text=True):
        if count >= 1:
            break
        if keyword in tag and tag.parent.name not in ["script", "style", "img"]:
            tag.replace_with(tag.replace(keyword, f"<strong>{keyword}</strong>", 1))
            count += 1

    return str(soup)



def convert_markdown_bold_to_html(html_text: str) -> str:
    import re
    # **text** → <strong>text</strong>
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html_text)


#########################

def is_similar_topic(new_topic, existing_titles, client):
    """
    GPT-4o를 이용해 기존 제목과의 유사성 비교
    """
    compare_prompt = f"""
    아래는 이미 블로그에 작성된 제목들이야:
    {existing_titles}

    그리고 지금 추천된 새로운 주제는 '{new_topic}'이야.
    이 새로운 주제가 기존 제목들과 얼마나 유사한지 0~100 사이의 점수로 평가해줘.
    0은 완전히 다른 주제이고, 100은 거의 같은 주제야.

    숫자만 출력해줘.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": compare_prompt}],
        temperature=0.4
    )
    result = response.choices[0].message.content.strip()
    try:
        return int(result)
    except ValueError:
        print(f"⚠️ 예상하지 못한 응답: {result}")
        return 0

# ✅ 함수: 글 전체 제목 가져오기
# def load_existing_titles():
#     import requests
#
#     titles = []
#     page = 1
#
#     while True:
#         url = f"{v_.domain_adress}/wp-json/wp/v2/posts?per_page=100&page={page}"
#         resp = requests.get(url)
#         if resp.status_code != 200:
#             break
#
#         data = resp.json()
#         if not data:
#             break
#
#         titles += [post['title']['rendered'] for post in data]
#         page += 1
#
#     print(f"총 {len(titles)}개의 게시글 제목을 가져왔습니다.")
#     return titles

# ✅ 수정된 함수: 최신 글 20개 제목만 가져오기
# def load_existing_titles():
#     import requests
#
#     url = f"{v_.domain_adress}/wp-json/wp/v2/posts?per_page=20&page=1"
#     resp = requests.get(url)
#
#     if resp.status_code != 200:
#         print("❌ 제목 가져오기 실패:", resp.status_code)
#         return []
#
#     data = resp.json()
#     titles = [post['title']['rendered'] for post in data]
#
#     print(f"📌 최신 글 {len(titles)}개의 제목을 가져왔습니다.")
#     return titles


# ✅ 최신 글 20개 제목 가져오기 함수

def load_existing_titles():
    import requests

    url = f"{v_.domain_adress}/wp-json/wp/v2/posts?per_page=20&page=1&orderby=date&order=desc"
    resp = requests.get(url)

    if resp.status_code != 200:
        print("❌ 제목 가져오기 실패:", resp.status_code)
        return []

    data = resp.json()
    titles = [post['title']['rendered'] for post in data]

    print(f"📌 최신 글 {len(titles)}개의 제목을 가져왔습니다. gpt")
    return titles

#$ 제목 정하기

def suggest_life_tip_topic():
    from openai import OpenAI
    import json

    import variable as v_

    from datetime import datetime
    today = datetime.today().strftime("%Y년 %m월 %d일")
    month = datetime.today().month
    if month in [3, 4, 5]:
        current_season = "봄"
    elif month in [6, 7, 8]:
        current_season = "여름"
    elif month in [9, 10, 11]:
        current_season = "가을"
    else:
        current_season = "겨울"
    this_year = datetime.today().year

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
        print("▶ 새로운 주제 추천 요청")
        client = OpenAI(api_key=v_.api_key, timeout=200)

        result_titles = load_existing_titles()

        # 2. system 역할에 블로그 방향성 명시
        system_prompt = f"""
        당신은 '{v_.my_topic}' 주제에 특화된 전문 블로그 기획자입니다.
        이 블로그는 사람들이 검색을 통해 찾는 실용적이고 시기적절한 정보를 제공합니다.

        당신의 임무는 **현재 계절({current_season})과 날짜({today})를 고려한 구체적인 정보성 주제**를 제안하는 것입니다.
        검색엔진 최적화(SEO)를 고려해 **사람들이 실제로 검색할 가능성이 높은 표현**으로 주제를 구성해야 합니다.

        {v_.my_topic_system}
        """

        # 3. user 프롬프트
        user_prompt = f"""
        📂 [블로그 카테고리]
        - {v_.my_category}

        📚 [이미 다룬 블로그 제목 목록]
        {result_titles}

        📅 [오늘 날짜]
        - {today}, 현재 계절: {current_season}

        🧭 [주제 선정 조건]
        - 최대한 위 목록 {result_titles} 들과 **겹치지 않는 새로운 주제** 10개만 리스트로 추천
        - [] 배열에 담아서 반복문으로 출력 가능하도록.
        - 검색 수요가 높고, 사람들이 궁금해할만한 실용 정보 위주로 제시
        - 제목 내용이 의미상 50% 이상 유사한 경우도 중복으로 간주하여 배제
        {v_.my_topic_user}

        ✅ [SEO 및 콘텐츠 기준]
        1. 제목은 **핵심 키워드가 앞에 위치**하도록 작성
        2. 너무 광범위하거나 흔한 주제(X) → 구체적 검색 문구로 제시
           - (예: '여름철 건강관리' ❌ → '폭염 속 전기요금 할인제도 신청방법' ✅)
        3. 계절감은 **내용에 반영**하되, 제목에 반복적으로 계절명 표기하지 않음
        4. 정책·지원금 관련 정보는 **{today} 기준 최근 60일 이내 발표된 내용만 포함**
            - 단, **{today}년 기준으로 신청기간 지난 정책·제도·지원금은 제외*
        5. 출력은 **한 줄 주제 제목**만. **이모지·특수문자 없이** 명확하게 작성
        6. 출력은 반드시 다음 형식처럼 JSON 배열로 해줘:
        ["주제1", "주제2", "주제3", "주제4", "주제5"]

        📌 [출력 예시]
        ["태풍 피해 복구 지원금 신청 방법", "전기요금 복지할인 조건 총정리", "청년전세보증금 반환보증 신청 절차"]

        """

        # 4. GPT 호출
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5
        )

        try:

            raw_gpt_response = response.choices[0].message.content.strip()
            result_suggest = parse_topic_list(raw_gpt_response)
            assert isinstance(result_suggest, list)

            # 기존 제목 가져오기
            existing_titles = load_existing_titles()

            print("🆕 추천 키워드들:", result_suggest)

            for kw in result_suggest:
                print("🆕 추천 키워드:", kw)



                # 중복 주제 여부 판단
                score = is_similar_topic(kw, existing_titles, client)

                if score >= 70:
                    print(f"⚠️ 유사 주제 가능성 높음 (유사도: {score}%)")



                else:
                    print(f"✅ OpenAI 상태 정상. 콘텐츠 작성 시작. (유사도: {score}%)")
                    life_tips_keyword(kw)

                    print("keyword")

                    suggest__ = True

                    break
        except Exception as e:
            print("❌ JSON 파싱 실패:", e)
            print("GPT 응답 내용:", response.choices[0].message.content)
            return


    return suggest__



def parse_topic_list(raw_text):
    import json
    import re

    # 마크다운 코드블록 제거: ```json ... ``` or ```plaintext ... ``` 등 제거
    cleaned = re.sub(r"^```(?:json|plaintext)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)

    try:
        return json.loads(cleaned)
    except Exception as e:
        print("❌ JSON 파싱 실패:", e)
        return None

def suggest_life_tip_topic_issue(keyword):
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
        print("▶ suggest_life_tip_topic_issue", keyword)
        client = OpenAI(api_key=v_.api_key, timeout=200)

        # 기존 제목 가져오기
        existing_titles = load_existing_titles()

        # 중복 주제 여부 판단
        score = is_similar_topic(keyword, existing_titles, client)

        if score >= 80:
            print(f"⚠️ 유사 주제 가능성 높음 (유사도: {score}%)")



        else:
            print("✅ OpenAI 상태 정상. 콘텐츠 작성 시작.")
            life_tips_keyword(keyword)

            print("suggest_life_tip_topic_issue end")

            suggest__ = True

    return suggest__


