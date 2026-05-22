import uuid
from datetime import datetime, timezone

from app.models.campaign import Campaign, CampaignStatus
from app.repositories.campaign_repository import CampaignRepository
from app.schemas.campaign import CampaignCreate
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

    def transition_status(self, campaign_id: str, new_status: CampaignStatus) -> Campaign:
        campaign = self.get(campaign_id)
        allowed: dict[CampaignStatus, set[CampaignStatus]] = {
            CampaignStatus.DRAFT: {CampaignStatus.ACTIVE},
            CampaignStatus.ACTIVE: {CampaignStatus.PAUSED, CampaignStatus.COMPLETED},
            CampaignStatus.PAUSED: {CampaignStatus.ACTIVE, CampaignStatus.COMPLETED},
            CampaignStatus.COMPLETED: set(),
        }
        if new_status not in allowed[campaign.status]:
            allowed_values = ", ".join(s.value for s in allowed[campaign.status]) or "none"
            raise InvalidTransition(
                f"Cannot transition from '{campaign.status.value}' to '{new_status.value}'. "
                f"Allowed transitions from '{campaign.status.value}': {allowed_values}."
            )
        updated = campaign.model_copy(update={"status": new_status})
        return self._repo.update(updated)

    def list(self) -> list[Campaign]:
        return self._repo.list()
