from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_campaign_service
from app.schemas.campaign import CampaignCreate, CampaignRead, CampaignTransition
from app.services.campaign_service import CampaignService
from app.services.errors import InvalidTransition, NotFound

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


@router.patch("/{campaign_id}/status", response_model=CampaignRead)
def transition_campaign(
    campaign_id: str,
    payload: CampaignTransition,
    service: CampaignService = Depends(get_campaign_service),
):
    try:
        return service.transition(campaign_id, payload)
    except NotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidTransition as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
