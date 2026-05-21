from fastapi import FastAPI, HTTPException, Request

from app import dependencies, seed
from app.routers import audio_jobs, campaigns, health, voices
from app.services.errors import NotFound

app = FastAPI(title="audio-campaign-api")


@app.exception_handler(NotFound)
def _not_found(_: Request, exc: NotFound) -> HTTPException:
    raise HTTPException(status_code=404, detail=str(exc))


app.include_router(health.router)
app.include_router(campaigns.router)
app.include_router(voices.router)
app.include_router(audio_jobs.router)

seed.run(dependencies.voice_repo, dependencies.campaign_repo, dependencies.audio_job_repo)
