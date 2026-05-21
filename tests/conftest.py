import pytest
from fastapi.testclient import TestClient

from app import dependencies
from app.main import app


@pytest.fixture
def client():
    dependencies.campaign_repo._items.clear()
    dependencies.voice_repo._items.clear()
    dependencies.audio_job_repo._items.clear()

    from app import seed
    seed.run(dependencies.voice_repo, dependencies.campaign_repo, dependencies.audio_job_repo)

    yield TestClient(app)

    dependencies.campaign_repo._items.clear()
    dependencies.voice_repo._items.clear()
    dependencies.audio_job_repo._items.clear()
