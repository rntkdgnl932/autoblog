import collections
import collections.abc
collections.Iterable = collections.abc.Iterable

import re
import time
import json
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import quote

from openai import OpenAI
from env_ai import wp_id, wp_ps, keys

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.media import UploadFile
from wordpress_xmlrpc.compat import xmlrpc_client

print("▶ OpenAI 및 WordPress 클라이언트 초기화")
client = OpenAI(api_key=keys())
wp     = Client("https://hobbycolorful.com/xmlrpc.php", wp_id(), wp_ps())

def ask_ai_for_cast(title):
    print(f"▶ AI에게 등장인물 직접 요청: {title}")
    prompt = f"드라마 '{title}'의 출연 배우를 정확하게 알려줘. 배우이름(드라마속이름) 이렇게 나열해줘."
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=100
        )
        result = resp.choices[0].message.content.strip()
        names = [name.strip("•*- ") for name in result.split(',') if name.strip()]
        print("✅ AI가 제공한 인물 목록:", names)
        return names
    except Exception as e:
        print("⚠️ AI 등장인물 요청 실패:", e)
        return []

def generate_title(title):
    print(f"▶ 감정형 제목 생성 요청: {title}")
    prompt = f"드라마 '{title}'에 대해 감정이 섞인 제목(의문형 또는 감성형)을 지어줘. 원제는 반드시 포함해줘. 40자 이내."
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
        max_tokens=60
    )
    title = resp.choices[0].message.content.strip()
    print(f"✅ 제목 생성 완료: {title}")
    return title

def get_metadata_and_plot(title):
    print(f"▶ 메타데이터 및 줄거리 생성 요청: {title}")
    cast = ask_ai_for_cast(title)
    cast_str = ', '.join(cast) if cast else '정보 없음'

    prompt = f"""
드라마 제목: {title}
출연 배우: {cast_str}

아래 JSON 형식으로 출력해 주세요. 등장인물 설명은 반드시 위 배우 기준으로 작성해 주세요.
```json
{{
  "characters": [{{"name": "배우명", "description": "50~80자 인물 설명"}}, ...],
  "basic_info": "장르, 공개 플랫폼 등 핵심 정보 (200자 이내)",
  "one_liner": "감정 중심 인상적 한 문장 요약",
  "opinion": "리뷰어의 감정이 담긴 짧은 감상 (100자 이내)"
}}
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7,
        max_tokens=600
    )
    raw = resp.choices[0].message.content.strip()
    print(f"▶ 원시 메타데이터 응답: {raw[:100]}...")
    if raw.startswith("```"):
        raw = "\n".join(raw.splitlines()[1:-1])
    meta = json.loads(raw)
    print(f"✅ 메타데이터 파싱 완료: characters={len(meta['characters'])}, info={meta['basic_info'][:20]}...")

    plot_prompt = f"드라마 '{title}'의 줄거리를 감정 중심으로 시청자의 시선에서 약 1000자 내외로 서술해줘. 단순 요약이 아닌 느낌과 여운 중심으로."
    plot_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": plot_prompt}],
        temperature=0.9,
        max_tokens=1500
    )
    plot = plot_resp.choices[0].message.content.strip()
    print(f"✅ 줄거리 생성 완료 (길이: {len(plot)}자)")

    return meta, plot

# 나머지 코드는 기존과 동일하게 유지됩니다 (생략)...


def extract_emotion_tag(one_liner):
    if any(x in one_liner for x in ["슬픔", "비극", "눈물", "절망"]):
        return "sad"
    if any(x in one_liner for x in ["행복", "희망", "따뜻"]):
        return "happy"
    if any(x in one_liner for x in ["웃음", "유쾌", "코믹"]):
        return "joy"
    if any(x in one_liner for x in ["긴장", "스릴", "추격", "비밀"]):
        return "thrill"
    return "neutral"

def gen_scene_upload(prompt, tag, slug):
    print(f"▶ [{tag}] 이미지 생성 요청: {prompt}")
    img_url = client.images.generate(prompt=prompt, n=1, size="512x512").data[0].url
    time.sleep(1)
    resp = requests.get(img_url, timeout=20); resp.raise_for_status()
    img = Image.open(BytesIO(resp.content)).convert("RGB")

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=60)
    data = buf.getvalue()
    filename = f"{slug}_{tag}.jpg"

    media = {
        "name":        filename,
        "type":        "image/jpeg",
        "caption":     prompt,
        "description": f"{tag} 장면 이미지",
        "bits":        xmlrpc_client.Binary(data)
    }
    print(f"▶ [{tag}] UploadFile 호출")
    try:
        res = wp.call(UploadFile(media))
        mid  = getattr(res, "id", res["id"])
        murl = getattr(res, "link", res.get("link"))
        print(f"   ✅ [{tag}] 업로드 성공 id={mid}, url={murl}")
        return mid, murl
    except Exception as e:
        print(f"   ⚠️ [{tag}] 업로드 실패: {e}")
        return None, None

def drama_start(query, category):
    print(f"▶ WORKFLOW START: {query} in category '{category}'")
    meta, plot = get_metadata_and_plot(query)
    show_title = generate_title(query)

    slug_base = re.sub(r'[^\w\-]', '', re.sub(r'\s+', '-', show_title.strip().lower()))
    slug = slug_base if slug_base else f"post-{int(time.time())}"
    print(f"▶ 제목: {show_title}\n▶ slug: {slug}\n▶ 카테고리: {category}")
    print(f"▶ 메타 one-liner: {meta['one_liner']}")

    emotion = extract_emotion_tag(meta['one_liner'])
    face_expression = {
        "sad": "with a sad expression",
        "happy": "with a joyful smile",
        "joy": "with a bright and cheerful smile",
        "thrill": "with a tense, focused expression",
        "neutral": "with a calm expression"
    }[emotion]

    thumb_prompt = (
        f"A cinematic rear-view scene of a slim, 20-year-old East Asian woman {face_expression} "
        f"watching an emotional moment from '{query}' on TV"
    )
    thumb_id, thumb_url = gen_scene_upload(thumb_prompt, "thumb", slug)

    body_prompt = (
        f"A rear-view shot of a slim, beautiful 20-year-old East Asian woman {face_expression} "
        f"sitting comfortably and watching a powerful scene from '{query}' on a modern TV"
    )
    body_id, body_url = gen_scene_upload(body_prompt, "body", slug)

    html = []
    if body_url:
        html.append(
            '<figure style="text-align:center;">'
            f'<img src="{body_url}" width="512" alt="본문 이미지"/>'
            '</figure>'
        )
    html.append("<h2>등장인물</h2>")
    for ch in meta["characters"]:
        html.append(f"<h3>{ch['name']}</h3><p>{ch['description']}</p>")
    html.append(f"<h2>기본정보</h2><p>{meta['basic_info']}</p>")
    html.append(f"<h2>줄거리</h2><p>{plot}</p>")
    html.append(f'<p style="font-size:1.2em;"><strong>한 줄 요약:</strong> {meta["one_liner"]}</p>')
    html.append(f'<h4 style="font-style:italic;color:#555;">{meta["opinion"]}</h4>')

    tags = [query, slug, "drama", "review"]

    post = WordPressPost()
    post.title       = show_title
    post.slug        = slug
    post.excerpt     = meta["one_liner"]
    post.content     = "\n".join(html)
    post.post_status = "publish"
    post.terms_names = {"category": [category], "post_tag": tags}
    post.thumbnail   = thumb_id

    print("▶ WP POSTING...")
    print(f"  ▶ title: {post.title}")
    print(f"  ▶ excerpt: {post.excerpt}")
    print(f"  ▶ category: {post.terms_names['category']}")
    print(f"  ▶ tags: {post.terms_names['post_tag']}")
    print(f"  ▶ thumbnail ID: {post.thumbnail}")
    print(f"  ▶ content sample: {post.content[:100]}...")

    wp.call(NewPost(post))
    print("✅ 포스팅 완료:", show_title)
