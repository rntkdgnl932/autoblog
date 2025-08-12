# naver_cafe_auto_post_v3.py
# - HTML 비지원 대비 텍스트 변환
# - 제목/본문 필드 오탐 방지 (iframe/placeholder/contenteditable 우선)
# - '말머리' 등 필수값 자동 처리 + 등록 실패 시 재시도
# - 등록 성공 여부를 URL/토스트/네트워크로 다각도 확인

import re
import time
import html
import traceback
from pathlib import Path
from typing import List, Optional

from playwright.sync_api import Playwright, sync_playwright, expect, Error

COOKIES_FILE = Path("naver_cookies.json")

# ===== 설정 =====
CLUB_ID = "27960969"
MENU_ID = "55"
WRITE_URL = f"https://cafe.naver.com/ca-fe/cafes/{CLUB_ID}/menus/{MENU_ID}/articles/write?boardType=L"

POST_TITLE = "[자동업로드] 예시 제목입니다"
POST_HTML = """
<h2>자동 업로드 본문 예시</h2>
<p>이 글은 Playwright로 자동 업로드되었습니다.</p>
<ul>
  <li>항목 1</li>
  <li>항목 2</li>
</ul>
<p><em>이미지도 함께 업로드할 수 있어요.</em></p>
"""
IMAGE_PATHS: List[str] = [
    # r"C:\path\to\image1.jpg",
]

# HTML 을 카페 친화 텍스트로 변환할지 여부 (권장: True)
FORCE_PLAIN_TEXT = True

# 말머리(필수인 게시판 대비): None이면 자동으로 첫 유효 옵션 선택
REQUIRED_HEADWORD: Optional[str] = None  # 예: "정보", "일반", None

# ===== 로깅 =====
def debug(m): print(f"[DEBUG] {m}")
def info(m):  print(f"[INFO]  {m}")
def warn(m):  print(f"[WARN]  {m}")

# ===== 유틸 =====
def sanitize_html_to_text(html_src: str) -> str:
    import re, html as _html
    t = re.sub(r"</(h[1-6]|p|li)>", "\n", html_src, flags=re.I)
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"<li[^>]*>", "• ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    t = _html.unescape(t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def is_login_page(url: str) -> bool:
    return "nid.naver.com/nidlogin.login" in url

def with_retry(fn, retries=3, delay=0.8):
    for i in range(retries):
        try:
            return fn()
        except Error as e:
            if "Execution context was destroyed" in str(e) or "Target closed" in str(e):
                time.sleep(delay)
                continue
            raise
    raise

# ===== Playwright 컨텍스트 =====
def create_context(playwright: Playwright, headless: bool):
    browser = playwright.chromium.launch(headless=headless, channel="chrome", slow_mo=50)
    if COOKIES_FILE.exists() and COOKIES_FILE.stat().st_size > 0:
        info("쿠키 파일 발견. storage_state로 복원합니다.")
        context = browser.new_context(
            storage_state=str(COOKIES_FILE),
            locale="ko-KR",
            timezone_id="Asia/Seoul",
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"),
        )
    else:
        info("쿠키 파일 없음. 새 컨텍스트로 시작합니다.")
        context = browser.new_context(
            locale="ko-KR",
            timezone_id="Asia/Seoul",
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"),
        )
    return context

def save_state(context):
    context.storage_state(path=str(COOKIES_FILE))
    info(f"쿠키 저장 완료 → {COOKIES_FILE.resolve()}")

def ensure_logged_in(context, return_to_url: Optional[str] = None):
    page = context.new_page()
    page.goto("https://www.naver.com", timeout=60_000)
    info("네이버 메인 진입. 로그인 페이지로 이동합니다.")
    page.goto("https://nid.naver.com/nidlogin.login", timeout=60_000)

    warn("브라우저에서 직접 로그인(2단계/보안인증 포함)을 완료하세요.")
    input("▶ 로그인 완료 후 콘솔에서 엔터를 누르면 계속합니다...")

    page.goto("https://www.naver.com", timeout=60_000)
    time.sleep(1)
    save_state(context)

    if return_to_url:
        page.goto(return_to_url, timeout=60_000)
        time.sleep(1)
    page.close()

# ===== 글쓰기/에디터 탐색 =====
def get_editor_frame(page):
    # URL로 먼저 후보 (프레임 URL이 글쓰기 포함일 수 있음)
    for f in page.frames:
        try:
            if "/articles/write" in (f.url or ""):
                return f
        except Exception:
            continue

    # placeholder / contenteditable 기반 탐색
    title_sels = [
        "input[name=title]", "textarea[name=title]",
        "input[placeholder*='제목']", "textarea[placeholder*='제목']",
    ]
    body_sels = [
        "[contenteditable='true'][data-placeholder*='내용']",  # 우선
        "[contenteditable='true']", "div[role='textbox']",
        # 일부 스킨은 textarea 계열 사용
        "textarea[placeholder*='내용']", "textarea:not([name=title])",
        "div.ql-editor", "div.CodeMirror textarea",
    ]
    for f in page.frames:
        try:
            for sel in title_sels + body_sels:
                if f.locator(sel).first.count() > 0:
                    return f
        except Exception:
            continue
    return page

def wait_until_write_ready(context, page, target_url, timeout_ms=90000):
    start = time.time()
    while True:
        if is_login_page(page.url):
            time.sleep(2.0)
            if is_login_page(page.url):
                page.close()
                ensure_logged_in(context, return_to_url=target_url)
                page = context.new_page()
                page.goto(target_url, timeout=60_000)

        try:
            page.wait_for_load_state("networkidle", timeout=10_000)
        except Exception:
            pass

        # 글쓰기 URL이면 프레임 확인
        if "/articles/write" in page.url:
            frm = get_editor_frame(page)
            if frm is not None:
                info("카페 글쓰기 페이지 로딩/안정화 완료")
                return page, frm

        if (time.time() - start) * 1000 > timeout_ms:
            raise TimeoutError(f"글쓰기 페이지 안정화 타임아웃. 현재 URL: {page.url}")

def open_write_page(context, page, url):
    debug(f"글쓰기 URL 진입: {url}")
    page.goto(url, timeout=60_000)
    page.wait_for_load_state("domcontentloaded")
    return wait_until_write_ready(context, page, url, timeout_ms=90000)

# ===== 필드 입력 =====
def set_title(page, frame, title: str):
    """
    네이버 카페 새 에디터: 제목은 페이지 레벨, 본문은 프레임일 수 있음.
    페이지와 프레임 모두에서 안전하게 탐색.
    """
    # 0) 공통 후보 셀렉터
    title_selectors = [
        'input[placeholder="제목을 입력해 주세요."]',
        'input[placeholder*="제목"]',
        'textarea[placeholder*="제목"]',
        'input[name="title"]',
        'textarea[name="title"]',
        'input[type="text"]',
    ]

    # 1) Playwright의 get_by_placeholder (정확 매칭)
    try:
        el = page.get_by_placeholder("제목을 입력해 주세요.")
        if el.count() > 0:
            el.first.click()
            try: el.first.fill("")
            except: pass
            el.first.type(title, delay=8)
            info(f"제목 입력 완료(페이지 레벨): {title}")
            return
    except Exception:
        pass

    try:
        el = frame.get_by_placeholder("제목을 입력해 주세요.")
        if el.count() > 0:
            el.first.click()
            try: el.first.fill("")
            except: pass
            el.first.type(title, delay=8)
            info(f"제목 입력 완료(프레임 레벨): {title}")
            return
    except Exception:
        pass

    # 2) CSS 셀렉터: 페이지 → 프레임 순으로 시도
    for sel in title_selectors:
        el = page.locator(sel).first
        if el.count() > 0 and el.is_visible():
            try:
                el.click(force=True, timeout=800)
            except:
                pass
            try: el.fill("")
            except: pass
            el.type(title, delay=8)
            info(f"제목 입력 완료(페이지 CSS): {title}")
            return

    for sel in title_selectors:
        el = frame.locator(sel).first
        if el.count() > 0 and el.is_visible():
            try:
                el.click(force=True, timeout=800)
            except:
                pass
            try: el.fill("")
            except: pass
            el.type(title, delay=8)
            info(f"제목 입력 완료(프레임 CSS): {title}")
            return

    # 3) 컨테이너 근처 탐색(말머리 영역 근처의 input)
    try:
        container = page.locator('div:has(button:has-text("말머리"))').first
        candidate = container.locator("input[type='text']").first
        if candidate.count() > 0 and candidate.is_visible():
            candidate.click()
            try: candidate.fill("")
            except: pass
            candidate.type(title, delay=8)
            info(f"제목 입력 완료(컨테이너 근처): {title}")
            return
    except Exception:
        pass

    # 전부 실패 시 에러
    raise RuntimeError("제목 필드를 찾지 못했습니다. (페이지/프레임 모두 탐색 실패)")


def set_headword_if_required(frame, preferred: Optional[str] = REQUIRED_HEADWORD):
    """
    말머리(필수인 게시판 대비) 자동 선택.
    스킨마다 다르므로 여러 후보 시도.
    """
    # 열기 버튼 후보
    open_btns = [
        "button:has-text('말머리')",
        "[aria-label*='말머리']",
        "div:has-text('말머리') button",
    ]
    for sel in open_btns:
        btn = frame.locator(sel).first
        if btn.count() > 0:
            try:
                btn.click()
                time.sleep(0.4)
                # 옵션 후보
                options = frame.locator("ul[role='listbox'] li, div[role='listbox'] div[role='option']")
                if options.count() == 0:
                    # 다른 스킨
                    options = frame.locator("li[role='option'], button[role='option']")
                if options.count() > 0:
                    chosen = False
                    if preferred:
                        for i in range(options.count()):
                            t = options.nth(i).inner_text().strip()
                            if preferred in t:
                                options.nth(i).click()
                                chosen = True
                                break
                    if not chosen:
                        # 첫 유효항목 선택(보통 0번은 '선택'일 수 있어 1번부터)
                        idx = 1 if options.count() > 1 else 0
                        options.nth(idx).click()
                    info("말머리 선택 완료")
                    return
            except Exception:
                continue
    # 말머리 UI가 없거나, 필수 아님
    debug("말머리 UI를 찾지 못했거나 필수 아님으로 판단")

def switch_to_html_mode_if_possible_in_frame(frame):
    candidates = [
        "button:has-text('HTML')", "button[aria-label*='HTML']",
        "button[title*='HTML']", "div[role='toolbar'] button:has-text('HTML')",
    ]
    for sel in candidates:
        btn = frame.locator(sel).first
        if btn.count() > 0:
            try:
                btn.click()
                info("에디터: HTML 모드 전환 시도")
                time.sleep(0.5)
                return True
            except Exception:
                continue
    warn("HTML 모드 버튼을 찾지 못함 → 일반 모드 입력 시도")
    return False

def fill_body_in_frame(page, frame, content: str, force_plain: bool = True):
    """
    본문 입력 (페이지/프레임 모두 탐색, aria-hidden 제외, ProseMirror/Quill 대응)
    1) 키보드 insert_text
    2) execCommand('insertText') + input 이벤트
    3) textContent 강제 + input 이벤트
    """
    text = sanitize_html_to_text(content) if force_plain else content

    selectors = [
        '[contenteditable="true"][data-placeholder*="내용"]:not([aria-hidden="true"])',
        'div.ProseMirror:not([aria-hidden="true"])',
        '[contenteditable="true"]:not([aria-hidden="true"])',
        'div[role="textbox"]:not([aria-hidden="true"])',
        'div.ql-editor:not([aria-hidden="true"])',
        'div.CodeMirror textarea',
        'textarea[placeholder*="내용"]',
    ]

    def _try_fill(owner, sel):
        el = owner.locator(sel).first
        if el.count() == 0 or not el.is_visible():
            return False

        # 0) 뷰로 스크롤+클릭+포커스
        try:
            el.scroll_into_view_if_needed()
        except: pass
        try:
            el.click(timeout=1200)
        except: pass
        try:
            el.focus()
        except:
            try:
                el.evaluate("e => e.focus()")
            except: pass

        # 1) 키보드로 입력
        kb = (frame.page.keyboard if hasattr(frame, "page") else page.keyboard)
        kb.insert_text(text)
        time.sleep(0.2)
        try_len = el.evaluate("e => (e.innerText || e.textContent || '').trim().length")
        if try_len and try_len >= min(5, len(text)):
            # ✅ 여기 디버그 추가
            try:
                cur_len = owner.evaluate(
                    "() => Array.from(document.querySelectorAll('[contenteditable=true]')).map(e => (e.innerText||'').length)")
                debug(f"본문 길이들(키보드): {cur_len}")
            except Exception:
                pass
            info(f"본문 입력 완료(키보드): {sel}")
            return True

        # 2) execCommand + input 이벤트
        el.evaluate("""(node, txt) => {
            node.focus();
            try { document.execCommand('selectAll', false, null); } catch(e) {}
            try { document.execCommand('insertText', false, txt); } catch(e) {}
            node.dispatchEvent(new InputEvent('input', {bubbles: true}));
        }""", text)
        time.sleep(0.1)
        try_len = el.evaluate("e => (e.innerText || e.textContent || '').trim().length")
        if try_len and try_len >= min(5, len(text)):
            # ✅ 여기 디버그 추가
            try:
                cur_len = owner.evaluate(
                    "() => Array.from(document.querySelectorAll('[contenteditable=true]')).map(e => (e.innerText||'').length)")
                debug(f"본문 길이들(execCommand): {cur_len}")
            except Exception:
                pass
            info(f"본문 입력 완료(execCommand): {sel}")
            return True

        # 3) 최후: textContent 강제 + input 이벤트
        el.evaluate("""(node, txt) => {
            node.focus();
            node.textContent = txt;
            node.dispatchEvent(new InputEvent('input', {bubbles: true}));
        }""", text)
        time.sleep(0.1)
        try_len = el.evaluate("e => (e.innerText || e.textContent || '').trim().length")
        if try_len and try_len >= min(5, len(text)):
            # ✅ 여기 디버그 추가
            try:
                cur_len = owner.evaluate(
                    "() => Array.from(document.querySelectorAll('[contenteditable=true]')).map(e => (e.innerText||'').length)")
                debug(f"본문 길이들(textContent): {cur_len}")
            except Exception:
                pass
            info(f"본문 입력 완료(textContent): {sel}")
            return True

        return False

    # 페이지 → 프레임 순서로 시도
    for sel in selectors:
        if _try_fill(page, sel):
            return
    for sel in selectors:
        if _try_fill(frame, sel):
            return

    # 마지막: 가장 큰 visible contenteditable로 시도
    def _largest_visible(owner):
        cands = owner.locator('[contenteditable="true"]:not([aria-hidden="true"])')
        n = cands.count()
        best = None; area = -1
        for i in range(n):
            c = cands.nth(i)
            try:
                if not c.is_visible():
                    continue
                box = c.bounding_box()
                if not box:
                    continue
                a = box["width"] * box["height"]
                if a > area:
                    best, area = c, a
            except:
                continue
        return best

    el = _largest_visible(page) or _largest_visible(frame)
    if el:
        try:
            el.scroll_into_view_if_needed()
            el.click(timeout=800)
            el.focus()
        except: pass
        (frame.page.keyboard if hasattr(frame, "page") else page.keyboard).insert_text(text)
        info("본문 입력 완료(최대 박스)")
        return

    raise RuntimeError("본문 입력 필드를 찾지 못했습니다. (숨김/더미 제외 후 실패)")



def _debug_dump_buttons(scope, root):
    try:
        btns = root.locator("button, [role='button'], div[role='button']")
        cnt = btns.count()
        print(f"[DEBUG] {scope}: candidate buttons = {cnt}")
        for i in range(min(cnt, 20)):
            try:
                t = btns.nth(i).inner_text().strip().replace("\n", " ")
                aname = btns.nth(i).get_attribute("aria-label") or ""
                print(f"  - #{i}: text='{t}', aria-label='{aname}' visible={btns.nth(i).is_visible()}")
            except Exception:
                pass
    except Exception:
        pass

def click_register_button(page, editor_frame=None, timeout_ms=5000):
    """
    '임시등록/임시저장' 절대 금지.
    - 텍스트/aria-label가 '등록' 또는 '등록하기'와 정확 일치일 때만 클릭
    - Ctrl+Enter 같은 단축키 제출은 사용하지 않음 (임시등록으로 매핑될 수 있음)
    """
    import re

    # exact matcher
    exact_ok = re.compile(r"^\s*(등록|등록하기)\s*$")
    exact_block = re.compile(r"임시")

    def _is_ok(txt):
        if not txt:
            return False
        if exact_block.search(txt):
            return False
        return bool(exact_ok.match(txt))

    def _scan_and_click(root, scope):
        # 1) role 기반 정확 매칭
        for name in ["등록", "등록하기"]:
            try:
                el = root.get_by_role("button", name=re.compile(rf"^\s*{name}\s*$")).first
                if el.count() > 0 and el.is_visible():
                    el.scroll_into_view_if_needed()
                    el.wait_for(state="visible", timeout=timeout_ms)
                    el.click()
                    info(f"등록 버튼 클릭({scope}, role=name='{name}')")
                    return True
            except:
                pass

        # 2) 일반 버튼/role 후보
        candidates = root.locator("button, [role='button'], div[role='button']")
        for i in range(candidates.count()):
            btn = candidates.nth(i)
            try:
                if not btn.is_visible():
                    continue
                txt = (btn.inner_text() or "").strip().replace("\n"," ")
                aria = (btn.get_attribute("aria-label") or "").strip()
                if _is_ok(txt) or _is_ok(aria):
                    if exact_block.search(txt) or exact_block.search(aria):
                        continue
                    btn.scroll_into_view_if_needed()
                    btn.wait_for(state="visible", timeout=timeout_ms)
                    if not btn.is_enabled():
                        warn("등록 버튼 비활성 상태 감지(본문/필수항목 확인 필요).")
                    btn.click()
                    info(f"등록 버튼 클릭({scope}, '{txt or aria}')")
                    return True
            except:
                continue
        return False

    # 상단으로 한번 스크롤 (헤더 영역 버튼 노출)
    try:
        page.keyboard.press("Home")
        time.sleep(0.2)
    except:
        pass

    if _scan_and_click(page, "page"):
        return
    if editor_frame and _scan_and_click(editor_frame, "frame"):
        return

    # 디버깅: 후보 출력
    try:
        cand = page.locator("button, [role='button'], div[role='button']")
        print(f"[DEBUG] page buttons: {cand.count()}")
        for i in range(min(20, cand.count())):
            try:
                t = (cand.nth(i).inner_text() or "").strip().replace("\n"," ")
                a = (cand.nth(i).get_attribute("aria-label") or "").strip()
                print(f"  - #{i} text='{t}' aria='{a}'")
            except:
                pass
    except:
        pass

    raise RuntimeError("정확한 ‘등록’ 버튼을 찾지 못했습니다. (임시등록 제외)")




def upload_images(page_or_frame, image_paths: List[str]):
    if not image_paths:
        info("이미지 업로드 생략")
        return

    # 업로드 버튼 시도(페이지/프레임 어디든)
    open_btns = [
        "button:has-text('사진')", "button:has-text('이미지')",
        "button[aria-label*='이미지']", "button[title*='이미지']",
        "div[role='toolbar'] button:has-text('사진')",
    ]
    for sel in open_btns:
        btn = page_or_frame.locator(sel).first
        if btn.count() > 0:
            try:
                btn.click()
                time.sleep(0.6)
                info("이미지 업로드 모달 열기 시도")
                break
            except Exception:
                pass

    inputs = page_or_frame.locator("input[type='file']")
    if inputs.count() == 0:
        warn("file input을 찾지 못함(스킨 상이 가능)")
    for i in range(inputs.count()):
        try:
            inputs.nth(i).set_input_files(image_paths)
            info(f"이미지 파일 지정 완료: {len(image_paths)}개")
            time.sleep(1.2)
            return
        except Exception:
            pass
    warn("이미지 업로드 실패. 셀렉터 보완 필요.")

# ===== 등록/검증 =====
def detect_validation_error(page_or_frame) -> Optional[str]:
    """
    유효성 오류/필수값 누락 토스트/경고 탐지
    """
    candidates = [
        "div:has-text('필수')", "div:has-text('입력')", "div:has-text('선택')",
        "div.toast", "div.snackbar", "div[role='alert']",
    ]
    for sel in candidates:
        el = page_or_frame.locator(sel).first
        if el.count() > 0:
            try:
                txt = el.inner_text().strip()
                if txt:
                    return txt[:120]
            except Exception:
                continue
    return None

def try_submit(editor_frame):
    btn = editor_frame.locator('button:has-text("등록")').first
    if btn.count() > 0:
        btn.click()
        info("등록 버튼 클릭")
        return True
    else:
        warn("등록 버튼을 찾지 못했습니다.")
        return False


def wait_post_result(page, wait_ms=10000) -> bool:
    end = time.time() + wait_ms/1000
    while time.time() < end:
        if re.search(r"/articles/\d+($|\?)", page.url):
            info(f"업로드 성공! 글 URL: {page.url}")
            return True
        time.sleep(0.4)
    return False

# ===== 메인 =====
def post_to_naver_cafe(headless: bool = False,
                       title: str = POST_TITLE,
                       html_body: str = POST_HTML,
                       image_paths: Optional[List[str]] = None):
    image_paths = image_paths or []
    with sync_playwright() as p:
        context = create_context(p, headless=headless)
        page = context.new_page()
        try:
            page, editor = open_write_page(context, page, WRITE_URL)

            # 1) 제목/본문 입력 (말머리 선택/HTML 모드 전환 없음)
            with_retry(lambda: set_title(page, editor, title))
            time.sleep(0.8)  # 에디터 렌더 안정화
            with_retry(lambda: fill_body_in_frame(page, editor, html_body, FORCE_PLAIN_TEXT))


            # 2) 이미지가 있다면 업로드 (프레임/페이지 둘 다 시도)
            if image_paths:
                try:
                    upload_images(editor, image_paths)
                except Exception:
                    upload_images(page, image_paths)

            # 3) '임시등록'이 아닌 '등록'만 정확 클릭 → 페이지 레벨에서 처리
            click_register_button(page, editor)   # ← 단축키 제출 제거!


            # 4) 결과 확인
            if not wait_post_result(page, wait_ms=10000):
                warn(f"업로드 확인 필요. 현재 URL: {page.url}")

            info("작업 종료")

        except Exception:
            warn("업로드 중 오류 발생")
            print(traceback.format_exc())
            shot = Path("error_screenshot.png")
            try:
                page.screenshot(path=str(shot), full_page=True)
                warn(f"오류 스크린샷 저장: {shot.resolve()}")
            except Exception:
                pass
        finally:
            try:
                save_state(context)
            except Exception:
                pass
            context.close()


# if __name__ == "__main__":
#     post_to_naver_cafe(
#         headless=False,
#         title=POST_TITLE,
#         html_body=POST_HTML,
#         image_paths=IMAGE_PATHS,
#     )

def _debug_dump_title_candidates(page, frame):
    sels = [
        'input[placeholder="제목을 입력해 주세요."]',
        'input[placeholder*="제목"]',
        'textarea[placeholder*="제목"]',
        'input[name="title"]',
        'textarea[name="title"]',
        'input[type="text"]',
    ]
    for scope, obj in [("page", page), ("frame", frame)]:
        for s in sels:
            try:
                c = obj.locator(s).count()
                debug(f"[{scope}] {s} -> {c}")
            except Exception:
                pass
