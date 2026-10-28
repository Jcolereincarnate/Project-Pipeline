# Job Pipeline MVP — React + Django

A starter scaffold for discovering jobs from Reddit, deduplicating them in PostgreSQL, and reviewing them in a React dashboard.

## Current scope
- Roles: Backend Engineer, Python / Django Developer, Junior Software Engineer, AI / ML Engineer, Full-Stack Developer
- Locations: Remote worldwide + Nigeria
- Experience: Junior and mid-level
- Sources: Reddit only
- Run modes: manual now; scheduled via Celery Beat when enabled
- Reddit collection uses the official OAuth API. Do not scrape Reddit HTML or bypass access controls.

## Architecture
React (Vite) → Django REST Framework → Pipeline service → Reddit OAuth adapter → normalization/filtering → PostgreSQL.
Pipeline runs are recorded for observability. Jobs use Reddit post IDs for idempotent deduplication. A management command can run the same pipeline outside the UI.

## Important Reddit API gate
This scaffold deliberately does not pretend that API access is already approved. Before live collection:
1. Review Reddit's current Data API Terms and Responsible Builder Policy.
2. Request/confirm the appropriate API access and describe the intended job-discovery use case accurately.
3. Create OAuth credentials only through Reddit's approved developer flow.
4. Put credentials in `.env`; never commit them.
5. Keep request rates conservative and respect API responses, limits, and policy requirements.

Until approved credentials are configured, the pipeline fails clearly rather than scraping pages or using unofficial workarounds.

## Prerequisites
- Python 3.11+
- Node.js LTS + npm
- PostgreSQL 14+
- Reddit API credentials if approved

## Backend setup
```bash
cd backend
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set DATABASE_URL, Django SECRET_KEY, and approved Reddit OAuth values.
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API: `http://127.0.0.1:8000/api/`
- `GET /api/jobs/`
- `GET /api/pipeline/runs/`
- `POST /api/pipeline/run/`

Run via CLI:
```bash
python manage.py run_pipeline
```

## Frontend setup
In a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Frontend expects Django at `http://127.0.0.1:8000`. Set `VITE_API_BASE_URL` in `frontend/.env` if needed.

## Scheduled runs (optional MVP extension)
The scaffold includes Celery dependencies and a task. To activate scheduling:
1. Run Redis.
2. Start a Celery worker.
3. Start Celery Beat.
4. Configure `CELERY_BEAT_SCHEDULE` in `backend/config/settings.py` to your desired cadence.
Do not enable a frequent schedule until API access and rate-limit behaviour are confirmed.

## First implementation milestones
1. Boot backend and frontend locally.
2. Run Django tests and verify migrations.
3. Test the API with Reddit access disabled (expected safe error).
4. Add approved Reddit OAuth credentials and validate a small, low-rate run.
5. Tune query terms/subreddits and relevance filters against real examples.
6. Add user authentication before exposing the dashboard publicly.
7. Enable scheduled runs only after the manual path is stable.

## Production checklist
- Add authentication/permissions to pipeline endpoints.
- Use HTTPS, secure environment variables, logging and monitoring.
- Set a single scheduler instance to avoid duplicate scheduled tasks.
- Add run locking if manual and scheduled runs could overlap.
- Keep source post IDs and permalinks for traceability.
- Review Reddit's terms/policy before changing collection, storage, or display behaviour.
