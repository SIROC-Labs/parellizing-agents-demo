from pydantic import BaseModel

from app.models.voice import VoiceGender


class VoiceRead(BaseModel):
    id: str
    name: str
    provider: str
    locale: str
    gender: VoiceGender
    style: str
    supports_sts: bool
    supports_tts: bool
