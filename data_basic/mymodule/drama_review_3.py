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
from bs4 import BeautifulSoup

# ――― 공통 클라이언트 초기화 ―――
client = OpenAI(api_key=keys())
wp     = Client("https://hobbycolorful.com/xmlrpc.php", wp_id(), wp_ps())

def overlay_text(img: Image.Image, text: str, font_size=36) -> Image.Image:
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("NanumGothic.ttf", font_size)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (img.width - w) // 2
    y = img.height - h - 30
    box = Image.new("RGBA", (w + 30, h + 20), (0, 0, 0, 200))
    img.paste(box, (x - 15, y - 10), box)
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    return img

def fetch_info_from_wiki(title):
    """
    1) 위키피디아 infobox에서 방송사·주연 추출
    2) 방송사 정보가 없으면, OpenAI에 질문하여 정확한 방송사를 받아옴
    """
    url = f"https://ko.wikipedia.org/wiki/{quote(title)}"
    company = None
    cast = []
    try:
        r = requests.get(url, timeout=10); r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        box = soup.select_one("table.infobox")
        if box:
            for row in box.select("tr"):
                th, td = row.select_one("th"), row.select_one("td")
                if not th or not td:
                    continue
                h, txt = th.text.strip(), td.get_text(" ", strip=True)
                if not company and re.search(r"(방영 채널|방송사)", h):
                    company = txt.split()[0]
                if re.search(r"(주연|출연)", h):
                    for part in re.split(r"<br\s*/?>|,|\n", str(td)):
                        name = BeautifulSoup(part, "html.parser").get_text().strip()
                        if name:
                            cast.append(name)
                    # 주연 뒤엔 더 이상 안봐도 됨
                    break
    except Exception as e:
        print("⚠️ 위키 크롤링 오류:", e)

    # 방송사 정보가 없으면 OpenAI에게 물어보기
    if not company:
        print("▶ 방송사 정보 누락, OpenAI에 요청 중…")
        prompt = (
            f"다음 드라마가 어느 방송사에서 방영되었는지 알려주세요: '{title}'\n"
            "정확한 채널명만 한 단어로 응답해 주세요."
        )
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=10
            )
            answer = resp.choices[0].message.content.strip()
            # 간단 정제: 띄어쓰기 제거
            company = re.split(r"\s|,|\.", answer)[0]
            print("   ▶ OpenAI 방송사 응답:", company)
        except Exception as e:
            print("⚠️ OpenAI 방송사 요청 실패:", e)
            company = "알수없음"

    return company, cast

def get_full_metadata(query, company, cast):
    prompt = f"""
드라마 제목: {query}
방송사: {company}
주연 배우: {', '.join(cast) or '정보없음'}

위 정보를 바탕으로 아래 JSON을 출력하세요:
```json
{{
  "characters":[{{"name":"배우1","description":"인물소개(50~80자)"}}…],
  "basic_info":"방영사·기간·장르 등(200자)",
  "one_liner":"한 줄 요약",
  "opinion":"추천 포인트(100자)"
}}
```"""
    print("▶ 메타 생성 요청")
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7, max_tokens=600
    )
    raw = resp.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = "\n".join(raw.splitlines()[1:-1])
    try:
        meta = json.loads(raw)
    except Exception as e:
        print("⚠️ 메타 JSON 파싱 실패:", e)
        meta = {
            "characters":[{"name":n,"description":""} for n in cast],
            "basic_info":f"{company} 방영 | 주연 {'·'.join(cast)}",
            "one_liner":"", "opinion":""
        }
    return meta

def generate_plot(query):
    prompt = f"드라마 '{query}' 줄거리를 한국어로 약 1000자 내외, 스포일러 없이 작성"
    print("▶ 줄거리 생성 요청")
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.8, max_tokens=1500
    )
    return resp.choices[0].message.content.strip()

def gen_scene_upload(prompt, tag, slug):
    print(f"▶ [{tag}] 이미지 생성 요청: {prompt}")
    img_url = client.images.generate(prompt=prompt, n=1, size="512x512").data[0].url
    time.sleep(1)
    resp = requests.get(img_url, timeout=20); resp.raise_for_status()
    img = Image.open(BytesIO(resp.content)).convert("RGB")

    # quality=60, no resize, 뒷모습 prompt 이미 장면 포함
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
        print(f"   ✅ [{tag}] 업로드 성공 id={mid}")
        return mid, murl
    except Exception as e:
        print(f"   ⚠️ [{tag}] 업로드 실패:", e)
        return None, None

def drama_start(query, category):
    slug       = re.sub(r'[^a-z0-9\-]', '', query.replace(" ", "-").lower())
    show_title = f"{query} 리뷰·줄거리"
    keywords   = [slug, "drama", "review"]

    print(f"▶ WORKFLOW START: {query} in category {category}")

    # 1) 방송사·주연
    company, cast = fetch_info_from_wiki(query)
    print(f"   ▶ COMPANY={company}, CAST={cast}")

    # 2) 메타 & 줄거리
    meta = get_full_metadata(query, company, cast)
    plot = generate_plot(query)

    # 3) 이미지 업로드
    thumb_prompt = (
        f"A cinematic rear-view scene of a slim, model-like 20-year-old East Asian woman "
        f"watching an emotional moment from '{query}' on TV"
    )
    thumb_id, thumb_url = gen_scene_upload(thumb_prompt, "thumb", slug)

    body_prompt = (
        f"A rear-view shot of a slim, beautiful 20-year-old East Asian woman "
        f"sitting comfortably and watching a powerful scene from '{query}' on a modern TV"
    )
    body_id, body_url = gen_scene_upload(body_prompt, "body", slug)

    # 4) HTML 구성
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
    html.append(
        f'<p style="font-size:1.2em;"><strong>한 줄 요약:</strong> {meta["one_liner"]}</p>'
    )
    html.append(
        f'<h4 style="font-style:italic;color:#555;">{meta["opinion"]}</h4>'
    )

    # 5) WP 포스팅
    post = WordPressPost()
    post.title       = show_title
    post.slug        = slug
    post.excerpt     = meta["one_liner"]
    post.content     = "\n".join(html)
    post.post_status = "publish"
    post.terms_names = {"category":[category], "post_tag":keywords}
    post.thumbnail   = thumb_id

    print("▶ WP POSTING…")
    wp.call(NewPost(post))
    print("✅ 포스팅 완료:", show_title)

# 사용 예시:
# drama_start("나의 해방일지", "HobbyGreen(리뷰)")
