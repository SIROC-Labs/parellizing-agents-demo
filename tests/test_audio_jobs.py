import pytest


@pytest.fixture
def campaign_id(client):
    response = client.post("/campaigns", json={"name": "Test Campaign", "client_name": "Test Client"})
    return response.json()["id"]


@pytest.fixture
def voice_id(client):
    voices = client.get("/voices").json()
    return voices[0]["id"]


def test_create_audio_job(client, campaign_id, voice_id):
    payload = {
        "campaign_id": campaign_id,
        "script_text": "Welcome to the summer sale. Deals up to 50% off.",
        "voice_id": voice_id,
        "target_duration_seconds": 30,
    }
    response = client.post("/audio-jobs", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["campaign_id"] == campaign_id
    assert data["voice_id"] == voice_id
    assert data["status"] == "queued"
    assert "id" in data
    assert "created_at" in data


def test_create_audio_job_unknown_campaign(client, voice_id):
    payload = {
        "campaign_id": "nonexistent-campaign",
        "script_text": "Some script text.",
        "voice_id": voice_id,
        "target_duration_seconds": 30,
    }
    response = client.post("/audio-jobs", json=payload)
    assert response.status_code == 404


def test_create_audio_job_unknown_voice(client, campaign_id):
    payload = {
        "campaign_id": campaign_id,
        "script_text": "Some script text.",
        "voice_id": "nonexistent-voice",
        "target_duration_seconds": 30,
    }
    response = client.post("/audio-jobs", json=payload)
    assert response.status_code == 404


def test_get_audio_job(client, campaign_id, voice_id):
    payload = {
        "campaign_id": campaign_id,
        "script_text": "Limited offer. Act now.",
        "voice_id": voice_id,
        "target_duration_seconds": 15,
    }
    created = client.post("/audio-jobs", json=payload).json()

    response = client.get(f"/audio-jobs/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_audio_job_not_found(client):
    response = client.get("/audio-jobs/does-not-exist")
    assert response.status_code == 404
