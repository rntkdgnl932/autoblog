from wordpress_xmlrpc.methods.media import UploadFile  # ✅ 이거 꼭 추가!
from wordpress_xmlrpc.compat import xmlrpc_client
from openai import OpenAI
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import GetPost, EditPost

import time
import variable as v_
from gas_start import (
    optimize_html_for_seo_with_gpt,
    summarize_for_description,
    stable_diffusion
)
from bs4 import BeautifulSoup
import re

# ✅ 후처리 함수
def postprocess_html_for_blog(html: str, keyword: str) -> str:
    def remove_nested_a_tags(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for a_tag in soup.find_all("a"):
            nested_links = a_tag.find_all("a")
            for nested in nested_links:
                nested.unwrap()
        return str(soup)

    def remove_whitespace_before_images(html: str) -> str:
        return re.sub(r'(\s*<br\s*/?>\s*)*(<img[^>]+>)', r'\2', html)

    def clean_ul_paragraphs(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for ul in soup.find_all("ul"):
            for p in ul.find_all("p"):
                p.unwrap()
        return str(soup)

    def boldify_keyword_once(html: str, keyword: str) -> str:
        pattern = re.escape(keyword)
        return re.sub(pattern, f"<strong>{keyword}</strong>", html, count=1)

    html = remove_nested_a_tags(html)
    html = remove_whitespace_before_images(html)
    html = clean_ul_paragraphs(html)
    html = boldify_keyword_once(html, keyword)

    return html


# ✅ 핵심: 기존 글 리디자인 후 업데이트
def redesign_existing_post(post_id: int):
    print(f"▶ 기존 글 리디자인 시작 - ID: {post_id}")
    wp = Client(v_.domain_adress + "/xmlrpc.php", v_.wd_id, v_.wd_pw)
    client = OpenAI(api_key=v_.api_key, timeout=30)

    post = wp.call(GetPost(post_id))
    original_html = post.content
    title = post.title
    keyword = title.strip().split(" ")[0]

    # ✅ 본문 이미지 생성
    image_html = ""
    try:
        scene_media = stable_diffusion(client, original_html, "scene", f"{keyword} 본문 이미지", str(post_id))
        if scene_media:
            upload_result = wp.call(UploadFile(scene_media))
            scene_url = upload_result.link  # 객체 접근
            image_html = f"<img src='{scene_url}' style='display:block; margin:auto;' alt='{keyword}'><br>"
            print(f"🖼 본문 이미지 삽입 완료: {scene_url}")
    except Exception as e:
        print(f"⚠️ 이미지 생성 또는 업로드 실패: {e}")

    # ✅ 요약
    one_line = summarize_for_description(client, original_html, title=title, keyword=keyword)

    # ✅ GPT 구조화
    html_with_image = f"{image_html}{original_html}"
    try:
        new_html = optimize_html_for_seo_with_gpt(client, html_with_image, keyword, one_line_summary=one_line)
    except Exception as e:
        print("❌ GPT 구조화 실패:", e)
        new_html = html_with_image  # 원문 그대로 유지

    # 후처리 후 비어 있으면 원문 유지
    final_html = postprocess_html_for_blog(new_html, keyword)
    if not final_html.strip():
        final_html = original_html

    # ✅ 후처리
    final_html = postprocess_html_for_blog(new_html, keyword)

    # ✅ 글 덮어쓰기
    post.content = final_html
    post.thumbnail = None  # 오류 방지용

    wp.call(EditPost(post_id, post))
    print(f"✅ 수정 완료 - {title} (ID: {post_id})")


# ✅ 여러 글 반복 처리 예시



def redesign_existing_post(post_id: int):
    from gas_start import summarize_for_description, stable_diffusion, optimize_html_for_seo_with_gpt

    print(f"▶ 기존 글 리디자인 시작 - ID: {post_id}")
    wp = Client(v_.domain_adress + "/xmlrpc.php", v_.wd_id, v_.wd_pw)
    client = OpenAI(api_key=v_.api_key, timeout=30)

    post = wp.call(GetPost(post_id))
    original_html = post.content
    title = post.title
    keyword = title.strip().split(" ")[0]

    # ✅ 한줄 요약 생성 (실패 시 대비)
    try:
        one_line = summarize_for_description(client, original_html, title=title, keyword=keyword)
    except Exception as e:
        print("❌ 요약 실패:", e)
        one_line = ""

    # ✅ 본문 이미지 생성
    try:
        scene_media = stable_diffusion(client, original_html, "scene", f"{keyword} 본문 이미지", str(post_id))
        if scene_media:
            res = wp.call(UploadFile(scene_media))
            scene_url = getattr(res, "link", res.get("link"))
            image_html = f"<img src='{scene_url}' style='display:block; margin:auto;' alt='{keyword}'><br>"
        else:
            image_html = ""
    except Exception as e:
        print("⚠️ 이미지 생성 실패:", e)
        image_html = ""

    # ✅ GPT 최적화 재작성
    try:
        html_with_image = f"{image_html}{original_html}"
        new_html = optimize_html_for_seo_with_gpt(client, html_with_image, keyword, one_line_summary=one_line)
    except Exception as e:
        print("❌ GPT 재작성 실패:", e)
        new_html = ""

    # ✅ 후처리
    final_html = postprocess_html_for_blog(new_html, keyword)

    # 🔒 GPT 실패 시 원래 글 유지
    if not final_html.strip():
        print("❌ 최종 HTML이 비어 있음 - 기존 글 유지")
        final_html = original_html

    # ✅ 글 수정 반영
    post.content = final_html
    post.thumbnail = None
    wp.call(EditPost(post_id, post))

    print(f"✅ 수정 완료 - {title} (ID: {post_id})")


