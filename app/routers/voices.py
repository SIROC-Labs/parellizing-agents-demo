from fastapi import APIRouter, Depends, Query

from app.dependencies import get_voice_service
from app.models.voice import VoiceGender
from app.schemas.voice import VoiceRead
from app.services.voice_service import VoiceService

router = APIRouter(prefix="/voices", tags=["voices"])


@router.get("", response_model=list[VoiceRead])
def list_voices(
    locale: str | None = Query(default=None),
    gender: VoiceGender | None = Query(default=None),
    style: str | None = Query(default=None),
    supports_sts: bool | None = Query(default=None),
    supports_tts: bool | None = Query(default=None),
    service: VoiceService = Depends(get_voice_service),
):
    return service.list_filtered(
        locale=locale,
        gender=gender,
        style=style,
        supports_sts=supports_sts,
        supports_tts=supports_tts,
    )
