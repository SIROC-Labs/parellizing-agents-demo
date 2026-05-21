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
