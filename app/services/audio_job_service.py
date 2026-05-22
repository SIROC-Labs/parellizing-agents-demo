import uuid
from datetime import datetime, timezone

from app.models.audio_job import AudioJob, AudioJobStatus
from app.repositories.audio_job_repository import AudioJobRepository
from app.repositories.campaign_repository import CampaignRepository
from app.repositories.voice_repository import VoiceRepository
from app.schemas.audio_job import AudioJobCreate, AudioJobUpdate
from app.services.errors import InvalidOperation, NotFound


class AudioJobService:
    def __init__(
        self,
        repo: AudioJobRepository,
        campaign_repo: CampaignRepository,
        voice_repo: VoiceRepository,
    ) -> None:
        self._repo = repo
        self._campaign_repo = campaign_repo
        self._voice_repo = voice_repo

    def create(self, data: AudioJobCreate) -> AudioJob:
        if self._campaign_repo.get(data.campaign_id) is None:
            raise NotFound(f"Campaign {data.campaign_id} not found")
        if self._voice_repo.get(data.voice_id) is None:
            raise NotFound(f"Voice {data.voice_id} not found")

        job = AudioJob(
            id=str(uuid.uuid4()),
            campaign_id=data.campaign_id,
            script_text=data.script_text,
            voice_id=data.voice_id,
            target_duration_seconds=data.target_duration_seconds,
            status=AudioJobStatus.QUEUED,
            created_at=datetime.now(timezone.utc),
        )
        return self._repo.add(job)

    def get(self, job_id: str) -> AudioJob:
        job = self._repo.get(job_id)
        if job is None:
            raise NotFound(f"AudioJob {job_id} not found")
        return job

    def update(self, job_id: str, data: AudioJobUpdate) -> AudioJob:
        job = self.get(job_id)

        terminal = {AudioJobStatus.COMPLETED, AudioJobStatus.FAILED}
        if job.status in terminal:
            raise InvalidOperation(f"AudioJob {job_id} is already in a terminal state ({job.status})")

        if data.status == AudioJobStatus.COMPLETED:
            if not data.output_url or data.actual_duration_seconds is None:
                raise InvalidOperation("Completing a job requires output_url and actual_duration_seconds")
        elif data.status == AudioJobStatus.FAILED:
            if not data.error_message:
                raise InvalidOperation("Failing a job requires error_message")

        updated = job.model_copy(update={
            "status": data.status,
            "output_url": data.output_url,
            "actual_duration_seconds": data.actual_duration_seconds,
            "error_message": data.error_message,
        })
        return self._repo.update(updated)
