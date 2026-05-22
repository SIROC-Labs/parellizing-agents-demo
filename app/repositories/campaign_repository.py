from app.models.campaign import Campaign


class CampaignRepository:
    def __init__(self) -> None:
        self._items: dict[str, Campaign] = {}

    def add(self, campaign: Campaign) -> Campaign:
        self._items[campaign.id] = campaign
        return campaign

    def get(self, campaign_id: str) -> Campaign | None:
        return self._items.get(campaign_id)

    def update(self, campaign: Campaign) -> Campaign:
        self._items[campaign.id] = campaign
        return campaign

    def list(self) -> list[Campaign]:
        return list(self._items.values())
