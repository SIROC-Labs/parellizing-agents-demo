from datetime import datetime

from pydantic import BaseModel

from app.models.audio_job import AudioJobStatus


class AudioJobCreate(BaseModel):
    campaign_id: str
    script_text: str
    voice_id: str
    target_duration_seconds: int


class AudioJobRead(BaseModel):
    id: str
    campaign_id: str
    script_text: str
    voice_id: str
    target_duration_seconds: int
    status: AudioJobStatus
    created_at: datetime
