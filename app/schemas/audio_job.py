from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.audio_job import AudioJobStatus


class AudioJobCreate(BaseModel):
    campaign_id: str
    script_text: str
    voice_id: str
    target_duration_seconds: int


class AudioJobUpdate(BaseModel):
    status: AudioJobStatus
    output_url: Optional[str] = None
    actual_duration_seconds: Optional[int] = None
    error_message: Optional[str] = None


class AudioJobRead(BaseModel):
    id: str
    campaign_id: str
    script_text: str
    voice_id: str
    target_duration_seconds: int
    status: AudioJobStatus
    created_at: datetime
    output_url: Optional[str] = None
    actual_duration_seconds: Optional[int] = None
    error_message: Optional[str] = None
