# Deployment Guide

## Prerequisites

- Docker 24+ with Docker Compose v2
- 4 GB RAM minimum
- Ports 3000, 8000, 5432, 6379, 9000, 9001 available

## Local Development

```bash
# 1. Clone the repository
git clone https://github.com/mpribisalic/TrueStructureAssuranceOS.git
cd TrueStructureAssuranceOS

# 2. Copy environment file
cp .env.example .env

# 3. Start all services
make up
```

Services started by `make up`:

| Service | URL | Description |
|---------|-----|-------------|
| API | http://localhost:8000 | FastAPI backend |
| Frontend | http://localhost:3000 | Next.js frontend |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health | http://localhost:8000/health | Health check |
| MinIO Console | http://localhost:9001 | Object storage UI |
| PostgreSQL | localhost:5432 | Database |
| Redis | localhost:6379 | Job queue |

## First Run

After `make up` completes:

```bash
# Load demo data
make seed-demo

# Run backend tests
make backend-test
```

Demo credentials:
- Email: `demo@assuranceos.local`
- Password: `demo1234`

## Environment Variables

Copy `.env.example` to `.env` and adjust:

| Variable | Required | Default | Notes |
|----------|----------|---------|-------|
| `DATABASE_URL` | yes | postgres://... | Change user/pass in production |
| `JWT_SECRET` | yes | change-this | Must be strong random string |
| `LLM_PROVIDER` | no | mock | Set to `openai` for real AI |
| `OPENAI_API_KEY` | if openai | — | Only needed for openai provider |
| `JWT_EXPIRES_MINUTES` | no | 1440 | Token lifetime |
| `MAX_UPLOAD_SIZE_MB` | no | 25 | File upload limit |

## Reset

To reset all data and start fresh:

```bash
make reset
```

This deletes all Docker volumes (database, storage, cache).

## Stopping

```bash
make down
```

## Production Notes

For production deployment (outside TRL 4 scope):

1. Set `APP_ENV=production`
2. Use a strong random `JWT_SECRET`
3. Place API behind nginx with TLS
4. Use managed PostgreSQL (RDS, Cloud SQL, etc.)
5. Use managed Redis (ElastiCache, etc.)
6. Replace MinIO with S3
7. Set `ENABLE_SIGNUPS=false`
8. Rotate secrets on first deployment

## Offline / Air-Gapped Deployment

With `LLM_PROVIDER=mock`, the system makes no external network calls.
All services run locally. Suitable for air-gapped environments after initial Docker image pull.
