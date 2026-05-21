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


@pytest.fixture
def queued_job(client, campaign_id, voice_id):
    payload = {
        "campaign_id": campaign_id,
        "script_text": "Buy now, limited time offer.",
        "voice_id": voice_id,
        "target_duration_seconds": 30,
    }
    return client.post("/audio-jobs", json=payload).json()


def test_update_job_to_processing(client, queued_job):
    response = client.patch(f"/audio-jobs/{queued_job['id']}", json={"status": "processing"})
    assert response.status_code == 200
    assert response.json()["status"] == "processing"


def test_complete_job(client, queued_job):
    response = client.patch(f"/audio-jobs/{queued_job['id']}", json={
        "status": "completed",
        "output_url": "https://cdn.example.com/audio/job-123.mp3",
        "actual_duration_seconds": 28,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["output_url"] == "https://cdn.example.com/audio/job-123.mp3"
    assert data["actual_duration_seconds"] == 28


def test_fail_job(client, queued_job):
    response = client.patch(f"/audio-jobs/{queued_job['id']}", json={
        "status": "failed",
        "error_message": "Voice synthesis timed out",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "failed"
    assert data["error_message"] == "Voice synthesis timed out"


def test_output_url_and_error_visible_on_fetch(client, queued_job):
    client.patch(f"/audio-jobs/{queued_job['id']}", json={
        "status": "completed",
        "output_url": "https://cdn.example.com/audio/job-abc.mp3",
        "actual_duration_seconds": 15,
    })
    data = client.get(f"/audio-jobs/{queued_job['id']}").json()
    assert data["output_url"] == "https://cdn.example.com/audio/job-abc.mp3"
    assert data["actual_duration_seconds"] == 15


def test_cannot_update_completed_job(client, queued_job):
    client.patch(f"/audio-jobs/{queued_job['id']}", json={
        "status": "completed",
        "output_url": "https://cdn.example.com/audio/done.mp3",
        "actual_duration_seconds": 20,
    })
    response = client.patch(f"/audio-jobs/{queued_job['id']}", json={"status": "processing"})
    assert response.status_code == 409


def test_cannot_update_failed_job(client, queued_job):
    client.patch(f"/audio-jobs/{queued_job['id']}", json={
        "status": "failed",
        "error_message": "Something went wrong",
    })
    response = client.patch(f"/audio-jobs/{queued_job['id']}", json={"status": "processing"})
    assert response.status_code == 409


def test_complete_without_output_url_rejected(client, queued_job):
    response = client.patch(f"/audio-jobs/{queued_job['id']}", json={
        "status": "completed",
        "actual_duration_seconds": 20,
    })
    assert response.status_code == 409


def test_complete_without_duration_rejected(client, queued_job):
    response = client.patch(f"/audio-jobs/{queued_job['id']}", json={
        "status": "completed",
        "output_url": "https://cdn.example.com/audio/done.mp3",
    })
    assert response.status_code == 409


def test_fail_without_error_message_rejected(client, queued_job):
    response = client.patch(f"/audio-jobs/{queued_job['id']}", json={"status": "failed"})
    assert response.status_code == 409


def test_update_nonexistent_job(client):
    response = client.patch("/audio-jobs/does-not-exist", json={"status": "processing"})
    assert response.status_code == 404
