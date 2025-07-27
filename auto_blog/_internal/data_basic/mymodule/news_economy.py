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

def news_economy_start():
    print("▶ 초기화: OpenAI·WP 클라이언트")
    client = OpenAI(api_key=keys())
    wp = Client("https://hobbycolorful.com/xmlrpc.php", wp_id(), wp_ps())

    RSS_URL = "http://www.yonhapnewstv.co.kr/category/news/economy/feed/"
    CATEGORY = "뉴스 및 이슈 (White)"

    print("▶ 1) RSS 파싱 중…")
    feed = feedparser.parse(RSS_URL)
    entry = feed.entries[0] if feed.entries else None

    if not entry:
        raise RuntimeError("RSS가 비어 있습니다.")

    print(f"✅ 수신: {entry.title}")

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

    def refine_title(raw_title):
        prompt = f"다음 뉴스 제목을 전문가 보고서 스타일로 자연스럽게 다듬어주세요. 키워드나 주석은 포함하지 마세요. 순수한 제목만 출력하세요.\n\n제목: \"{raw_title}\""
        try:
            print("▶ 제목 재작성 요청")
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=100
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print("❌ 제목 재작성 실패:", e)
            return raw_title

    refined_title = refine_title(entry.title)

    def get_structured_data():
        safe_title = json.dumps(refined_title)
        safe_text = json.dumps(full_text)
        prompt = (
            f"기사 제목: {safe_title}\n본문:\n{safe_text}\n\n"
            "아래 형식으로 JSON으로 구성하여 구조화하고 분석가의 인사이트가 반영된 표현을 사용하세요:\n"
            "- slug_keywords: 핵심 키워드 3~5개 (제목에는 포함하지 않음)\n"
            "- sections: subtitle(소제목), paragraph(해설), image_prompt(이미지 생성용)\n"
            "- one_liner: 전체 내용 요약\n"
            "- opinion: 분석 및 전망 (SEO 최적화된 어휘 사용)\n"
            "- related_tags: 연관 태그 배열\n"
            "```json\n"
            "{\n"
            f'  "title": {safe_title},\n'
            '  "slug_keywords": ["키워드1", "키워드2"],\n'
            '  "sections": [\n'
            '    {"subtitle": "소제목", "paragraph": "...", "image_prompt": "..."}\n'
            '  ],\n'
            '  "one_liner": "...",\n'
            '  "opinion": "...",\n'
            '  "related_tags": ["태그1", "태그2"]\n'
            "}\n```"
        )
        for i in range(2):
            try:
                print(f"▶ 구조화 요청 시도 {i+1}")
                resp = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )
                raw = resp.choices[0].message.content or ""
                if raw.startswith("```"):
                    raw = "\n".join(raw.splitlines()[1:-1])
                return json.loads(raw)
            except Exception as e:
                print(f"❌ 구조화 실패 ({i+1}):", e)
                time.sleep(1)
        return {
            "title": refined_title,
            "slug_keywords": [],
            "sections": [{"subtitle": refined_title, "paragraph": full_text[:200], "image_prompt": None}],
            "one_liner": full_text[:100] + "…",
            "opinion": "",
            "related_tags": []
        }

    data = get_structured_data()

    def generate_excerpt(text):
        prompt = f"다음 내용을 100자 이내로 블로그 요약용 문장으로 만들어줘:\n\n{text}"
        try:
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=120
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print("❌ 요약 생성 실패:", e)
            return text[:100] + "…"

    excerpt = generate_excerpt(full_text)

    raw_slug = "-".join(data.get("slug_keywords", [])[:4])
    slug = re.sub(r'[^a-z0-9\-]', '', raw_slug.lower()) or f"post-{int(time.time())}"

    def gen_and_upload(prompt, tag):
        if not prompt:
            print(f"⚠️ 프롬프트 없음 ({tag})")
            return None, None
        try:
            full_prompt = prompt + " editorial infographic, clean layout"
            url = client.images.generate(prompt=full_prompt, n=1, size="512x512").data[0].url
            img_data = requests.get(url, timeout=20).content
            img = Image.open(BytesIO(img_data)).convert("RGB").resize((512, 512))
            buf = BytesIO(); img.save(buf, format="JPEG", quality=60)
        except Exception as e:
            print(f"❌ 이미지 생성 실패 ({tag}):", e)
            return None, None

        media = {
            "name": f"{slug}-{tag}.jpg",
            "type": "image/jpeg",
            "caption": data["one_liner"],
            "description": data["opinion"],
            "bits": xmlrpc_client.Binary(buf.getvalue())
        }
        try:
            resp = wp.call(UploadFile(media))
            mid = resp.id if hasattr(resp, "id") else resp["id"]
            link = resp.link if hasattr(resp, "link") else resp["link"]
            return mid, link
        except Exception as e:
            print(f"❌ 업로드 실패 ({tag}):", e)
            return None, None

    keywords = data.get("slug_keywords", [])
    related_tags = data.get("related_tags", [])
    all_tags = keywords + related_tags

    subtitles = [sec["subtitle"] for sec in data["sections"]]
    combined_prompt = " ".join(subtitles + keywords)

    thumb_id, thumb_url = gen_and_upload(combined_prompt + " summary", "thumb")
    sec_id, sec_url = gen_and_upload(combined_prompt, "section")

    html = []
    if sec_url:
        html.append('<figure style="text-align:center;"><img src="' + sec_url + '" width="512"/></figure>')
    for sec in data["sections"]:
        html.append(f"<h2>{sec['subtitle']}</h2>")
        html.append(f"<p>{sec['paragraph']}</p>")
    html.append(f"<p><strong>한 줄 요약:</strong> {data['one_liner']}</p>")
    html.append(f"<h4 style='font-style:italic;color:#555'>{data['opinion']}</h4>")

    post = WordPressPost()
    post.title = refined_title
    post.slug = slug
    post.excerpt = excerpt
    post.content = "\n".join(html)
    post.post_status = "publish"
    post.terms_names = {"category": [CATEGORY], "post_tag": all_tags}
    if thumb_id:
        post.thumbnail = thumb_id

    print("▶ 업로드 중…")
    wp.call(NewPost(post))
    print("✅ 완료! 제목:", refined_title)

# 실행