from app.models.voice import Voice
from app.repositories.voice_repository import VoiceRepository


class VoiceService:
    def __init__(self, repo: VoiceRepository) -> None:
        self._repo = repo

    def list(self) -> list[Voice]:
        return self._repo.list()
