from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class Campaign(BaseModel):
    id: str
    name: str
    client_name: str
    status: CampaignStatus
    created_at: datetime
