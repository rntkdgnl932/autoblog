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
# =====
# =============================================================================
# Gemini 호출 래퍼 (문자열 반환) - STOP인데 parts 없음 대응 + JSON 저온 재프롬프트 1회
# =============================================================================
import time
import random
import json
import google.generativeai as genai
import google.api_core.exceptions as gax
from google.generativeai.types import RequestOptions

def _is_retryable_exception(exc: Exception) -> bool:
    retryable_types = (
        getattr(gax, "DeadlineExceeded", tuple()),
        getattr(gax, "ServiceUnavailable", tuple()),
        getattr(gax, "ResourceExhausted", tuple()),  # 429
        getattr(gax, "InternalServerError", tuple()),
    )
    if isinstance(exc, retryable_types):
        return True
    msg = str(exc).lower()
    retry_keywords = [
        "deadline exceeded", "service unavailable", "temporarily unavailable",
        "connection reset", "connection aborted", "timed out", "timeout",
        "rate limit", "429", "unavailable", "try again"
    ]
    return any(k in msg for k in retry_keywords)

def _backoff(attempt: int, base: float = 1.0, cap: float = 20.0) -> float:
    wait = min(cap, base * (2 ** attempt))
    wait *= (0.5 + random.random())  # 0.5~1.5 지터
    return wait


# extractor.py (혹은 기존 파일 내부)
from typing import Any, Optional
from .types import RespOut  # 위 RespOut 경로에 맞게 수정

def _extract_text_from_parts(resp: Any) -> RespOut:
    """
    Gemini SDK 응답에서 텍스트/메타 정보를 '안전하게' 추출합니다.
    - response.text 에는 접근하지 않습니다 (SDK에 따라 ValueError 발생).
    - candidates[0].content.parts 를 신뢰해서 문자열을 모읍니다.
    - SAFETY 차단 여부, finish_reason, block_reason, safety_ratings, parts 존재 여부를 함께 반환합니다.
    """
    out: RespOut = {
        "text": None,
        "blocked": False,
        "finish_reason": None,
        "block_reason": None,
        "safety_ratings": None,
        "has_parts": False,
    }

    try:
        # prompt_feedback에서 차단 사유(있다면) 추출
        prompt_feedback = getattr(resp, "prompt_feedback", None)
        if prompt_feedback is not None:
            # SDK 버전에 따라 속성명이 다를 수 있어 둘 다 시도
            out["block_reason"] = (
                getattr(prompt_feedback, "block_reason", None)
                or getattr(prompt_feedback, "block_reason_message", None)
            )

        candidates = getattr(resp, "candidates", []) or []
        if not candidates:
            return out

        c0 = candidates[0]

        # finish_reason (enum or int → str로 정규화)
        finish_reason = getattr(c0, "finish_reason", None)
        out["finish_reason"] = getattr(finish_reason, "name", None) or str(finish_reason) if finish_reason is not None else None

        # SAFETY 차단 여부
        if out["finish_reason"] and str(out["finish_reason"]).upper() == "SAFETY":
            out["blocked"] = True

        # safety_ratings 그대로 보관 (타입 Any)
        out["safety_ratings"] = getattr(c0, "safety_ratings", None)

        # 본문 parts에서 텍스트 조립
        content = getattr(c0, "content", None)
        parts = getattr(content, "parts", None) if content is not None else None
        if parts:
            out["has_parts"] = True
            pieces: list[str] = []
            for p in parts:
                t = getattr(p, "text", None)
                if isinstance(t, str) and t:   # ← 타입 체커 OK
                    pieces.append(t)
            if pieces:
                joined = "".join(pieces).strip()
                if joined:
                    out["text"] = joined

        return out

    except Exception as exc:
        # 파싱 중 예외는 로깅만 하고, out 기본값 반환
        print(f"⚠️ 응답 파싱 오류(파트 추출): {type(exc).__name__}: {exc}")
        return out


def _low_temp_json_reprompt(model_name: str, base_prompt: str, request_options: RequestOptions) -> str | None:
    """
    is_json=True인데 parts가 비었을 때, 저온·단호한 형식 지시로 1회 재프롬프트.
    """
    try:
        model = genai.GenerativeModel(model_name)
        strict_prompt = (
            "You must return ONLY valid JSON.\n"
            "Do NOT include any explanations, code fences, or markdown.\n"
            "Return a JSON array or object as requested.\n\n"
            f"{base_prompt}"
        )
        resp = model.generate_content(
            [{"role": "user", "parts": [{"text": strict_prompt}]}],
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                response_mime_type="application/json",
                candidate_count=1,
            ),
            request_options=request_options,
        )
        ex = _extract_text_from_parts(resp)
        print(f"   └─ 저온 재프롬프트 결과: finish_reason={ex['finish_reason']} | has_parts={ex['has_parts']}")
        if ex["blocked"]:
            print("   └─ 저온 재프롬프트도 SAFETY 차단")
            return None
        return ex["text"] if ex["text"] else None
    except Exception as exc:
        print(f"   └─ 저온 재프롬프트 예외: {type(exc).__name__}: {exc}")
        return None

def call_gemini(prompt, temperature=0.6, is_json=False, max_retries=5):
    """
    반환:
      - 성공: str(response_text)
      - SAFETY 차단: "SAFETY_BLOCKED"
      - 실패: "API_ERROR"
    """
    model_name = "gemini-2.5-pro"
    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
    }
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        response_mime_type="application/json" if is_json else "text/plain",
        candidate_count=1,
        # 필요시 최대 토큰 제한:
        # max_output_tokens=1024,
        # top_p=0.9,
    )
    request_options = RequestOptions(timeout=300)

    for attempt in range(max_retries):
        try:
            print(f"▶ [Gemini] 시도 {attempt+1}/{max_retries} | model={model_name} | json={is_json} | temp={temperature}")

            model = genai.GenerativeModel(model_name)
            resp = model.generate_content(
                [{"role": "user", "parts": [{"text": prompt}]}],  # 권장 포맷
                generation_config=generation_config,
                safety_settings=safety_settings,
                request_options=request_options,
            )

            ex = _extract_text_from_parts(resp)
            print(f"   ├─ finish_reason={ex['finish_reason']} | blocked={ex['blocked']} | has_parts={ex['has_parts']}")

            if ex["blocked"]:
                print(f"   ├─ SAFETY 차단(block_reason={ex['block_reason']}) → 중단")
                return "SAFETY_BLOCKED"

            # 정상 텍스트
            if ex["text"]:
                print(f"✅ 응답 수신 (길이={len(ex['text'])})")
                return ex["text"]

            # parts 없음/빈 텍스트인데 finish_reason=STOP → JSON 모드일 경우 저온 재프롬프트 1회
            if is_json:
                print("⚠️ 후보는 있으나 텍스트가 비어 있음 → 저온 재프롬프트 시도(1회)")
                fixed = _low_temp_json_reprompt(model_name, prompt, request_options)
                if fixed and fixed.strip():
                    print(f"✅ 저온 재프롬프트 성공 (길이={len(fixed)})")
                    return fixed
                else:
                    print("   └─ 저온 재프롬프트 실패 → 재시도 루프로 이동")
            else:
                print("⚠️ 후보는 있으나 텍스트가 비어 있음 → 재시도 대상")

        except Exception as exc:
            et = type(exc).__name__
            print(f"❌ 예외 발생 [{et}]: {exc}")
            if not _is_retryable_exception(exc):
                print("🚫 재시도 비대상 오류 → 즉시 실패")
                return "API_ERROR"

        # 재시도 대기
        wait = _backoff(attempt)
        print(f"⏳ {wait:.1f}초 대기 후 재시도")
        time.sleep(wait)

    print("❌ 최대 재시도 횟수 초과 → 실패 처리")
    return "API_ERROR"





