import uuid
from datetime import datetime, timezone

from app.models.campaign import Campaign, CampaignStatus
from app.repositories.campaign_repository import CampaignRepository
from app.schemas.campaign import CampaignCreate
from app.services.errors import NotFound


class CampaignService:
    def __init__(self, repo: CampaignRepository) -> None:
        self._repo = repo

    def create(self, data: CampaignCreate) -> Campaign:
        campaign = Campaign(
            id=str(uuid.uuid4()),
            name=data.name,
            client_name=data.client_name,
            status=CampaignStatus.DRAFT,
            created_at=datetime.now(timezone.utc),
        )
        return self._repo.add(campaign)

    def get(self, campaign_id: str) -> Campaign:
        campaign = self._repo.get(campaign_id)
        if campaign is None:
            raise NotFound(f"Campaign {campaign_id} not found")
        return campaign

    def list(self) -> list[Campaign]:
        return self._repo.list()
