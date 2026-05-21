from pydantic import BaseModel


class VoiceRead(BaseModel):
    id: str
    name: str
    provider: str
    locale: str
    supports_sts: bool
    supports_tts: bool
