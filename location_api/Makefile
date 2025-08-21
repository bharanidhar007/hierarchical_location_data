.PHONY: up down logs migrate seed test fmt

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f api

migrate:
	docker compose exec api alembic upgrade head

seed:
	docker compose exec api python scripts/seed_data.py

test:
	docker compose exec api pytest -q
