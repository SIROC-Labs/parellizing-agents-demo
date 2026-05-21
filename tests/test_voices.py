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
