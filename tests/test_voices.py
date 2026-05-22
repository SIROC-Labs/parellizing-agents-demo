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


def test_seeded_voices_include_known_entries(client):
    voices = client.get("/voices").json()
    names = {v["name"] for v in voices}
    assert "Aria" in names
    assert "Marco" in names


def test_voice_has_gender_and_style_fields(client):
    voices = client.get("/voices").json()
    voice = voices[0]
    assert "gender" in voice
    assert "style" in voice


def test_voice_gender_values_are_valid(client):
    voices = client.get("/voices").json()
    valid_genders = {"male", "female", "neutral"}
    for v in voices:
        assert v["gender"] in valid_genders


def test_all_seeded_voices_have_non_empty_style(client):
    voices = client.get("/voices").json()
    for v in voices:
        assert v["style"] and isinstance(v["style"], str)
