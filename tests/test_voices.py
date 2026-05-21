def test_list_voices_returns_seeded_voices(client):
    response = client.get("/voices")
    assert response.status_code == 200
    voices = response.json()
    assert len(voices) > 0


def test_voice_has_expected_fields(client):
    voices = client.get("/voices").json()
    voice = voices[0]
    assert "id" in voice
    assert "name" in voice
    assert "provider" in voice
    assert "locale" in voice
    assert "supports_sts" in voice
    assert "supports_tts" in voice
    assert "gender" in voice
    assert "style" in voice


def test_seeded_voices_include_known_entries(client):
    voices = client.get("/voices").json()
    names = {v["name"] for v in voices}
    assert "Aria" in names
    assert "Marco" in names


def test_seeded_voices_have_gender_and_style(client):
    voices = client.get("/voices").json()
    for v in voices:
        assert v["gender"] in ("male", "female", "neutral")
        assert isinstance(v["style"], str) and len(v["style"]) > 0


def test_filter_by_gender(client):
    voices = client.get("/voices", params={"gender": "female"}).json()
    assert all(v["gender"] == "female" for v in voices)
    assert len(voices) > 0


def test_filter_by_locale(client):
    voices = client.get("/voices", params={"locale": "en-US"}).json()
    assert all(v["locale"] == "en-US" for v in voices)
    assert len(voices) > 0


def test_filter_by_style(client):
    voices = client.get("/voices", params={"style": "conversational"}).json()
    assert all(v["style"] == "conversational" for v in voices)
    assert len(voices) > 0


def test_filter_by_supports_sts(client):
    voices = client.get("/voices", params={"supports_sts": "true"}).json()
    assert all(v["supports_sts"] is True for v in voices)


def test_filter_by_supports_tts(client):
    voices = client.get("/voices", params={"supports_tts": "true"}).json()
    assert all(v["supports_tts"] is True for v in voices)


def test_combined_filters(client):
    voices = client.get("/voices", params={"gender": "male", "style": "conversational"}).json()
    assert all(v["gender"] == "male" and v["style"] == "conversational" for v in voices)


def test_filter_no_matches_returns_empty_list(client):
    voices = client.get("/voices", params={"locale": "xx-XX"}).json()
    assert voices == []


def test_filter_gender_no_matches_returns_empty_list(client):
    voices = client.get("/voices", params={"gender": "neutral"}).json()
    assert voices == []
