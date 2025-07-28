import os
import json
import re
import requests
from bs4 import BeautifulSoup
import variable as v_

ORG_DB_PATH = "C:/my_games/auto_blog/mysettings/idpw/my_list.json"

# ✅ 1. 기관명 자동 추출 함수
def my_organization_list(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()

    raw_candidates = re.findall(r"([\w\uAC00-\uD7AF]{2,10}(청|부|처|공단|공사|위원회|원|센터|기금|재단|지원단|협회|지원센터))", text)
    cleaned = set()

    for org, _ in raw_candidates:
        if not re.search(r"[0-9]|[^\w\uAC00-\uD7AF]", org):
            cleaned.add(org.strip())

    return list(cleaned)

# ✅ 2. Google Custom Search로 대표번호 및 홈페이지 검색

def scan_internet(org_name):
    if not org_name:
        return

    try:
        if not os.path.exists(ORG_DB_PATH):
            os.makedirs(os.path.dirname(ORG_DB_PATH), exist_ok=True)
            with open(ORG_DB_PATH, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

        try:
            with open(ORG_DB_PATH, 'r', encoding='utf-8') as f:
                org_data = json.load(f)
        except json.JSONDecodeError:
            backup_path = ORG_DB_PATH + ".bak"
            os.rename(ORG_DB_PATH, backup_path)
            print(f"[!] JSON 오류 발생 - 백업 저장: {backup_path}")
            org_data = {}

        print(f"[WEB] 검색중: {org_name}")

        # 🔍 1차 검색: 홈페이지
        query_home = f"{org_name}"
        resp_home = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": v_.my_google_custom_api,
                "cx": v_.my_google_custom_id,
                "q": query_home,
                "num": 3
            }
        )
        results_home = resp_home.json()
        site_url = ""
        for item in results_home.get("items", []):
            link = item.get("link", "")
            if re.search(r"https?://[\w\.-]*\.(go\.kr|or\.kr|co\.kr|ac\.kr|re\.kr|ne\.kr|pe\.kr|com|net|org|edu|kr)", link):
                site_url = link
                break

        # 🔍 2차 검색: 전화번호
        query_phone = f"{org_name} 대표번호"
        resp_phone = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": v_.my_google_custom_api,
                "cx": v_.my_google_custom_id,
                "q": query_phone,
                "num": 3
            }
        )
        results_phone = resp_phone.json()
        phone = ""
        for item in results_phone.get("items", []):
            snippet = item.get("snippet", "")
            phone_match = re.search(r"(0\d{1,2}-\d{3,4}-\d{4})", snippet)
            if phone_match:
                phone = phone_match.group(1)
                break

        # ✅ 저장 (기존값도 덮어쓰기)
        if phone and site_url:
            org_data[org_name] = {"전화": phone, "사이트": site_url}
            print(f"[+] 저장완료: {org_name} ({phone}, {site_url})")
        else:
            print(f"[-] 검색 실패: {org_name} - phone: {phone}, url: {site_url}")

        with open(ORG_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(org_data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"[ERROR] {org_name} 검색 중 오류: {e}")

# ✅ 3. HTML에서 기관명 관련 전화/사이트를 자동 대체 (중복 h2 제거 포함)
def last_upload_ready(html_content):
    if not os.path.exists(ORG_DB_PATH):
        return html_content

    with open(ORG_DB_PATH, 'r', encoding='utf-8') as f:
        org_data = json.load(f)

    # 🔍 중복 <h2> 제거
    soup = BeautifulSoup(html_content, 'html.parser')
    seen_h2 = set()
    for h2 in soup.find_all("h2"):
        text = h2.get_text(strip=True)
        if text in seen_h2:
            h2.decompose()
        else:
            seen_h2.add(text)

    html_content = str(soup)

    # 🧠 GPT 최종검수를 위한 패턴 기반 교체
    def replace_info(match):
        full_text = match.group(0)
        for org, info in org_data.items():
            if org in full_text:
                result = full_text
                if re.search(r"전화|대표번호|고객센터", full_text):
                    result = f"{org} 대표전화: {info['전화']}"
                if re.search(r"홈페이지|사이트|공식 홈페이지", full_text):
                    result = f'{org} (<a href="{info["사이트"]}" target="_blank" rel="noopener">공식 홈페이지</a>)'
                return result
        return full_text

    pattern = r"([\w\uAC00-\uD7AF]{2,10}(청|부|처|공단|공사|위원회|원|센터|기금|재단|지원단|협회|지원센터))[^<\n]{0,40}(전화|대표번호|고객센터|홈페이지|사이트|공식 홈페이지)"
    html_content = re.sub(pattern, replace_info, html_content)

    return html_content
