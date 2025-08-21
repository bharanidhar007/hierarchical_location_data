# Hierarchical Location API (FastAPI + PostgreSQL + Redis)

A production-ready FastAPI service for hierarchical location data (Country → State → City → Town) with:
- Browsing, search, pagination, and filters
- Endpoints for each layer
- SQLAlchemy + Alembic migrations
- Seed data loader
- Redis-backed caching (fastapi-cache2)
- Dockerized with Docker Compose
- Automated tests with pytest + httpx
- Optional GraphQL (Strawberry)
- Optional geospatial fields (GeoAlchemy2) & PostGIS
- Basic multilingual support via JSONB `translations` columns

## Quickstart (Docker)
```bash
# 1) copy .env.example to .env and adjust if needed
cp .env.example .env

# 2) build & run
docker compose up --build

# 3) API docs
open http://localhost:8000/docs

# 4) GraphQL (optional)
open http://localhost:8000/graphql

# 5) Run migrations & seed (in another terminal)
docker compose exec api alembic upgrade head
docker compose exec api python scripts/seed_data.py
```

## Local Dev (without Docker)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python scripts/seed_data.py
uvicorn app.main:app --reload
```

## Environment Variables
See `.env.example` for all settings.

## Project Structure
```
app/
  api/v1/endpoints/  # REST endpoints
  core/              # config & constants
  db/                # database session & models
  repositories/      # DB access layer
  schemas/           # Pydantic schemas
  services/          # extra services (cache, search, etc.)
scripts/             # seed loader
alembic/             # migrations
tests/               # pytest
```

## Features
- **Pagination**: `limit` (default 20, max 200) and `offset`
- **Search**: `q` parameter (case-insensitive partial matches)
- **Filters**: by parent id (country/state/city), by code, etc.
- **Caching**: `GET` list endpoints cached with Redis. Use `CACHE_TTL` to control TTL.
- **Multilingual**: name fields + `translations` JSONB, eg: `{ "es": {"name": "España"} }`
- **Geospatial (optional)**: enable PostGIS + GeoAlchemy2 (`USE_POSTGIS=1`) for POINT geometries.
- **GraphQL (optional)**: enable Strawberry GraphQL at `/graphql`.
- **Performance**: indexes on codes & foreign keys; query-optimized repositories.

## Tests
```bash
pytest -q
```

## Notes
- If you enable PostGIS, the `docker-compose.yml` already uses a PostGIS image. Disable by switching to vanilla Postgres image if not needed.
- For MySQL, adjust SQLAlchemy URL and remove PostGIS/JSONB-specific parts.
```

