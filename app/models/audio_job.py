from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class AudioJobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AudioJob(BaseModel):
    id: str
    campaign_id: str
    script_text: str
    voice_id: str
    target_duration_seconds: int
    status: AudioJobStatus
    created_at: datetime
