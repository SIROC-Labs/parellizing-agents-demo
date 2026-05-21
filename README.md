# audio-campaign-api

Demo FastAPI backend for an audio advertising platform. Clients create ad campaigns, pick a voice from a catalogue, and submit scripts to be turned into audio.

**Campaigns** represent an advertising flight for a client. They move through a lifecycle from draft to active to completed.

**Voices** are the available AI narrators. Each voice has a provider, a locale, and flags for what it supports (text-to-speech, speech-to-speech).

**Audio jobs** are the unit of work. A job ties a script to a campaign and a voice, and tracks the status of the audio generation from queued through to completed or failed.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

```bash
uvicorn app.main:app --reload
# open http://localhost:8000/docs
```

## Test

```bash
pytest
```

---

## Your tasks

Pick one. Paste the Asana URL into your AI agent and let it run.

---

### Task 1 — Campaign lifecycle management

Right now a campaign can be created but its status is fixed at `draft` forever. Clients need to be able to move campaigns through their lifecycle: launch them, pause them when budgets run out, and mark them complete when the flight ends.

Add an endpoint to transition a campaign's status. The API should enforce that transitions follow the natural lifecycle — a completed campaign cannot be reactivated, and a draft campaign cannot be paused before it has ever launched. Attempting an invalid transition should return a clear error explaining what transitions are allowed from the current status.

**Acceptance criteria:**
- Clients can change a campaign's status via the API
- Invalid transitions are rejected with a descriptive error
- Valid transitions: `draft → active`, `active → paused`, `active → completed`, `paused → active`, `paused → completed`
- The new endpoint and all transition rules are covered by tests

**How to verify:** grab a campaign ID from `GET /campaigns` — use one with `status: draft`.

```bash
# Valid transition — should return 200 with status: active
curl -X POST http://localhost:8001/campaigns/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'

# Another valid step — should return 200 with status: paused
curl -X POST http://localhost:8001/campaigns/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status": "paused"}'

# Invalid transition — should return 4xx with a clear error
curl -X POST http://localhost:8001/campaigns/{id}/status \
  -H "Content-Type: application/json" \
  -d '{"status": "draft"}'
```

---

### Task 2 — Voice filtering and discovery

The API currently returns all voices in a single flat list with no way to narrow it down. As the voice catalogue grows, clients need to find voices that match their campaign requirements — the right language, the right gender, the right capabilities.

Extend the voice model with additional attributes — at minimum gender and a style descriptor (for example: conversational, professional, energetic). Update the seed data so all existing voices have realistic values. Add filtering to `GET /voices` so clients can pass query parameters to narrow the results. Filters should be combinable.

**Acceptance criteria:**
- Voices have at least two new descriptive attributes
- Seed data reflects realistic values for all voices
- `GET /voices` accepts query params to filter by any combination of locale, gender, style, and capability flags
- Requests with filters that match nothing return an empty list, not an error
- New attributes and filtering behaviour are covered by tests

**How to verify:**

```bash
# New fields visible on each voice
curl http://localhost:8002/voices

# Filter by locale
curl "http://localhost:8002/voices?locale=en-US"

# Filter by gender
curl "http://localhost:8002/voices?gender=female"

# Combined filter
curl "http://localhost:8002/voices?locale=en-US&supports_sts=true"

# No matches — should return [] not an error
curl "http://localhost:8002/voices?locale=zh-CN"
```

---

### Task 3 — Audio job output and completion

Audio jobs are created with status `queued` and then nothing happens — there is no way to record what happened to a job after it was picked up for processing. A job processor needs to be able to mark jobs as completed or failed and attach the result.

Add an endpoint to update a job's status and record the outcome. When a job is marked as completed, the caller must provide the URL where the generated audio file can be found and the actual duration of the output in seconds. When a job is marked as failed, the caller must provide an error message. Jobs already in a terminal state cannot be updated.

**Acceptance criteria:**
- Jobs can be updated to `processing`, `completed`, or `failed` via the API
- Completing a job requires an output URL and the actual duration
- Failing a job requires an error message
- Updating a job already in `completed` or `failed` is rejected
- Output URL and error message are visible when fetching the job
- All new behaviour is covered by tests

**How to verify:** grab a `queued` job ID from `GET /audio-jobs` — the seed data has one.

```bash
# Move to processing — should return 200
curl -X PATCH http://localhost:8003/audio-jobs/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "processing"}'

# Complete it with output — should return 200 with output_url and actual_duration_seconds
curl -X PATCH http://localhost:8003/audio-jobs/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "completed", "output_url": "https://cdn.example.com/out.mp3", "actual_duration_seconds": 28}'

# Try to update a completed job — should return 4xx
curl -X PATCH http://localhost:8003/audio-jobs/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "processing"}'

# Fail a different job without an error message — should return 4xx
curl -X PATCH http://localhost:8003/audio-jobs/{other-id} \
  -H "Content-Type: application/json" \
  -d '{"status": "failed"}'
```
