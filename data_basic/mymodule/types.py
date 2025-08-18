# types.py 등 공용 타입 정의 위치에 두세요
from typing import Any, Optional, TypedDict

class RespOut(TypedDict):
    text: Optional[str]
    blocked: bool
    finish_reason: Optional[str]
    block_reason: Optional[str]
    safety_ratings: Any
    has_parts: bool
