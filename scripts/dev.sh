#!/bin/bash
set -e
echo "Starting development environment..."
cd "$(dirname "$0")/.."
cp -n .env.example .env || true
docker compose up --build
