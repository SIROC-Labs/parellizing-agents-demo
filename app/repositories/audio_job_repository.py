from app.models.audio_job import AudioJob


class AudioJobRepository:
    def __init__(self) -> None:
        self._items: dict[str, AudioJob] = {}

    def add(self, job: AudioJob) -> AudioJob:
        self._items[job.id] = job
        return job

    def get(self, job_id: str) -> AudioJob | None:
        return self._items.get(job_id)

    def update(self, job: AudioJob) -> AudioJob:
        self._items[job.id] = job
        return job

    def list(self) -> list[AudioJob]:
        return list(self._items.values())
