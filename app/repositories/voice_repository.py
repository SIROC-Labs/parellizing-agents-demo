from app.models.voice import Voice


class VoiceRepository:
    def __init__(self) -> None:
        self._items: dict[str, Voice] = {}

    def add(self, voice: Voice) -> Voice:
        self._items[voice.id] = voice
        return voice

    def get(self, voice_id: str) -> Voice | None:
        return self._items.get(voice_id)

    def list(self) -> list[Voice]:
        return list(self._items.values())
