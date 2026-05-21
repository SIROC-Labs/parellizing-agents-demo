import uuid
from datetime import datetime, timedelta, timezone

from app.models.audio_job import AudioJob, AudioJobStatus
from app.models.campaign import Campaign, CampaignStatus
from app.models.voice import Voice


def _dt(days_ago: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days_ago)


def run(voice_repo, campaign_repo, audio_job_repo) -> None:
    voices = [
        Voice(id=str(uuid.uuid4()), name="Aria",  provider="elevenlabs", locale="en-US", supports_sts=True,  supports_tts=True,  gender="female", style="conversational"),
        Voice(id=str(uuid.uuid4()), name="Marco", provider="elevenlabs", locale="es-ES", supports_sts=True,  supports_tts=True,  gender="male",   style="conversational"),
        Voice(id=str(uuid.uuid4()), name="Yuki",  provider="google",     locale="ja-JP", supports_sts=False, supports_tts=True,  gender="female", style="professional"),
        Voice(id=str(uuid.uuid4()), name="Lena",  provider="google",     locale="de-DE", supports_sts=False, supports_tts=True,  gender="female", style="professional"),
        Voice(id=str(uuid.uuid4()), name="James", provider="openai",     locale="en-GB", supports_sts=True,  supports_tts=True,  gender="male",   style="energetic"),
    ]
    for v in voices:
        voice_repo.add(v)

    aria, marco, james = voices[0], voices[1], voices[4]

    campaigns = [
        Campaign(id=str(uuid.uuid4()), name="Summer Sale 2025",       client_name="Acme Retail",    status=CampaignStatus.ACTIVE,     created_at=_dt(30)),
        Campaign(id=str(uuid.uuid4()), name="Brand Awareness Q3",     client_name="Nova Insurance", status=CampaignStatus.ACTIVE,     created_at=_dt(14)),
        Campaign(id=str(uuid.uuid4()), name="Product Launch — Spark", client_name="Spark Devices",  status=CampaignStatus.DRAFT,      created_at=_dt(2)),
        Campaign(id=str(uuid.uuid4()), name="Holiday Campaign 2024",  client_name="Acme Retail",    status=CampaignStatus.COMPLETED,  created_at=_dt(120)),
    ]
    for c in campaigns:
        campaign_repo.add(c)

    summer, brand, launch, holiday = campaigns

    audio_jobs = [
        AudioJob(id=str(uuid.uuid4()), campaign_id=summer.id,  voice_id=aria.id,  script_text="Summer's here. Up to 50% off everything in store. This weekend only at Acme Retail.",                       target_duration_seconds=15, status=AudioJobStatus.COMPLETED,  created_at=_dt(28)),
        AudioJob(id=str(uuid.uuid4()), campaign_id=summer.id,  voice_id=james.id, script_text="Don't miss Acme Retail's biggest summer sale. Incredible deals across every department.",                   target_duration_seconds=15, status=AudioJobStatus.COMPLETED,  created_at=_dt(25)),
        AudioJob(id=str(uuid.uuid4()), campaign_id=brand.id,   voice_id=aria.id,  script_text="Nova Insurance. Protecting what matters most. Get a quote today and save up to 20% on your first year.",   target_duration_seconds=30, status=AudioJobStatus.PROCESSING, created_at=_dt(1)),
        AudioJob(id=str(uuid.uuid4()), campaign_id=brand.id,   voice_id=marco.id, script_text="Nova Seguros. Protegemos lo que más importa. Solicita tu presupuesto hoy.",                                target_duration_seconds=30, status=AudioJobStatus.QUEUED,     created_at=_dt(0)),
        AudioJob(id=str(uuid.uuid4()), campaign_id=launch.id,  voice_id=james.id, script_text="Introducing Spark One. The device that changes everything. Available from the first of next month.",        target_duration_seconds=20, status=AudioJobStatus.FAILED,     created_at=_dt(1)),
        AudioJob(id=str(uuid.uuid4()), campaign_id=holiday.id, voice_id=aria.id,  script_text="Happy holidays from Acme Retail. Find the perfect gift for everyone on your list.",                        target_duration_seconds=15, status=AudioJobStatus.COMPLETED,  created_at=_dt(100)),
    ]
    for j in audio_jobs:
        audio_job_repo.add(j)
