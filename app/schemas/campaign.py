from datetime import datetime

from pydantic import BaseModel

from app.models.campaign import CampaignStatus


class CampaignCreate(BaseModel):
    name: str
    client_name: str


class CampaignTransition(BaseModel):
    status: CampaignStatus


class CampaignRead(BaseModel):
    id: str
    name: str
    client_name: str
    status: CampaignStatus
    created_at: datetime
