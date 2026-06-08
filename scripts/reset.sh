#!/bin/bash
set -e
echo "Resetting environment (volumes will be deleted)..."
cd "$(dirname "$0")/.."
docker compose down -v
docker compose up --build
