from fastapi import APIRouter, Depends, status

from app.dependencies import get_audio_job_service
from app.schemas.audio_job import AudioJobCreate, AudioJobRead
from app.services.audio_job_service import AudioJobService

router = APIRouter(prefix="/audio-jobs", tags=["audio-jobs"])


@router.post("", response_model=AudioJobRead, status_code=status.HTTP_201_CREATED)
def create_audio_job(payload: AudioJobCreate, service: AudioJobService = Depends(get_audio_job_service)):
    return service.create(payload)


@router.get("/{job_id}", response_model=AudioJobRead)
def get_audio_job(job_id: str, service: AudioJobService = Depends(get_audio_job_service)):
    return service.get(job_id)
