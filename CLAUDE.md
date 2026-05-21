# audio-campaign-api — Agent Instructions

## Project

Python FastAPI backend for audio advertising. Manages campaigns, voices, and audio generation jobs. In-memory storage, no database, no auth.

**Repository:** https://github.com/SIROC-Labs/parellizing-agents-demo

## Dev commands

```bash
# Install
python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"

# Run (default port 8000)
uvicorn app.main:app --reload

# Run on a specific port
uvicorn app.main:app --reload --port 8001

# Tests
pytest -v
```

## Architecture

```
app/models/        — domain objects (Campaign, Voice, AudioJob)
app/schemas/       — API request/response shapes
app/repositories/  — in-memory data access
app/services/      — business logic; raises NotFound for missing records
app/routers/       — thin HTTP layer, one file per domain
app/dependencies.py — singleton repos + Depends() factories
app/seed.py        — example voices loaded at startup
tests/conftest.py  — TestClient fixture with isolated state per test
```

All business logic lives in services. Routers only parse requests and call services. Keep it that way.

## Existing endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/campaigns` | List all campaigns |
| `POST` | `/campaigns` | Create a campaign (`name`, `client_name`) |
| `GET` | `/campaigns/{id}` | Get a campaign |
| `GET` | `/voices` | List all voices |
| `POST` | `/audio-jobs` | Create an audio job |
| `GET` | `/audio-jobs/{id}` | Get an audio job |

## Available tasks

These are the three tasks attendees implement. Each touches a single domain so three agents can run in parallel without conflicts.

**Task 1 — Campaign lifecycle management** (`feature/campaign-lifecycle`)
Campaigns are stuck in `draft` forever. Add an endpoint to transition campaign status. Valid transitions: `draft → active`, `active → paused`, `active → completed`, `paused → active`, `paused → completed`. Invalid transitions must return a clear error. All existing tests must pass unchanged.
Files: `app/models/campaign.py`, `app/services/campaign_service.py`, `app/routers/campaigns.py`, `tests/test_campaigns.py`.

**Task 2 — Voice filtering and discovery** (`feature/voice-filtering`)
The voice list has no filters. Add `gender` (male/female/neutral) and `style` (e.g. conversational, professional, energetic) to the Voice model. Update seed data with realistic values for all existing voices. Add query parameters to `GET /voices` so clients can filter by any combination of `locale`, `gender`, `style`, `supports_sts`, and `supports_tts`. Filtering with no matches returns an empty list.
Files: `app/models/voice.py`, `app/schemas/voice.py`, `app/repositories/voice_repository.py`, `app/services/voice_service.py`, `app/routers/voices.py`, `app/seed.py`, `tests/test_voices.py`.

**Task 3 — Audio job output and completion** (`feature/job-completion`)
Jobs are created as `queued` and never updated. Add an endpoint to update job status. Completing a job requires `output_url` (string) and `actual_duration_seconds` (int). Failing a job requires `error_message` (string). Jobs already in `completed` or `failed` cannot be updated. Both fields must be visible when fetching the job.
Files: `app/models/audio_job.py`, `app/schemas/audio_job.py`, `app/services/audio_job_service.py`, `app/routers/audio_jobs.py`, `tests/test_audio_jobs.py`.

---

## Automated task workflow

When the user gives you an Asana task URL (with or without additional text), follow these steps in order. Do not skip steps.

### Step 1 — Read the task

Use the Asana MCP tools to fetch the task. Extract:
- Task title (used to derive the branch name)
- Task description (the specification you will implement)
- Any subtasks or attached context

### Step 2 — Derive names

From the task title, produce:
- **branch name**: `feature/<slug>` where slug is the title lowercased, spaces replaced with `-`, special chars removed. Example: "Add campaign filters" → `feature/add-campaign-filters`
- **worktree directory**: `.worktrees/<branch-slug>` inside the repo. Example: `.worktrees/add-campaign-filters`

### Step 3 — Create the worktree

From the root of this repository:

```bash
git worktree add .worktrees/<branch-slug> -b feature/<slug>
```

Verify it was created:
```bash
git worktree list
```

### Step 4 — Set up the worktree

```bash
cd .worktrees/<branch-slug>
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Verify setup:
```bash
.venv/bin/python -c "import fastapi; print('ok')"
```

### Step 5 — Analyse, plan, implement

Work inside the worktree directory (`.worktrees/<branch-slug>`).

Follow the standard feature development workflow:
- Read the full task description carefully
- Explore the relevant files in the codebase to understand what needs to change
- Use `superpowers:writing-plans` to create an implementation plan
- Use `superpowers:executing-plans` or `superpowers:subagent-driven-development` to implement it
- Run `pytest -v` after implementation and fix any failures before continuing

### Step 6 — Find a free port

Check ports 8001 through 8010 and use the first one that is not in use:

```bash
for port in 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010; do
  if ! lsof -i :$port &>/dev/null 2>&1; then
    echo $port
    break
  fi
done
```

### Step 7 — Start the server

From the worktree directory, start the server in the background on the port found in Step 6:

```bash
nohup .venv/bin/uvicorn app.main:app --port <PORT> > /tmp/audio-api-<PORT>.log 2>&1 &
echo $! > /tmp/audio-api-<PORT>.pid
```

Wait 2 seconds, then verify it started:

```bash
curl -s http://localhost:<PORT>/health
```

Report the following to the user:
- The URL: `http://localhost:<PORT>`
- The API docs: `http://localhost:<PORT>/docs`
- The log file path for debugging: `/tmp/audio-api-<PORT>.log`

### Step 8 — Push and create PR

From the worktree directory:

```bash
git push -u origin feature/<slug>
```

Then create a pull request with `gh`:

```bash
gh pr create \
  --title "<Task title>" \
  --body "$(cat <<'EOF'
## Summary
<bullet points describing what was implemented>

## Test plan
- [ ] `pytest -v` passes
- [ ] Server running at http://localhost:<PORT> — verify via /docs

Asana: <task URL>
EOF
)"
```

### Step 9 — Post a comment on the Asana task

Use the Asana MCP tools to post a comment on the original task. The comment should include:
- A one-line summary of what was implemented
- The PR URL
- The local URL for manual testing: `http://localhost:<PORT>/docs`

Example comment:
```
Implemented. PR: <PR URL>
Running locally for review: http://localhost:<PORT>/docs
```

Do not change the task status, assignee, or any other field. Only post the comment.

---

## Stopping a running instance

To stop a server started by this workflow:

```bash
kill $(cat /tmp/audio-api-<PORT>.pid) && rm /tmp/audio-api-<PORT>.pid
```

## Notes for agents

- Work entirely inside the worktree directory after Step 3. Do not modify files in the original repo.
- The repo root is the base. Treat files outside `.worktrees/` as read-only during task execution.
- If the worktree already exists for a branch, skip Step 3 and continue from Step 4.
- If the port check finds no free port in range 8001–8010, report this to the user and stop.
- If tests fail after implementation, fix them before proceeding to Step 7. Do not ship failing tests.
