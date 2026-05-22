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


def test_filter_by_gender_male(client):
    voices = client.get("/voices", params={"gender": "male"}).json()
    assert len(voices) > 0
    assert all(v["gender"] == "male" for v in voices)


def test_filter_by_gender_female(client):
    voices = client.get("/voices", params={"gender": "female"}).json()
    assert len(voices) > 0
    assert all(v["gender"] == "female" for v in voices)


def test_filter_by_style(client):
    voices = client.get("/voices", params={"style": "conversational"}).json()
    assert len(voices) > 0
    assert all(v["style"] == "conversational" for v in voices)


def test_filter_by_locale(client):
    voices = client.get("/voices", params={"locale": "en-US"}).json()
    assert len(voices) > 0
    assert all(v["locale"] == "en-US" for v in voices)


def test_filter_by_supports_tts(client):
    voices = client.get("/voices", params={"supports_tts": True}).json()
    assert len(voices) > 0
    assert all(v["supports_tts"] is True for v in voices)


def test_filter_by_supports_sts(client):
    voices = client.get("/voices", params={"supports_sts": True}).json()
    assert len(voices) > 0
    assert all(v["supports_sts"] is True for v in voices)


def test_filter_combined_gender_and_style(client):
    voices = client.get("/voices", params={"gender": "male", "style": "professional"}).json()
    assert len(voices) > 0
    assert all(v["gender"] == "male" and v["style"] == "professional" for v in voices)


def test_filter_no_matches_returns_empty_list(client):
    response = client.get("/voices", params={"gender": "neutral"})
    assert response.status_code == 200
    assert response.json() == []


def test_filter_nonexistent_style_returns_empty_list(client):
    response = client.get("/voices", params={"style": "whispering"})
    assert response.status_code == 200
    assert response.json() == []


def test_no_filters_returns_all_voices(client):
    all_voices = client.get("/voices").json()
    filtered_voices = client.get("/voices", params={}).json()
    assert len(all_voices) == len(filtered_voices)
