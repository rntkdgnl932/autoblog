import re
import json
import time
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import quote

from openai import OpenAI
from env_ai import wp_id, wp_ps, keys

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.media import UploadFile
from wordpress_xmlrpc.compat import xmlrpc_client

# ――― 설정 ―――
print("▶ 초기화: OpenAI·WP 연결")
client   = OpenAI(api_key=keys())
wp       = Client("https://hobbycolorful.com/xmlrpc.php", wp_id(), wp_ps())

CATEGORY = "HobbyGreen(리뷰)"
QUERY    = "동백꽃 필 무렵"

# ―― 1) 방송사·주연 추출 ――
def fetch_info_from_wiki(title):
    url = f"https://ko.wikipedia.org/wiki/{quote(title)}"
    try:
        r = requests.get(url, timeout=10); r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        box = soup.select_one("table.infobox")
        company, cast = None, []
        if box:
            for row in box.select("tr"):
                th, td = row.select_one("th"), row.select_one("td")
                if not th or not td: continue
                h, txt = th.text.strip(), td.get_text(" ", strip=True)
                if not company and re.search(r"(방영 채널|방송사)", h):
                    company = txt.split()[0]
                if re.search(r"(주연|출연)", h):
                    for part in re.split(r"<br\s*/?>|,|\n", str(td)):
                        n = BeautifulSoup(part, "html.parser").get_text().strip()
                        if n: cast.append(n)
                    break
        return (company or "KBS"), cast
    except:
        return "KBS", []

COMPANY, CAST = fetch_info_from_wiki(QUERY)
SHOW_TITLE = f"{COMPANY} 방영 {QUERY} 줄거리·등장인물"
KEYWORDS   = [COMPANY.lower(), QUERY.replace(" ", "").lower(), "drama"]
print(f"DEBUG → COMPANY={COMPANY}, CAST={CAST}")
print(f"DEBUG → SHOW_TITLE={SHOW_TITLE}, KEYWORDS={KEYWORDS}")

# ―― 2) 메타 생성 ――
def get_full_metadata():
    prompt = f"""
드라마 제목: {QUERY}
방송사: {COMPANY}
주연 배우: {', '.join(CAST)}

아래 JSON 양식으로 응답해 주세요:
```json
{{
  "characters":[
    {{ "name":"배우1","description":"인물 소개(50~80자)" }},
    ...
  ],
  "basic_info":"방영사·기간·장르 등(200자 내외)",
  "one_liner":"한 줄 요약",
  "opinion":"추천 포인트(100자 내외)"
}}
```"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7, max_tokens=600
    )
    raw = resp.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = "\n".join(raw.splitlines()[1:-1])
    try:
        data = json.loads(raw)
    except:
        data = {
            "characters":[{"name":n,"description":""} for n in CAST],
            "basic_info":f"{COMPANY} 방영 | 주연 {'·'.join(CAST)}",
            "one_liner":"",
            "opinion":""
        }
    print(f"DEBUG → META={data}")
    return data

META = get_full_metadata()

# ―― 3) 줄거리 생성 ――
def generate_plot():
    prompt = f"드라마 '{QUERY}' 줄거리를 한국어로 약 1000자 내외, 스포일러 없이 작성해 주세요."
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.8, max_tokens=1500
    )
    plot = resp.choices[0].message.content.strip()
    print(f"DEBUG → plot length={len(plot)}")
    return plot

PLOT = generate_plot()

# ―― 4) 포스터 URL 두 개 수집 (헤더·파라미터 보강) ――
def fetch_two_posters():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    params = {
        "q": f"드라마 {QUERY} 포스터",
        "first": "1",
        "count": "50",
        "mkt": "ko-KR",
        "safeSearch": "Off",
    }
    print(f"DEBUG → 이미지 검색 요청 params={params}")
    r = requests.get("https://www.bing.com/images/search",
                     params=params, headers=headers, timeout=10)
    print("DEBUG → HTTP 상태:", r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")
    tags = soup.select("a.iusc")
    print("DEBUG → iusc 태그 개수:", len(tags))
    urls = []
    for tag in tags:
        raw = tag.get("m")
        if not raw:
            continue
        info = json.loads(raw)
        url = info.get("murl")
        if url and re.search(r'\.(?:jpe?g|png)$', url, re.IGNORECASE):
            urls.append(url)
            print("  ▶ 후보 URL:", url)
            if len(urls) == 2:
                break
    while len(urls) < 2:
        urls.append(None)
    print(f"DEBUG → 선택된 포스터 URL 2개: {urls}")
    return urls[0], urls[1]

# ―― 5) 다운로드 헬퍼 ――
def robust_get(url, retries=3):
    for i in range(retries):
        try:
            r = requests.get(url, timeout=10); r.raise_for_status()
            print(f"DEBUG → 다운로드 성공 ({i+1}/{retries})")
            return r.content
        except Exception as e:
            print(f"  ⚠️ 다운로드 실패 ({i+1}/{retries}):", e)
            time.sleep(1)
    return None

# ―― 6) XML-RPC 업로드 (512×512) ――
def upload_via_xmlrpc(img_b, tag):
    buf = BytesIO()
    Image.open(BytesIO(img_b)).convert("RGB") \
         .resize((512,512), Image.LANCZOS) \
         .save(buf, "JPEG", quality=60, optimize=True)
    data = buf.getvalue()
    filename = "-".join(KEYWORDS + [tag]) + ".jpg"
    media = {
        "name": filename,
        "type": "image/jpeg",
        "caption": "",
        "description": "",
        "bits": xmlrpc_client.Binary(data)
    }
    print(f"▶ XML-RPC 업로드 시도 ({tag})")
    res = wp.call(UploadFile(media))
    mid  = getattr(res, "id", res["id"])
    link = getattr(res, "link", res.get("link"))
    print(f"  ✅ 업로드 성공 ({tag}) id={mid}")
    return mid, link

# ―― 7) 워크플로우 ――
def drama_start():
    print("▶ 워크플로우 시작")
    thumb_url, body_url = fetch_two_posters()

    thumb_id = None
    if thumb_url:
        img = robust_get(thumb_url)
        if img:
            thumb_id, _ = upload_via_xmlrpc(img, "thumb")

    body_id = body_link = None
    if body_url:
        img = robust_get(body_url)
        if img:
            body_id, body_link = upload_via_xmlrpc(img, "body")

    html = []
    if body_link:
        html.append(
            '<figure style="text-align:center;">'
            f'<img src="{body_link}" width="512" alt="본문 포스터"/>'
            f'<figcaption>출처: {body_url}</figcaption>'
            '</figure>'
        )

    html.append("<h2>등장인물</h2>")
    for ch in META["characters"]:
        html.append(f"<h3>{ch['name']}</h3><p>{ch['description']}</p>")

    html.append("<h2>기본정보</h2><p>" + META["basic_info"] + "</p>")
    html.append("<h2>줄거리</h2><p>" + PLOT + "</p>")
    html.append(
        f'<p style="font-size:1.2em;"><strong>한 줄 요약:</strong> {META["one_liner"]}</p>'
    )
    html.append(
        f'<h4 style="font-style:italic;color:#555;">{META["opinion"]}</h4>'
    )

    post = WordPressPost()
    post.title       = SHOW_TITLE
    post.slug        = re.sub(r'[^a-z0-9\-]', '', SHOW_TITLE.lower().replace(" ", "-"))
    post.excerpt     = PLOT[:80].rsplit(" ",1)[0] + "…"
    post.content     = "\n".join(html)
    post.post_status = "publish"
    post.terms_names = {"category":[CATEGORY], "post_tag":KEYWORDS}
    if thumb_id:
        post.thumbnail = thumb_id

    print("▶ 워드프레스 업로드 중…")
    wp.call(NewPost(post))
    print("✅ 게시 완료:", post.slug)
