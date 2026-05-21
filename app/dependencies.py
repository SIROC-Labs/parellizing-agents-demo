from app.repositories.audio_job_repository import AudioJobRepository
from app.repositories.campaign_repository import CampaignRepository
from app.repositories.voice_repository import VoiceRepository
from app.services.audio_job_service import AudioJobService
from app.services.campaign_service import CampaignService
from app.services.voice_service import VoiceService

campaign_repo = CampaignRepository()
voice_repo = VoiceRepository()
audio_job_repo = AudioJobRepository()


def get_campaign_service() -> CampaignService:
    return CampaignService(campaign_repo)


def get_voice_service() -> VoiceService:
    return VoiceService(voice_repo)


def get_audio_job_service() -> AudioJobService:
    return AudioJobService(audio_job_repo, campaign_repo, voice_repo)
