
def news_economy_start():
    import re
    import time
    import feedparser
    import requests
    import json
    from io import BytesIO
    from PIL import Image
    from bs4 import BeautifulSoup

    from openai import OpenAI
    from env_ai import wp_id, wp_ps, keys

    from wordpress_xmlrpc import Client, WordPressPost
    from wordpress_xmlrpc.methods.posts import NewPost
    from wordpress_xmlrpc.methods.media import UploadFile
    from wordpress_xmlrpc.compat import xmlrpc_client

    # ――― 0) 설정 ―――
    print("▶ 초기화: OpenAI·WP 클라이언트")
    client = OpenAI(api_key=keys())
    wp = Client("https://hobbycolorful.com/xmlrpc.php", wp_id(), wp_ps())

    RSS_URL = "http://www.yonhapnewstv.co.kr/category/news/economy/feed/"
    CATEGORY = "HobbyWhite(뉴스)"

    # ――― 1) RSS 파싱 & 본문 크롤링 ―――
    print("▶ 1) RSS 파싱 중…")
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        raise RuntimeError("RSS가 비어 있습니다.")
    entry = feed.entries[0]
    print("✅ RSS 수신:", entry.title)

    def fetch_full_text(url):
        try:
            html = requests.get(url, timeout=10).text
            soup = BeautifulSoup(html, "html.parser")
            node = soup.select_one("#articleBodyContents")
            text = node.get_text(" ", strip=True) if node else entry.summary
            print("▶ 본문 크롤링 성공")
            return text
        except Exception as e:
            print("❌ 본문 크롤링 실패:", e)
            return entry.summary

    full_text = fetch_full_text(entry.link)

    # ――― 1.5) 제목 전문가 스타일 재작성 ―――
    def refine_title(raw_title):
        prompt = (
            f"다음 뉴스 기사의 제목을 전문 리포트 헤드라인 스타일로 자연스럽게 다듬어 주세요:\n\n"
            f"원제목: \"{raw_title}\""
        )
        try:
            print("▶ 제목 재작성 요청")
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=30
            )
            refined = resp.choices[0].message.content.strip()
            print("✅ 재작성된 제목:", refined)
            return refined
        except Exception as e:
            print("❌ 제목 재작성 실패:", e)
            return raw_title

    refined_title = refine_title(entry.title)

    # ――― 2) OpenAI 구조화 요청 ―――
    def get_structured_data():
        safe_title = json.dumps(refined_title)
        safe_text = json.dumps(full_text)
        prompt = (
            f"기사 제목: {safe_title}\n본문:\n{safe_text}\n\n"
            "아래 JSON 형식으로 응답하세요:\n"
            "- slug_keywords: 핵심 3~5개 키워드 배열\n"
            "- sections: subtitle(한 문장 요약), paragraph(200~300자), image_prompt\n"
            "- one_liner: 전체를 한 문장으로 요약\n"
            "- opinion: 분석가 의견\n"
            "```json\n"
            "{\n"
            f'  "title": {safe_title},\n'
            '  "slug_keywords": ["키워드1","키워드2","키워드3"],\n'
            '  "sections":[\n'
            '    {"subtitle":"섹션1","paragraph":"…","image_prompt":"…"},\n'
            '    {"subtitle":"섹션2","paragraph":"…","image_prompt":"…"}\n'
            '  ],\n'
            '  "one_liner":"…",\n'
            '  "opinion":"…"\n'
            "}\n```"
        )
        for i in range(2):
            try:
                print(f"▶ 2) 구조화 요청 시도 {i + 1}")
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=800
                )
                raw = resp.choices[0].message.content or ""
                print("▶ 응답(raw):", raw[:100].replace("\n", " "), "…")
                if raw.startswith("```"):
                    raw = "\n".join(raw.splitlines()[1:-1])
                data = json.loads(raw)
                print("✅ 구조화 완료")
                return data
            except Exception as e:
                print(f"❌ JSON 파싱 실패 ({i + 1}):", e)
                time.sleep(1)
        print("▶ Fallback 적용")
        return {
            "title": refined_title,
            "slug_keywords": [],
            "sections": [{"subtitle": refined_title, "paragraph": full_text[:200], "image_prompt": None}],
            "one_liner": full_text[:100] + "…",
            "opinion": ""
        }

    data = get_structured_data()

    # ――― 2.5) 목록용 요약 생성 ―――
    def generate_excerpt(text):
        prompt = (
            f"다음 뉴스 내용을 자극적이고 임팩트 있게 100자 내외로 요약하세요:\n\n{text}"
        )
        try:
            print("▶ 목록용 요약 생성 요청")
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=120
            )
            excerpt = resp.choices[0].message.content.strip().replace("\n", " ")
            print("✅ 요약 완료:", excerpt)
            return excerpt[:200]
        except Exception as e:
            print("❌ 요약 생성 실패:", e)
            return full_text[:100].strip() + "…"

    excerpt = generate_excerpt(full_text)

    # ――― 3) 슬러그 생성 ―――
    raw_slug = "-".join(data.get("slug_keywords", [])[:4])
    slug = re.sub(r'[^a-z0-9\-]', '', raw_slug.lower()) or f"post-{int(time.time())}"
    print("▶ 3) 생성된 슬러그:", slug)

    # ――― 4) 이미지 생성·업로드 ―――
    keywords = data.get("slug_keywords", [])
    subtitles = [sec["subtitle"] for sec in data["sections"]]
    combined_prompt = " ".join(subtitles + keywords)

    def gen_and_upload(prompt, tag):
        if not prompt:
            print(f"⚠️ 이미지 프롬프트 없음 ({tag})")
            return None, None
        full_prompt = prompt + " infographic"
        print(f"▶ 이미지 생성 ({tag}):", full_prompt)
        try:
            url = client.images.generate(prompt=full_prompt, n=1, size="512x512").data[0].url
            img_data = requests.get(url, timeout=30).content
            img = Image.open(BytesIO(img_data)).convert("RGB").resize((512, 512), Image.LANCZOS)
            buf = BytesIO();
            img.save(buf, format="JPEG", quality=60, optimize=True)
            print(f"   ▶ 최적화 완료 ({tag})")
        except Exception as e:
            print(f"❌ 생성/최적화 실패 ({tag}):", e)
            return None, None

        media = {
            "name": f"{slug}-{tag}.jpg",
            "type": "image/jpeg",
            "caption": data["one_liner"],
            "description": data["opinion"],
            "bits": xmlrpc_client.Binary(buf.getvalue())
        }
        try:
            print(f"▶ UploadFile 호출 ({tag})")
            resp = wp.call(UploadFile(media))
            mid = resp["id"] if isinstance(resp, dict) else resp.id
            link = resp.get("link") if isinstance(resp, dict) else resp.link
            print(f"   ▶ 업로드 완료 ({tag}) id={mid}")
            return mid, link
        except Exception as e:
            print(f"❌ 업로드 실패 ({tag}):", e)
            return None, None

    # 4.1) 썸네일 (목록용)
    thumb_prompt = f"{combined_prompt} summary: {data['one_liner']}"
    print("▶ 4.1) 썸네일 프롬프트:", thumb_prompt)
    thumb_id, thumb_url = gen_and_upload(thumb_prompt, "thumb")

    # 4.2) 본문 이미지
    print("▶ 4.2) 본문 이미지 프롬프트:", combined_prompt)
    sec_id, sec_url = gen_and_upload(combined_prompt, "sec1")

    # ――― 5) 포스팅 조립 & 업로드 ―――
    html = []

    # 본문 이미지
    if sec_url:
        html.append(
            '<figure style="text-align:center;">'
            f'<img src="{sec_url}" width="512" alt="{subtitles[0]}"/>'
            '</figure>'
        )

    # 소제목→내용
    for sec in data["sections"]:
        html.append(f"<h2>{sec['subtitle']}</h2>")
        html.append(f"<p>{sec['paragraph']}</p>")

    # 한 줄 요약 & 의견
    html.append(
        f'<p style="font-size:1.2em;"><strong>한 줄 요약:</strong> {data["one_liner"]}</p>'
    )
    html.append(
        f'<h4 style="font-size:1.2em;font-style:italic;color:#555;">'
        f'{data["opinion"]}'
        '</h4>'
    )

    post = WordPressPost()
    post.title = refined_title
    post.slug = slug
    post.excerpt = excerpt
    post.content = "\n".join(html)
    post.post_status = "publish"
    post.terms_names = {
        "category": [CATEGORY],
        "post_tag": keywords
    }
    if thumb_id:
        post.thumbnail = thumb_id

    print("▶ 5) WP 포스팅 시도…")
    wp.call(NewPost(post))
    print("✅ 완료! 슬러그:", slug)
