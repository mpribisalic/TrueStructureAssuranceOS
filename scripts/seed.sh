#!/bin/bash
set -e
echo "Seeding demo data..."
cd "$(dirname "$0")/.."
docker compose exec api uv run python scripts/seed_demo.py
