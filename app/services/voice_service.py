from app.models.voice import Voice, VoiceGender
from app.repositories.voice_repository import VoiceRepository


class VoiceService:
    def __init__(self, repo: VoiceRepository) -> None:
        self._repo = repo

    def list(self) -> list[Voice]:
        return self._repo.list()

    def list_filtered(
        self,
        *,
        locale: str | None = None,
        gender: VoiceGender | None = None,
        style: str | None = None,
        supports_sts: bool | None = None,
        supports_tts: bool | None = None,
    ) -> list[Voice]:
        return self._repo.list_filtered(
            locale=locale,
            gender=gender,
            style=style,
            supports_sts=supports_sts,
            supports_tts=supports_tts,
        )
