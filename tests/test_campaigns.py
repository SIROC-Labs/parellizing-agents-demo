def test_create_campaign(client):
    payload = {"name": "Summer Radio Push", "client_name": "Acme Corp"}
    response = client.post("/campaigns", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Summer Radio Push"
    assert data["client_name"] == "Acme Corp"
    assert data["status"] == "draft"
    assert "id" in data
    assert "created_at" in data


def test_list_campaigns(client):
    before = len(client.get("/campaigns").json())
    client.post("/campaigns", json={"name": "Campaign A", "client_name": "Brand X"})
    client.post("/campaigns", json={"name": "Campaign B", "client_name": "Brand Y"})

    response = client.get("/campaigns")
    assert response.status_code == 200
    assert len(response.json()) == before + 2


def test_get_campaign(client):
    created = client.post("/campaigns", json={"name": "Promo Wave", "client_name": "Brand Z"}).json()

    response = client.get(f"/campaigns/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_campaign_not_found(client):
    response = client.get("/campaigns/does-not-exist")
    assert response.status_code == 404


def test_list_campaigns_returns_seed_data(client):
    response = client.get("/campaigns")
    assert response.status_code == 200
    assert len(response.json()) > 0


def _create_campaign(client, name="Test Campaign", client_name="Acme"):
    return client.post("/campaigns", json={"name": name, "client_name": client_name}).json()


def test_transition_draft_to_active(client):
    campaign = _create_campaign(client)
    response = client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "active"})
    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_transition_active_to_paused(client):
    campaign = _create_campaign(client)
    client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "active"})
    response = client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "paused"})
    assert response.status_code == 200
    assert response.json()["status"] == "paused"


def test_transition_active_to_completed(client):
    campaign = _create_campaign(client)
    client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "active"})
    response = client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "completed"})
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_transition_paused_to_active(client):
    campaign = _create_campaign(client)
    client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "active"})
    client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "paused"})
    response = client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "active"})
    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_transition_paused_to_completed(client):
    campaign = _create_campaign(client)
    client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "active"})
    client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "paused"})
    response = client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "completed"})
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_invalid_transition_draft_to_paused(client):
    campaign = _create_campaign(client)
    response = client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "paused"})
    assert response.status_code == 422
    assert "draft" in response.json()["detail"]


def test_invalid_transition_completed_to_active(client):
    campaign = _create_campaign(client)
    client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "active"})
    client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "completed"})
    response = client.patch(f"/campaigns/{campaign['id']}/status", json={"status": "active"})
    assert response.status_code == 422
    assert "completed" in response.json()["detail"]


def test_transition_campaign_not_found(client):
    response = client.patch("/campaigns/does-not-exist/status", json={"status": "active"})
    assert response.status_code == 404
