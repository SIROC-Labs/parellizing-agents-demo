from fastapi import APIRouter, Depends

from app.dependencies import get_voice_service
from app.schemas.voice import VoiceRead
from app.services.voice_service import VoiceService

router = APIRouter(prefix="/voices", tags=["voices"])


@router.get("", response_model=list[VoiceRead])
def list_voices(service: VoiceService = Depends(get_voice_service)):
    return service.list()
