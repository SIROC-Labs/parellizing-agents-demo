import uuid
from datetime import datetime, timezone

from app.models.campaign import Campaign, CampaignStatus
from app.repositories.campaign_repository import CampaignRepository
from app.schemas.campaign import CampaignCreate, CampaignTransition
from app.services.errors import InvalidTransition, NotFound


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

    def transition(self, campaign_id: str, data: CampaignTransition) -> Campaign:
        campaign = self.get(campaign_id)
        allowed: dict[CampaignStatus, set[CampaignStatus]] = {
            CampaignStatus.DRAFT: {CampaignStatus.ACTIVE},
            CampaignStatus.ACTIVE: {CampaignStatus.PAUSED, CampaignStatus.COMPLETED},
            CampaignStatus.PAUSED: {CampaignStatus.ACTIVE, CampaignStatus.COMPLETED},
            CampaignStatus.COMPLETED: set(),
        }
        valid = allowed[campaign.status]
        if data.status not in valid:
            names = ", ".join(s.value for s in valid) if valid else "none"
            raise InvalidTransition(
                f"Cannot transition from '{campaign.status.value}' to '{data.status.value}'. "
                f"Allowed transitions from '{campaign.status.value}': {names}."
            )
        updated = campaign.model_copy(update={"status": data.status})
        return self._repo.update(updated)

    def list(self) -> list[Campaign]:
        return self._repo.list()
