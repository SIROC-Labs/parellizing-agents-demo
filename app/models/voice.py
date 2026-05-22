from typing import Literal

from pydantic import BaseModel

VoiceGender = Literal["male", "female", "neutral"]


class Voice(BaseModel):
    id: str
    name: str
    provider: str
    locale: str
    gender: VoiceGender
    style: str
    supports_sts: bool
    supports_tts: bool
