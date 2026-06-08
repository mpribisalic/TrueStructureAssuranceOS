# Deployment Guide — True Structure Assurance OS

## Architecture

- **Frontend**: Vercel (Next.js) → app.yourdomain.com
- **Backend API**: Railway or Render → api.yourdomain.com  
- **Database**: Railway PostgreSQL or Supabase

## Option A: Railway (Recommended, ~5-15 EUR/month)

### Steps

1. Create Railway account at railway.app
2. New Project → Deploy from GitHub repo
3. Select `mpribisalic/TrueStructureAssuranceOS`
4. Railway auto-detects `railway.json` at repo root
5. Add PostgreSQL plugin to the project
6. Set environment variables (see below)
7. Add custom domain: api.yourdomain.com

### Environment Variables (Railway)

Set these in Railway dashboard → Variables:

| Variable | Value |
|----------|-------|
| APP_ENV | production |
| JWT_SECRET | (generate 32+ char random string) |
| DATABASE_URL | (auto-set by Railway PostgreSQL plugin) |
| CORS_ORIGINS | ["https://app.yourdomain.com"] |
| OBJECT_STORAGE_PROVIDER | local |
| LLM_PROVIDER | mock |

### Automatic Migrations

The startup command runs `alembic upgrade head` before starting the server.
First deploy will create all tables automatically.

## Option B: Render (Free tier available)

1. Create Render account at render.com
2. New → Blueprint → Connect GitHub repo
3. Render reads `render.yaml` automatically
4. Set JWT_SECRET manually in dashboard
5. Add custom domain: api.yourdomain.com

## Frontend Deployment (Vercel)

1. Import repo at vercel.com
2. Set Root Directory: `apps/web`
3. Set environment variable: `NEXT_PUBLIC_API_URL=https://api.yourdomain.com`
4. Add custom domain: app.yourdomain.com

## DNS Setup (Bluehost)

Add CNAME records in Bluehost DNS:

| Name | Type | Value |
|------|------|-------|
| app | CNAME | cname.vercel-dns.com |
| api | CNAME | (Railway/Render provided URL) |
| www | CNAME | (Vercel landing page URL) |

## Load Demo Dataset

After first deployment, seed the demo data:

```bash
# Set API URL
export API_BASE=https://api.yourdomain.com/api/v1

# Seed demo user and project
cd apps/api
uv run python scripts/seed_demo.py

# Run full demo flow
uv run python scripts/demo_flow.py
```

## Health Check

Verify deployment: `GET https://api.yourdomain.com/health`

Expected response:
```json
{"status": "ok", "app": "True Structure Assurance OS", "env": "production", "database": "ok"}
```
