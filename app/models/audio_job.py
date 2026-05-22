from datetime import datetime
from enum import Enum
from typing import Optional

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
    output_url: Optional[str] = None
    actual_duration_seconds: Optional[int] = None
    error_message: Optional[str] = None
