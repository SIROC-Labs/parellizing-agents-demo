from fastapi import APIRouter, Depends, status

from app.dependencies import get_campaign_service
from app.schemas.campaign import CampaignCreate, CampaignRead
from app.services.campaign_service import CampaignService

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("", response_model=list[CampaignRead])
def list_campaigns(service: CampaignService = Depends(get_campaign_service)):
    return service.list()


@router.post("", response_model=CampaignRead, status_code=status.HTTP_201_CREATED)
def create_campaign(payload: CampaignCreate, service: CampaignService = Depends(get_campaign_service)):
    return service.create(payload)


@router.get("/{campaign_id}", response_model=CampaignRead)
def get_campaign(campaign_id: str, service: CampaignService = Depends(get_campaign_service)):
    return service.get(campaign_id)
