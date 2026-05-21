from app.models.voice import Voice


class VoiceRepository:
    def __init__(self) -> None:
        self._items: dict[str, Voice] = {}

    def add(self, voice: Voice) -> Voice:
        self._items[voice.id] = voice
        return voice

    def get(self, voice_id: str) -> Voice | None:
        return self._items.get(voice_id)

    def list(
        self,
        *,
        locale: str | None = None,
        gender: str | None = None,
        style: str | None = None,
        supports_sts: bool | None = None,
        supports_tts: bool | None = None,
    ) -> list[Voice]:
        results = self._items.values()
        if locale is not None:
            results = (v for v in results if v.locale == locale)
        if gender is not None:
            results = (v for v in results if v.gender == gender)
        if style is not None:
            results = (v for v in results if v.style == style)
        if supports_sts is not None:
            results = (v for v in results if v.supports_sts == supports_sts)
        if supports_tts is not None:
            results = (v for v in results if v.supports_tts == supports_tts)
        return list(results)
