.PHONY: up down reset logs backend-test frontend-test lint format migrate seed-demo demo

up:
	docker compose up --build

down:
	docker compose down

reset:
	docker compose down -v
	docker compose up --build

logs:
	docker compose logs -f

backend-test:
	cd apps/api && uv run pytest tests/ -v

frontend-test:
	cd apps/web && npm test

lint:
	cd apps/api && uv run ruff check .
	cd apps/web && npm run lint

format:
	cd apps/api && uv run ruff format .

migrate:
	cd apps/api && uv run alembic upgrade head

seed-demo:
	cd apps/api && uv run python scripts/seed_demo.py

demo:
	@echo "Opening demo at http://localhost:3000"
	@echo "API docs at http://localhost:8000/docs"
