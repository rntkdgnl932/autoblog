from PyQt5.QtTest import QTest
import google.generativeai as genai
import os


# 사용자 정의 변수 모듈 (유동적으로 변경되는 부분)
import variable as v_

# --- 설정 로드 ---
dir_path = "C:\\my_games\\" + str(v_.game_folder)
file_path_one = dir_path + "\\mysettings\\idpw\\onecla.txt"
if os.path.isfile(file_path_one):
    with open(file_path_one, "r", encoding='utf-8-sig') as file:
        lines_one = file.read().split('\n')
        v_.wd_id = lines_one[0]
        v_.wd_pw = lines_one[1]
        v_.domain_adress = lines_one[2]
        if len(lines_one) > 3:
            # variable.py 또는 텍스트 파일에 Gemini API 키를 저장했다고 가정
            v_.gemini_api_key = lines_one[3]
        if len(lines_one) > 4:
            v_.my_category = lines_one[4]
else:
    print('one 파일 없당')

# --- 클라이언트 설정 ---
# ✅ Gemini API + WordPress 클라이언트 설정
try:
    genai.configure(api_key=v_.my_gas_key)
except Exception as e:
    print(f"❌ Gemini API 키 설정 실패: {e}")



# ==============================================================================
# Gemini API 호출 래퍼 함수 (안전 설정 포함)
# ==============================================================================
def call_gemini(prompt, temperature=0.6, is_json=False, max_retries=3):
    import time  # time.sleep()을 위해 상단에 추가해야 합니다.
    from google.generativeai.types import RequestOptions
    """
    API 호출 실패 시 원인을 파악하여 '통신 오류'에 대해서만 자동 재시도합니다.
    """
    for attempt in range(max_retries):
        QTest.qWait(100)
        try:
            model = genai.GenerativeModel('gemini-2.5-pro')
            safety_settings = {
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE", "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE", "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
            generation_config = genai.types.GenerationConfig(
                temperature=temperature, response_mime_type="application/json" if is_json else "text/plain"
            )

            # ✅ 2. 일반 dict 대신, import한 RequestOptions 객체를 사용합니다.
            request_options = RequestOptions(timeout=300)

            response = model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings,
                request_options=request_options  # 수정된 객체 전달
            )

            if response.parts:
                return response.text

            elif response.candidates and response.candidates[0].finish_reason.name == "SAFETY":
                print("⚠️ API 응답이 안전 필터에 의해 차단되었습니다. (재시도 안 함)")
                return "SAFETY_BLOCKED"

            else:
                print(f"⚠️ API가 알 수 없는 이유로 빈 응답을 반환했습니다. ({attempt + 1}/{max_retries}차 시도)")
                time.sleep(5 * (attempt + 1))
                continue

        except Exception as e:
            print(f"❌ Gemini API 통신 중 예외 발생: {e} ({attempt + 1}/{max_retries}차 시도)")
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))
            continue

    print("❌ 최대 재시도 횟수를 초과했습니다. 최종 실패 처리합니다.")
    return "API_ERROR"


# uploader.py 또는 blog_function.py

# blog_function.py

import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import pyperclip

# blog_function.py

# inputimeout 관련 import는 이제 필요 없으므로 삭제하거나 주석 처리합니다.
# from inputimeout import inputimeout, TimeoutOccurred
import threading  # 파이썬 기본 내장 라이브러리


# blog_function.py

# ... (기존 import 구문들은 동일) ...

# blog_function.py

# blog_function.py
# blog_function.py
# blog_function.py 에 포함될 함수

import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# blog_function.py

import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import threading


def check_cafe_access(club_id, menu_id):
    """
    1차: 프로필 자동 로그인을 시도.
    2차: 실패 시 나타나는 로그인 창에서 5분간 수동 로그인을 대기합니다.
    """
    chrome_options = Options()
    user_data_path = r"C:\Chrome-Bot-Profile"
    chrome_options.add_argument(f"user-data-dir={user_data_path}")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    print("▶ 1단계: 로그인 및 카페 글쓰기 페이지 접근 테스트 시작...")

    # 우리가 최종적으로 확인한, 실제 글쓰기 에디터 페이지 URL
    write_url = f"https://cafe.naver.com/ca-fe/cafes/{club_id}/menus/{menu_id}/articles/write"

    try:
        driver.get(write_url)
        time.sleep(3)  # 페이지가 완전히 그려질 시간을 물리적으로 대기

        # 로그인 페이지가 나타나는지 먼저 확인
        if "nid.naver.com/nidlogin.login" in driver.current_url:
            # 로그인 페이지가 나타났으므로 수동 로그인 절차 진행
            print("⚠️ 프로필 자동 로그인이 실패하여 수동 로그인을 시작합니다.")
            print("   로그인 페이지가 감지되었습니다. 5분 내에 로그인을 완료해주세요.")

            user_input = None

            def get_user_input():
                nonlocal user_input
                user_input = input("   로그인 완료 후 여기서 Enter를 누르세요: ")

            input_thread = threading.Thread(target=get_user_input)
            input_thread.daemon = True
            input_thread.start()
            input_thread.join(timeout=300)  # 5분(300초) 동안 스레드 완료를 기다림

            if input_thread.is_alive():
                print("\n❌ 5분 시간 초과! 업로드를 중단합니다.")
                driver.quit()
                return None, None

            # 수동 로그인 후, 글쓰기 페이지로 다시 이동
            print("▶ 입력을 확인하고 글쓰기 페이지로 재이동합니다.")
            driver.get(write_url)
            time.sleep(3)

        # 글쓰기 페이지의 핵심인 'cafe_main' 프레임이 나타나는지만 확인
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'cafe_main')))
        driver.switch_to.default_content()  # 확인 후, 원래 프레임으로 복귀

        print("✅ 1단계 성공: 글쓰기 페이지 접근 확인. 브라우저를 유지합니다.")
        return driver, wait  # 성공 시 driver와 wait 객체 반환

    except Exception as e:
        print(f"❌ 1단계 실패: 페이지 접근 중 알 수 없는 오류 발생. 원인: {e}")
        driver.save_screenshot('error_screenshot_check_access.png')
        driver.quit()  # 실패 시 브라우저 종료
        return None, None


# blog_function.py

import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pyperclip


def upload_to_naver_cafe(club_id, menu_id, subject, html_content):
    """
    중첩된 iframe을 포함한 모든 iframe을 탐색하여 글쓰기 에디터를 찾아 업로드합니다.
    (최종 지능형 버전)
    """
    chrome_options = Options()
    user_data_path = r"C:\Chrome-Bot-Profile"
    chrome_options.add_argument(f"user-data-dir={user_data_path}")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)
    print("▶ 최종 업로드 프로세스를 시작합니다...")

    try:
        # 1. 글쓰기 페이지로 직접 이동
        write_url = f"https://cafe.naver.com/ca-fe/cafes/{club_id}/menus/{menu_id}/articles/write"
        driver.get(write_url)
        print("DEBUG: 글쓰기 페이지로 이동했습니다. 에디터 탐색을 시작합니다...")
        time.sleep(5)  # 페이지의 모든 스크립트가 로드될 때까지 충분히 대기

        # 2. '제목 입력창'이 있는 올바른 iframe 찾기
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        if not iframes:
            raise Exception("페이지에서 어떤 iframe도 찾을 수 없습니다.")

        print(f"DEBUG: {len(iframes)}개의 iframe을 발견. 순차적으로 탐색합니다.")

        found_editor = False
        for index, iframe in enumerate(iframes):
            try:
                driver.switch_to.frame(iframe)
                # 이 iframe 안에 'subject'라는 이름의 제목 입력창이 있는지 확인
                wait.until(EC.presence_of_element_located((By.NAME, 'subject')))

                # 찾았다면, 이곳이 우리가 작업할 올바른 iframe임
                print(f"✅ DEBUG: {index + 1}번째 iframe에서 글쓰기 에디터를 찾았습니다!")
                found_editor = True
                break  # 올바른 iframe을 찾았으니 반복문 종료
            except:
                # 못 찾았다면, 다시 원래 페이지로 복귀하여 다음 iframe 탐색 준비
                driver.switch_to.default_content()

        if not found_editor:
            raise Exception("모든 iframe을 탐색했지만 '제목 입력창'을 찾지 못했습니다.")

        # 3. 제목 입력 (이제 driver는 올바른 iframe 안에 있습니다)
        driver.find_element(By.NAME, 'subject').send_keys(subject)

        # 4. HTML 모드 전환 및 본문 붙여넣기
        driver.find_element(By.CLASS_NAME, 'se-e-tool-button-html').click()
        html_textarea = driver.find_element(By.TAG_NAME, 'textarea')

        pyperclip.copy(html_content)
        html_textarea.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 5. 최종 등록
        # 등록 버튼은 iframe 밖에 있으므로, 다시 원래 페이지로 복귀해야 함
        driver.switch_to.default_content()
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.BaseButton.btn-txt.btn-submit')))
        submit_button.click()

        print("✅ 네이버 카페 게시글 자동 업로드 성공!")
        time.sleep(5)
        return True

    except Exception as e:
        print(f"❌ 업로드 중 에러 발생: {e}")
        print(traceback.format_exc())
        driver.save_screenshot('final_error_screenshot.png')
        return False
    finally:
        driver.quit()

def post_the_article(driver, wait, subject, html_content):
    """
    게시판 페이지에서 '글쓰기' 버튼을 누르고 실제 글을 포스팅합니다.
    """
    print("▶ 3단계: 실제 콘텐츠 업로드 시작...")
    try:
        # 1. '글쓰기' 버튼을 누르기 위해 다시 메인 프레임으로 전환
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'cafe_main')))

        # 2. '글쓰기' 버튼 클릭
        # '글쓰기' 버튼의 ID는 보통 'writeFormBtn' 입니다.
        write_button = wait.until(EC.element_to_be_clickable((By.ID, "writeFormBtn")))
        write_button.click()

        print("DEBUG: '글쓰기' 버튼 클릭 성공. 에디터 로딩 대기...")
        time.sleep(3)

        # 3. 글쓰기 에디터 프레임으로 다시 전환
        # 글쓰기 버튼을 누르면 새로운 프레임이 로드될 수 있습니다.
        # 기존 프레임에서 빠져나왔다가 다시 들어가는 것이 안정적입니다.
        driver.switch_to.default_content()
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'cafe_main')))

        # 4. 제목 입력 및 포스팅 (이전 코드와 동일)
        wait.until(EC.visibility_of_element_located((By.NAME, 'subject'))).send_keys(subject)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-e-tool-button-html'))).click()
        html_textarea = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'textarea')))
        pyperclip.copy(html_content)
        html_textarea.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.BaseButton.btn-txt.btn-submit')))
        submit_button.click()

        print("✅ 3단계 성공: 네이버 카페 게시글 자동 업로드 완료!")
        time.sleep(5)
        return True

    except Exception as e:
        print(f"❌ 3단계 실패: 업로드 중 에러 발생: {e}")
        print(traceback.format_exc())
        driver.save_screenshot('error_screenshot_posting.png')
        return False
    finally:
        driver.quit()

